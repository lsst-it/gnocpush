FROM python:3.12

WORKDIR /app
COPY . .
RUN pip install .
ENTRYPOINT ["gnocgateway"]
