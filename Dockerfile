FROM python:3.13.2

WORKDIR /app

WORKDIR /app/app

COPY . .

COPY . /app

RUN pip install -r requarement.txt

CMD ["python", "main.py"]