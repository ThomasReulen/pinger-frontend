FROM python:3-slim

WORKDIR /usr/src/app

ENV FLASK_APP=pinger 
ENV FLASK_ENV=development

#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask 

COPY . .

#CMD [ "python", "./main.py" ]
CMD ["flask","run", "--host", "0.0.0.0", "--port", "5000"] 