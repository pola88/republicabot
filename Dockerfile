FROM python:3

COPY ./requirements.txt /republicaboot/requirements.txt

WORKDIR /republicaboot

RUN pip install -r requirements.txt

COPY . /republicaboot

CMD [ "python", "./app/main.py" ]
