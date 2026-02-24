FROM python:3.9

WORKDIR /app

COPY web/requirements.txt .
RUN pip install -r requirements.txt \
    && pip install contrast-security

COPY web/ .

RUN mkdir -p /app/static/archivos
RUN chmod -R 777 /app/static

CMD ["python", "app.py"]
