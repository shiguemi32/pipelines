FROM platiagro/datascience-1386e2046833-notebook-cpu:0.0.2

WORKDIR /app

ENV MODEL_NAME Model
ENV API_TYPE REST
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0
ENV PARAMETERS '[{"type":"STRING","name":"dataset","value":""},{"type":"STRING","name":"target","value":""},{"type":"STRING","name":"experiment_id","value":""}]'
ENV LOG_LEVEL DEBUG

EXPOSE 5000

COPY Model.py /app/Model.py

CMD ["sh", "-c", "seldon-core-microservice \"$MODEL_NAME\" \"$API_TYPE\" --service-type \"$SERVICE_TYPE\" --persistence \"$PERSISTENCE\" --parameters \"$PARAMETERS\" --log-level \"$LOG_LEVEL\""]
