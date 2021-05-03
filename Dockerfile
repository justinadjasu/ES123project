FROM python:latest
WORKDIR /usr/src/app
COPY ./ /usr/src/app/
RUN pip install -r requirements.txt
CMD [ "APP_HOST=project123es.herokuapp.com", "bokeh serve --port 5006 --allow-websocket-origin $$APP_HOST:5000 --allow-websocket-origin $$APP_HOST:5006 applet & echo hello", "sleep 10; python3 application.py" ]