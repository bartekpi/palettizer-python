FROM python:3.7-slim as build
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
