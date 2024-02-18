FROM python:3.9-buster

WORKDIR /code

ENV PORT 7000

COPY requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y git

RUN pip3 install --force-reinstall -r requirements.txt

COPY . /code

ENV PYTHONPATH "${PYTHONPATH}:."

EXPOSE 7000/tcp

CMD [ "python", "src/main.py" ]
