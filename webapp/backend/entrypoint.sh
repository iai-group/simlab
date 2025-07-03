#!/bin/bash
set -e 

echo "Starting custom entrypoint script..."

# --- GCS Credentials Setup ---
if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
  echo "WARNING: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set."
  echo "Gcsfuse will attempt to use Application Default Credentials (ADC) or may fail."
  echo "Ensure you have mounted a service account key or configured ADC for the container."
fi

# --- GCS Fuse Mounting ---
GCS_BUCKET_NAME="${GCS_BUCKET_NAME}"
# Define the internal mount point for the GCS bucket (must match Dockerfile mkdir)
GCS_MOUNT_POINT="/mnt/gcs_bucket"

if [ -z "$GCS_BUCKET_NAME" ]; then
  echo "ERROR: GCS_BUCKET_NAME environment variable is not set. Cannot mount bucket."
  exit 1
fi

echo "Attempting to mount GCS bucket '$GCS_BUCKET_NAME' to '$GCS_MOUNT_POINT'..."

mkdir -p "$GCS_MOUNT_POINT"
chown -R $(whoami):$(id -gn) "$GCS_MOUNT_POINT"

gcsfuse \
    --implicit-dirs \
    --file-mode=664 \
    --dir-mode=775 \
    "$GCS_BUCKET_NAME" "$GCS_MOUNT_POINT" &

# Check if mounting was successful
sleep 3
if mountpoint -q "$GCS_MOUNT_POINT"; then
  echo "GCS bucket mounted successfully at $GCS_MOUNT_POINT."
else
  echo "ERROR: GCS bucket mount failed! Check gcsfuse logs for more details."
  exit 1
fi

# --- Start the main application ---
echo "Starting Flask and Celery application..."
exec "$@"
