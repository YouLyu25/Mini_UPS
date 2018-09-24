FROM ubuntu:16.04

RUN mkdir /ups_code
RUN apt-get update && apt-get -y install python3
RUN apt-get update && apt-get -y install python3-pip
RUN python3 -m pip install threadpool
RUN python3 -m pip install google
RUN python3 -m pip install six
RUN python3 -m pip install psycopg2

WORKDIR /ups_code
ADD . /ups_code
ADD init_curr_world.sh /ups_code
EXPOSE 6666
CMD python3 /ups_code/ups_server.py
