FROM python:3.9-slim

WORKDIR /webapp/backend

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5005

ENV FLASK_APP=webapp.backend.app

WORKDIR /

# CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5005", "--cert", "adhoc", "--debug"]  
CMD ["sh", "-c", "celery -A webapp.backend.async_tasks.celery_worker.celery worker --loglevel=info & flask run --host 0.0.0.0 --port 5005 --cert adhoc --debug"]