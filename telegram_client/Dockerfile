FROM python:3.11
WORKDIR /telegram_client
COPY ../requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY telegram_client/ telegram_client/
COPY tg_client.py .
CMD ["python", "tg_client.py"]