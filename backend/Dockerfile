FROM python:3.12.3-slim-bookworm

WORKDIR /home/app

RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

    COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install  -r requirements.txt

COPY app.py models.py ./

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]