FROM python:3-slim

WORKDIR /usr/src/app

ENV FLASK_APP=pinger 
ENV FLASK_ENV=development
ENV DATA_FOLDER=/pinger-data 
ENV AWS_SHARED_CREDENTIALS_FILE=/aws/credentials

#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask boto3

COPY . .

#CMD [ "python", "./main.py" ]
CMD ["flask","run", "--host", "0.0.0.0", "--port", "5000"] 