FROM python:3.12-bookworm

WORKDIR /usr/src/app

COPY requirements.txt requirements.pi.txt ./

RUN pip install --no-cache-dir --prefer-binary -r requirements.pi.txt

COPY . .

CMD [ "python", "./service.py" ]
