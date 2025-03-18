FROM python:3.12-slim
ARG PIP_EXTRA_INDEX_URL

ARG PIP_EXTRA_INDEX_URL
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cargo \
    git \
    libffi-dev \
    librdkafka-dev \
    libssl-dev \
    python3-dev

WORKDIR /app

ENV PATH /home/worker/.local/bin:${PATH}

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["python", "api/main.py", "--host", "0.0.0.0"]
