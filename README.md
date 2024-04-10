# begin_with_yourself_bot_3

## Installation

1. Clone the repository:
   ```bash
   cd ~/Dev/
   git clone git@github.com:Studio-Yandex-Practicum/begin_with_yourself_bot_3.git
   cd begin_with_yourself_bot_3
   ```
2. Create a virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Setup Environment Variables

After installation create a file named `.env` by duplicating the provided `.env.example`. Adjust the parameters as necessary.
```bash
cp .env.example .env
```

## Run backend

```bash
cd backend/
python manage.py migrate
python manage.py runserver
```

## Run telegram_client

```bash
cd telegram_client/
python main.py
```

## Run linter

```bash
cd ~/Dev/begin_with_yourself_bot_3
pylint $(git ls-files '*.py')
```

## Run backend with PostgreSQL in Docker

```bash
cd begin_with_yourself_bot_3/
docker compose up
```
in a separate terminal:
```bash
cd backend/
python manage.py migrate
python manage.py runserver
```
run migrations for tg_bot database:
```bash
cd telegram_client/
alembic upgrade head

## Load fixtures

```bash
python manage.py loaddata workout_types.json
```