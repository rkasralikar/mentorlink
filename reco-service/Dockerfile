FROM python:3.9-buster

WORKDIR /code

ENV PORT 9011

COPY requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y git

RUN pip3 install --force-reinstall -r requirements.txt

COPY . /code

ENV PYTHONPATH "${PYTHONPATH}:."

EXPOSE 9011/tcp

ARG log_level
ENV LOGLEVEL ${log_level}
ARG config_file
ENV CONF_FILE ${config_file}
ENV INARG=${CONF_FILE:+"-c ${CONF_FILE} -l ${LOGLEVEL}"}

RUN echo ${INARG}

CMD [ "sh", "-c", "echo ${INARG}; python src/main.py ${INARG}" ]
