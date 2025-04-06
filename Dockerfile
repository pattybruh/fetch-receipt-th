FROM python:3.11-slim

#env vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install flask pandas numpy tensorflow matplotlib

#port that flask runs on
EXPOSE 5000

#run command
CMD ["python", "app.py"]
