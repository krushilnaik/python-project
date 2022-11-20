FROM python:3.9-slim

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://localhost:5000/health || exit 1

EXPOSE 5000

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD flask run --host 0.0.0.0
