FROM python:3.8-aplpine

RUN mkdir /usr/src/app/
COPY ./code /usr/src/app/
WORKDIR /usr/src/app/

ENV FLASK_APP=app.py 
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True

RUN apk update && apk add --no-cache python3-dev gcc libc-dev musl-dev linux-headers tesseract-orc tesseract-ocr-data-spa
RUN apk add -u zlib-dev jpeg-dev gcc musl-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run"]