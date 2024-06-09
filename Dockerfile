FROM python:3.9.10-slim-buster

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt && pip install python-dotenv

COPY . .

EXPOSE 3000

CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
