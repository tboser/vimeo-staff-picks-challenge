FROM ubuntu:17.10

# Set working directory
WORKDIR /usr/share/flask-app

# Install python and pip
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# install Python modules
ADD requirements.txt /usr/share/flask-app/requirements.txt
RUN pip install -r requirements.txt

# Expose
EXPOSE  5000
COPY . /usr/share/flask-app

# Run
ENTRYPOINT ["python"]
CMD ["run-flask.py"]