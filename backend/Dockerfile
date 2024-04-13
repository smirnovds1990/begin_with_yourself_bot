FROM python:3.11
WORKDIR /backend
RUN pip install gunicorn==21.2.0
COPY ../requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY backend/ .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "backend.wsgi"]