FROM python:2.7.12

WORKDIR /app/
COPY core/requirements.txt .
RUN pip install -r requirements.txt

COPY ./core/ /app/
ENTRYPOINT [ "python", "app.py" ]