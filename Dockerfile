FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/