FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc make git curl && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash appuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .
USER appuser

CMD ["make", "all"]
