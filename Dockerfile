FROM python:3.8

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 8501
COPY . /app
RUN chmod +x /app/up.sh

ENTRYPOINT ["/app/up.sh"]
