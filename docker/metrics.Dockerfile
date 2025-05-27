FROM python:3.10-slim

WORKDIR /app

COPY requirements/requirements_metrics.txt /app/
RUN pip install --no-cache-dir -r requirements_metrics.txt

COPY metrics_server /app/metrics_server

CMD ["uvicorn", "metrics_server.metrics_server:app", "--host", "0.0.0.0", "--port", "8000"]