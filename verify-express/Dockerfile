FROM python:3.10.8
RUN mkdir -p /app_verify_express
WORKDIR /app_verify_express
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 3007
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD [ "flask","run","-p","3007"]