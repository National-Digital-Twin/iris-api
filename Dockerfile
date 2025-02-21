FROM python:3.11-slim
ARG PIP_EXTRA_INDEX_URL

ARG PIP_EXTRA_INDEX_URL
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PATH /home/worker/.local/bin:${PATH}

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0"]
