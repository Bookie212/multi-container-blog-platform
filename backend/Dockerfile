FROM python:3.12-alpine

WORKDIR /home/app

RUN apk add --no-cache postgresql-libs

RUN apk add --no-cache --virtual .build-deps \
    gcc \ 
    musl-dev \ 
    postgresql-dev

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install  --no-cache-dir -r requirements.txt

RUN apk del .build-deps

COPY app.py models.py ./

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]