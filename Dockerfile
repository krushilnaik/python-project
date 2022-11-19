FROM python:3.9-slim

EXPOSE 5000

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

# COPY . .

CMD [ "flask", "run", "--host", "0.0.0.0" ]
