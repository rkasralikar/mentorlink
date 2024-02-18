FROM python:3.9-buster

WORKDIR /code

ENV PORT 5000
ENV KAFKA_PORT 9196

COPY requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y git

RUN apt-get install -y jq

RUN pip3 install --force-reinstall -r requirements.txt

COPY . /code

ENV PYTHONPATH "${PYTHONPATH}:."

EXPOSE 5000/tcp
EXPOSE 5001/tcp
EXPOSE 5002/tcp
EXPOSE 5003/tcp
EXPOSE 9196/tcp
EXPOSE 11935/tcp

ARG etl_list
ENV ETL_LIST ${etl_list}
ARG freq
ENV FREQ ${freq}
ARG log_level
ENV LOGLEVEL ${log_level}
ARG rest_server_config_file
ENV REST ${rest_server_config_file}
ARG kafka_config_file
ENV KAFKA ${kafka_config_file}
ENV KINARG=${KAFKA:+"-k ${KAFKA} -l ${LOGLEVEL}"}
ENV RINARG=${REST:+"-r ${rest_server_config_file} -l ${LOGLEVEL}"}
ENV INARG=${KINARG:-${RINARG:-"-e ${ETL_LIST} -f ${FREQ} -l ${LOGLEVEL}"}}
ENV INARG=${INARG:-${RINARG:+$RINARG}}
ENV INARG=${INARG:-${KINARG:+$KINARG}}
CMD [ "sh", "-c", "echo ${INARG}; python src/main.py ${INARG}" ]

