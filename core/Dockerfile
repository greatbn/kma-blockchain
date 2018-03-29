FROM python:2.7.12

WORKDIR /app/
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app/
ENTRYPOINT [ "python", "/app/app.py" ]