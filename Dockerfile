# base image  
FROM python:3.9   
# setup environment variable  

 
WORKDIR /banking_system

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# install dependencies  
RUN pip install --upgrade pip  

# copy whole project to your docker home directory. 
COPY . /banking_system/
# run this command to install all dependencies  
RUN pip install -r requirements.txt  
# port where the Django app runs  
EXPOSE 8000  
# start server  
COPY ./start-script.sh /
ENTRYPOINT ["sh", "/start-script.sh"]
