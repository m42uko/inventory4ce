FROM python:3.10.5-slim-buster

RUN apt update 

WORKDIR /inventory-4ce

COPY requirements.txt requirements.txt

RUN pip install --trusted-host pypi.org -r requirements.txt

COPY . .

WORKDIR /inventory-4ce/inventory4ce
VOLUME /inventory-4ce/inventory4ce/_data

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
