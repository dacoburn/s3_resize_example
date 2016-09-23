FROM iron/python:3-dev
# Install packages.
#RUN apk update && apk upgrade && apk add openssh-client && rm -rf /var/cache/apk/*
RUN apk update && apk add build-base python3-dev jpeg-dev zlib-dev && rm -rf /var/cache/apk/* 
RUN pip3 install boto3 uuid PILLOW
ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR /app
ADD . /app
ENTRYPOINT ["python3", "python_resize.py"]
