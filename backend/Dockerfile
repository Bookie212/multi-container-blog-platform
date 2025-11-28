FROM python:3.11-slim

WORKDIR /home/app

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install  --no-cache-dir -r requirements.txt

COPY app.py models.py ./

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]