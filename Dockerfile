FROM python:3.12.2

RUN pip install --upgrade pip

# install all dependencies
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# only install taxifare after installing the dependencies so the
# dependencies will be updated on taxifare
COPY /app /app
#RUN pip install .

#COPY Makefile Makefile

#CMD uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT
CMD uvicorn app.main:app --host 0.0.0.0  --port $PORT
