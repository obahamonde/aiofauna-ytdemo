FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["aiofauna","dev"]


# docker run -d -p 8080:8080 -v app:/app python-development