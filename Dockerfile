FROM python:3.12-slim
ARG PIP_EXTRA_INDEX_URL
ARG GITHUB_ACCESS_TOKEN

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cargo \
    git \
    libffi-dev \
    librdkafka-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/* \
    python3-dev

WORKDIR /app

ENV PATH /home/worker/.local/bin:${PATH}
ENV GITHUB_ACCESS_TOKEN ${GITHUB_ACCESS_TOKEN}

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV GITHUB_ACCESS_TOKEN unset

COPY . .

CMD ["python", "api/main.py", "--host", "0.0.0.0"]
