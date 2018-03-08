FROM amazonlinux
EXPOSE 7777 

COPY solution /opt/devops-challenge

RUN yum -y install python35 python35-devel python35-pip python35-setuptools python35-virtualenv 
RUN pip-3.5 install --upgrade pip && \
    pip-3.5 install -r /opt/devops-challenge/requirements.txt
WORKDIR "/opt/devops-challenge"

ENV PYTHONPATH=.:$PYTHONPATH=/opt/devops-challenge/
