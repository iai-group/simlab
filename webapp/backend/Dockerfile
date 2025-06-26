FROM python:3.9-slim

# Install system dependencies required for Docker
RUN apt-get update && apt-get install -y \
    curl \
    lsb-release \
    fuse \
    gnupg2 \
    ca-certificates \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | tee /etc/apt/trusted.gpg.d/docker.asc \
    && echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list \
    && apt-get update && apt-get install -y docker-ce-cli \
    && apt-get clean

RUN export GCSFUSE_REPO=gcsfuse-$(lsb_release -c -s) \
    && echo "deb https://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list

RUN apt-get update && apt-get install -y --no-install-recommends gcsfuse \
    && apt-get clean

RUN mkdir -p /mnt/gcs_bucket

WORKDIR /webapp/backend

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5005

ENV FLASK_APP=webapp.backend.app

WORKDIR /

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5005", "--cert", "adhoc", "--debug"]  
CMD ["sh", "-c", "celery -A webapp.backend.async_tasks.celery_worker.celery worker --loglevel=info --time-limit=900 & flask run --host 0.0.0.0 --port 5005 --cert adhoc --debug"]