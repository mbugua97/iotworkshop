FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY Requirements.txt /app/

RUN pip install --upgrade pip \
    && pip install -r Requirements.txt


COPY . /app/

EXPOSE 8200

CMD ["uvicorn", "toggle.asgi:application", "--host", "0.0.0.0", "--port", "8200", "--workers", "20"]