FROM python:3.10.8
RUN mkdir -p /app_send_email
WORKDIR /app_send_email
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 3008
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD [ "flask","run","-p","3008"]