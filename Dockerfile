FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY pyproject.toml .
COPY backend ./backend
COPY core ./core
COPY tests ./tests
COPY README.md .
COPY SURAYA_CORE_SPEC.md .

RUN pip install --no-cache-dir .

RUN mkdir -p /app/data

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
