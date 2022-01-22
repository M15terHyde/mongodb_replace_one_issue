FROM python:3.10.1
COPY ./products/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN apt update; apt upgrade -y

COPY products/main.py /app/main.py
COPY support /app/support/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]