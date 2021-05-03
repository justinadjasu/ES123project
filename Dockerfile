FROM python:latest
WORKDIR /usr/src/app
COPY ./ /usr/src/app/
RUN pip install -r requirements.txt
ENV APP_HOST=project123es.herokuapp.com
CMD ["bokeh serve --port 5006 --allow-websocket-origin project123es.herokuapp.com:5000 --allow-websocket-origin project123es.herokuapp.com:5006 applet & echo hello", "sleep 10; python3 application.py"]