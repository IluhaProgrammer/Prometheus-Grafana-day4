# 📊 FastAPI + Prometheus + Grafana — Application Metrics Lab

Учебный проект для практического освоения **application-level мониторинга** с использованием **FastAPI**, **Prometheus** и **Grafana**.

Проект выполнен в рамках изучения мониторинга (Day 4) и демонстрирует, как приложение **самостоятельно экспортирует метрики**, которые затем собираются Prometheus и визуализируются в Grafana.


## 🎯 Цели проекта

* Понять разницу между **infrastructure metrics** и **application metrics**
* Реализовать экспорт метрик из FastAPI
* Научиться работать с:

  * `Counter`
  * `Histogram`
* Настроить `/metrics` endpoint
* Подключить Prometheus и Grafana через Docker Compose
* Визуализировать:

  * RPS
  * Latency (p95)
  * Errors

## 🧠 Что мониторим

### Метрики

* **http_requests_total** — общее количество HTTP-запросов
* **request_duration_seconds** — время обработки запросов

### SRE Golden Signals

* **Requests** — нагрузка (RPS)
* **Latency** — скорость ответа (p95)
* **Errors** — стабильность (5xx)

## 🏗 Архитектура

```
Client
   ↓
FastAPI (/metrics)
   ↓
prometheus_client
   ↓
Prometheus
   ↓
Grafana
```

## 🗂 Структура проекта

```
fastapi-metrics-lab/
├── app/
│   └── main.py
│   └── requirements.txt
│   └── Dockerfile
├── prometheus/
│   └── prometheus.yml
├── docker-compose.yml
└── README.md
```


## 🚀 Запуск проекта

### Требования

* Docker
* Docker Compose

### Запуск

```bash
docker compose up -d --build
```

После запуска будут доступны:

* FastAPI: [http://localhost:8000](http://localhost:8000)
* Метрики: [http://localhost:8000/metrics](http://localhost:8000/metrics)
* Prometheus: [http://localhost:9090](http://localhost:9090)
* Grafana: [http://localhost:3000](http://localhost:3000)


## 🔌 FastAPI эндпоинты

| Endpoint   | Описание                        |
| ---------- | ------------------------------- |
| `/`        | Базовый endpoint                |
| `/slow`    | Медленный запрос (latency test) |
| `/error`   | Возвращает 500 ошибку           |
| `/metrics` | Prometheus metrics              |


## 📈 Prometheus метрики

### Requests (RPS)

```promql
sum(rate(http_requests_total[1m]))
```

### Errors (5xx)

```promql
sum(rate(http_requests_total{status=~"5.."}[1m]))
```

### Latency (p95)

```promql
histogram_quantile(
  0.95,
  sum(rate(request_duration_seconds_bucket[1m])) by (le)
)
```


## 📊 Grafana

Grafana подключена к Prometheus как Data Source.

Реализованы графики:

* 📈 RPS (Requests per Second)

<img width="534" height="336" alt="image" src="https://github.com/user-attachments/assets/3c8a0950-4501-4670-aa36-0476d7b15df4" />


* ⏱ p95 Latency

<img width="610" height="368" alt="image" src="https://github.com/user-attachments/assets/b7efebe7-b366-4791-98d8-d65e50ef5346" />


* ❌ Error Rate (5xx)

<img width="608" height="367" alt="image" src="https://github.com/user-attachments/assets/bf70608d-546b-4815-aa73-4d3e4c64a365" />


## 🐳 Docker

* FastAPI собирается через **Dockerfile**
* Prometheus и Grafana запускаются через **docker-compose**
* Используется внутренняя Docker-сеть


## 🧪 Что было проверено вручную

* Генерация нагрузки через `/slow`
* Генерация ошибок через `/error`
* Проверка роста счётчиков
* Проверка изменения p95 latency


## 🧠 Ключевые выводы

* Prometheus **не считает метрики**, он их собирает
* Application metrics должны экспортироваться из кода
* `Histogram` — основной инструмент для latency
* Labels дают гибкость, но требуют аккуратного использования


## 📚 Используемые технологии

* FastAPI
* prometheus_client
* Prometheus
* Grafana
* Docker / Docker Compose
* VScode

## 👨‍💻 Автор

Проект выполнен в учебных целях в рамках прокачки навыков **DevOps / SRE**.


🔥 Проект используется как практическая база для дальнейшего изучения:

* Alertmanager
* Logging - ELK
* RED / USE методологий
