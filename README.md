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

## Run backend without Docker

set in .env:
DB_HOST=localhost
DB_PORT=5432

```bash
cd ~/Dev/begin_with_yourself_bot_3/
docker compose up db
cd backend/
python manage.py migrate
python manage.py runserver
```
Go to http://localhost:8000/

## Run telegram_client without Docker

set in .env:
DB_HOST=localhost
DB_PORT=5433

```bash
cd ~/Dev/begin_with_yourself_bot_3/
docker compose up telegram_db
python tg_client.py
```
Open @bot_name (where 'bot_name' is your bot's name) in telegram and send '/start'

## Run backend in Docker

set in .env:
DB_HOST=db
DB_PORT=5432

```bash
cd begin_with_yourself_bot_3/
docker compose up db backend nginx
```
in a separate terminal:
```bash
docker compose exec backend python manage.py collectstatic
docker compose exec backend cp -r /backend/collected_static/. /backend_static/static/
```
```bash
docker compose exec -it backend python manage.py migrate
```
Go to http://localhost:8000/

## Run backend in Docker

set in .env:
DB_HOST=telegram_db
DB_PORT=5432

```bash
cd begin_with_yourself_bot_3/
docker compose up telegram_db telegram_client
```

run migrations for tg_bot database:
```bash
docker compose exec telegram_client alembic upgrade head
```
Open @bot_name (where 'bot_name' is your bot's name) in telegram and send '/start'

## Run linter

```bash
cd ~/Dev/begin_with_yourself_bot_3/
pylint $(git ls-files '*.py')
```

## Load fixtures

```bash
python manage.py loaddata workout_types.json
```