FROM python:3.9.24

WORKDIR /usr/src/app

COPY ../requirements.txt .
COPY ../update_from_csv.py .

RUN pip install -r requirements.txt

CMD ["python", "update_from_csv.py"]
