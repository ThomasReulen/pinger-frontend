FROM --platform=linux/amd64 python:3-slim

WORKDIR /usr/src/app

ENV AWS_SHARED_CREDENTIALS_FILE=/aws/credentials
ENV FLASK_APP=pinger 
ENV FLASK_ENV=development
ENV DATA_FOLDER=/pinger-data 
ENV DATA_FOLDER_TARGET=/pinger-data-target
ENV IP=8.8.8.8
ENV DELTA_SECONDS=10000

#RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install -y ssh rsync zip curl  && \
    pip install flask boto3 && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm awscliv2.zip

COPY . .

#CMD [ "python", "./main.py" ]
CMD ["flask","run", "--host", "0.0.0.0", "--port", "5000"] 
