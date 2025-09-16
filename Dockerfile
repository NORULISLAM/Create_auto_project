FROM python:3.10-slim

WORKDIR /app

COPY . .


RUN pip install --no-cache-dir -r requirements.txt

RUN chmod -R 777 /app

EXPOSE 7860

CMD ["python", "app.py"]

