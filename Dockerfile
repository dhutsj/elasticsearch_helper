# Test workflow
FROM python:3.7.9

WORKDIR /home
ADD source .
RUN mkdir ~/.pip
RUN echo "\
[global] \n\
index-url=http://mirrors.aliyun.com/pypi/simple/ \n\
[install] \n\
trusted-host=mirrors.aliyun.com" > ~/.pip/pip.conf
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD python app.py 
