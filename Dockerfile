FROM python:3

RUN ln -fs /usr/share/zoneinfo/America/Argentina/Buenos_Aires /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

COPY ./requirements.txt /republicaboot/requirements.txt

WORKDIR /republicaboot

RUN pip install -r requirements.txt

COPY . /republicaboot

CMD [ "python", "./app/main.py" ]
