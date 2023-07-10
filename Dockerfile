FROM python:3.10.5-slim-buster

RUN sed -i -e 's/http:\/\/deb\.debian\.org\/debian/http:\/\/thsdiza06repo02\.ent04\.res\/apt\/debian/' /etc/apt/sources.list

RUN apt update 

WORKDIR /inventory-4ce

COPY pip.conf pip.conf

COPY requirements.txt requirements.txt

ENV PIP_CONFIG_FILE pip.conf

RUN pip install --trusted-host pypi.org -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
