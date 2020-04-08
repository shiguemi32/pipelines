FROM platiagro/datascience-1386e2046833-notebook-cpu:0.0.2

COPY . /app
WORKDIR /app

EXPOSE 5000

ENV MODEL_NAME Predictor
ENV API_TYPE REST
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0

CMD seldon-core-microservice $MODEL_NAME $API_TYPE \
    --service-type $SERVICE_TYPE \
    --persistence $PERSISTENCE \
    --parameters $PARAMETERS