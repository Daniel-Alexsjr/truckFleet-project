FROM python:3.13.3-slim

WORKDIR /app

RUN pip install pandas

COPY app/ /app/

CMD ["python", "main.py"]