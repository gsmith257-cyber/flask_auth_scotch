FROM python:3-alpine

RUN apk update && \
    apk add mariadb mariadb-dev && \
    apk add mariadb-connector-c-dev

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

RUN export FLASK_APP=project


# Bundle app source
COPY . .

EXPOSE 80
CMD [ "flask", "run", "--host","0.0.0.0","--port","5000"]
