FROM platiagro/datascience-1386e2046833-notebook-cpu:0.0.2

COPY . /app
WORKDIR /app

EXPOSE 5000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["seldon-core-microservice", "$MODEL_NAME", "$API_TYPE", \
    "--service-type", "$SERVICE_TYPE", \
    "--persistence", "$PERSISTENCE", \
    "--parameters", "$PARAMETERS", \
    "--log-level", "$LOG_LEVEL"]

