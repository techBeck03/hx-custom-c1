FROM python:slim-buster

RUN pip install ansible
RUN apt-get update && apt-get install sshpass -y
RUN ansible-galaxy collection install cisco.intersight

COPY . /app
WORKDIR /app

CMD ansible-playbook -i inventory hx.yml --ask-vault-pass