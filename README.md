# Incident API — Маленький API-сервис для учёта инцидентов.


# Как запустить

## Клонируйте репозиторий

```
git clone git@github.com:Nikitkosss/incidents-api.git
cd incidents-api
```

## Убедитесь, что у вас есть .env файл с переменными:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_PORT=5434
POSTGRES_SERVER=127.0.0.1
```

## Запуск через Docker

```
docker compose up --build
```

## Или создайте и активируйте виртуальное окружение (рекомендуется)

```
python -m venv venv
source venv/bin/activate    # Linux/macOS
# или
venv\Scripts\activate       # Windows
```

## Установите зависимости

```
pip install -r requirements.txt
```

## Запустите сервер

```
uvicorn main:app --host 127.0.0.1 --port 8000
```

### Сервер будет доступен по адресу: http://127.0.0.1:8000
### Документация Swagger UI: http://127.0.0.1:8000/docs 

## Доступные эндпоинты:
### Создать инцидент
```curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/incidents/create_incident' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "description": "string",
    "source": "operator"
  }'
```
### Ответ:
```
{
  "id": 8,
  "description": "string",
  "status": "open",
  "source": "operator",
  "created_at": "2025-11-07T09:53:44.207655"
}
```
### Получить инциденты (с фильтром по статусу)
```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/incidents/get_incidents?status=in_progress' \
  -H 'accept: application/json'
```
### Ответ:
```
[
  {
    "id": 3,
    "description": "string",
    "status": "in_progress",
    "source": "operator",
    "created_at": "2025-11-07T09:21:41.798351"
  },
  {
    "id": 7,
    "description": "string",
    "status": "in_progress",
    "source": "operator",
    "created_at": "2025-11-07T09:52:39.369946"
  }
]
```
### Обновить статус инцидента
```
curl -X 'PATCH' \
  'http://127.0.0.1:8000/api/v1/incidents/update_incident?incident_id=7' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "status": "closed"
  }'
```
### Ответ:
```
{
  "id": 7,
  "description": "string",
  "status": "closed",
  "source": "operator",
  "created_at": "2025-11-07T09:52:39.369946"
}
```

## Примечания

#### Статусы инцидентов: open, in_progress, closed (определяются через IncidentStatus enum).
#### Попытка перевести инцидент в статус open через PATCH — запрещена (возвращается 400).
#### Для локальной разработки используйте ```--reload``` при запуске uvicorn.