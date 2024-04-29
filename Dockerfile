FROM python:3.12

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .
ENTRYPOINT ["gnocpush"]
