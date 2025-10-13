FROM python:3.9.24

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /usr/src/app

COPY ../requirements.txt .
COPY ../update_from_csv.py .

RUN pip install -r requirements.txt

# Change ownership of necessary files and directories to the non-root user
RUN chown -R appuser:appuser update_from_csv.py

# Switch to the non-root user
USER appuser

CMD ["python", "update_from_csv.py"]
