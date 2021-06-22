FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /image_uploader
COPY requirements.txt /image_uploader/requirements.txt
RUN pip install -r requirements.txt
COPY . /image_uploader/