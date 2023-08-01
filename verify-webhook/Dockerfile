FROM python:3.10.8
RUN mkdir -p /app_verify_webhook
WORKDIR /app_verify_webhook
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 3006
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD [ "flask","run","-p","3006"]