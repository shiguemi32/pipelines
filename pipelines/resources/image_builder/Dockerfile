FROM python:3.6-buster

COPY . /app
WORKDIR /app

EXPOSE 5000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["seldon-core-microservice", "$MODEL_NAME", "$API_TYPE", \
    "--service-type", "$SERVICE_TYPE", \
    "--persistence", "$PERSISTENCE", \
    "--parameters", "$PARAMETERS", \
    "--log-level", "$LOG_LEVEL"]

