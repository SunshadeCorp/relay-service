FROM python:3-buster

WORKDIR /usr/src/app

RUN pip install pigpio~=1.78 gpiozero~=1.6.2 paho-mqtt~=1.5.1 PyYAML~=5.4.1

COPY . .

CMD [ "python", "./service.py" ]
