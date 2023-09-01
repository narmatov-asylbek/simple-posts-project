## Technical stack
- Python 3.11
- PostgreSQL
- FastAPI

## API

1. Create and activate virtual environment

``` shell
cd starnavi
virtualenv -p python3.11 .venv
source .venv/bin/activate
```

2. Installing requirements

``` shell
pip install -r requirements.txt
```

3. Exporting Environment variables and migrate

``` shell
EXPORT DB_URI="postgresql+psycopg2://test:test@localhost:5432/test"

alembic upgrade head
```
4. Running uvicorn server

``` shell
uvicorn app.main:app --host 0.0.0.0 --reload
```

5. Swagger documentation on `/docs`

## Bot
1. Update a file named `bot_config.toml'
2. Run `bot.py`:

``` shell
python bot.py
```
