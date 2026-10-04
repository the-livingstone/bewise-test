# bewise-test

Сервис **Walk the dog** — небольшое REST API на FastAPI для приёма и просмотра заявок. Новые заявки сохраняются в PostgreSQL и публикуются в топик Kafka `applications`.

## Стек

- **Python 3.11**, Poetry
- **FastAPI** + **Uvicorn**
- **SQLAlchemy 2** (async) + **asyncpg**
- **PostgreSQL 15**
- **Apache Kafka** (aiokafka)

## Быстрый старт (Docker)

1. Скопируйте переменные окружения:

   ```bash
   cp env.example .env
   ```

2. Для запуска API в контейнере укажите в `.env` хост PostgreSQL как имя сервиса Compose:

   ```env
   POSTGRES_HOST=postgres
   KAFKA_SERVER=kafka
   ```

3. Поднимите инфраструктуру и приложение:

   ```bash
   docker compose up --build
   ```

4. API будет доступен на порту из `API_PORT` (по умолчанию **8000**).

При `DEBUG=True` в `.env` открывается интерактивная документация: `http://localhost:8000/_docs`.

## Локальная разработка (без Docker для API)

1. Установите зависимости:

   ```bash
   poetry install
   ```

2. Поднимите PostgreSQL и Kafka.

3. Настройте `.env` (хосты `localhost` / порты с хост-машины).

4. Создайте таблицы и запустите сервер из каталога пакета:

   ```bash
   cd bewise_test
   poetry run python -m app.main
   ```

   При первом запуске `main` создаёт схему БД через SQLAlchemy.

## Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `DEBUG` | Режим отладки, Swagger на `/_docs` | `False` |
| `TESTING` | Флаг тестового режима | `False` |
| `API_HOST` | Хост Uvicorn | `0.0.0.0` |
| `API_PORT` | Порт API | `8000` |
| `POSTGRES_USER` | Пользователь БД | — |
| `POSTGRES_PASSWORD` | Пароль БД | — |
| `POSTGRES_HOST` | Хост PostgreSQL | `postgres` (в коде) |
| `POSTGRES_PORT` | Порт PostgreSQL | `5432` |
| `POSTGRES_NAME` | Имя базы | `db` |
| `POSTGRES_MIN_POOL_SIZE` | Размер пула соединений | `1` |
| `POSTGRES_MAX_POOL_SIZE` | Максимальный оверфлоу пула | `5` |
| `KAFKA_SERVER` | Хост брокера | `kafka` |
| `KAFKA_PORT` | Порт брокера | `9092` |

Файл конфигурации читается из `.env` относительно рабочей директории (см. `bewise_test/app/config.py`).

## API

### `POST /applications`

Создать заявку.

**Тело запроса (JSON):**

```json
{
  "user_name": "ivan",
  "description": "Нужна помощь с прогулкой"
}
```

**Ответ:** объект заявки с полями `id`, `user_name`, `description`, `created_at`. Событие уходит в Kafka.

### `GET /applications`

Список заявок с пагинацией и фильтром.

| Query-параметр | Описание | По умолчанию |
|----------------|----------|--------------|
| `username` | Фильтр по имени пользователя | без фильтра |
| `page` | Номер страницы | `1` |
| `page size` | Размер страницы | `10` |

**Пример:**

```bash
curl "http://localhost:8000/applications?username=ivan&page=1&page%20size=10"
```

Ошибки домена обрабатываются как JSON с полями `status_code` и `title`.

## Структура проекта

```
bewise_test/
  app/
    main.py          # точка входа, lifespan, Kafka producer
    routes.py        # HTTP-маршруты
    service.py       # создание заявки: БД + Kafka
    models.py        # доменная модель
    schemas.py       # DTO запросов
    messages.py      # публикация в Kafka
    config.py        # настройки из .env
    db/
      base.py        # engine, session
      orm.py         # SQLAlchemy-модели
      repos.py       # репозиторий заявок
docker-compose.yml   # postgres, kafka, fastapi
Dockerfile
pyproject.toml
env.example
```

## Compose-сервисы

| Сервис | Назначение |
|--------|------------|
| `postgres` | PostgreSQL, данные в `.docker-volumes/postgres` |
| `kafka` | Брокер, при старте создаётся топик `applications` |
| `fastapi` | Образ приложения, порт `API_PORT` |
