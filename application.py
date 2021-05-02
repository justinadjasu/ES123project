# python native modules
import sys
import os
from uuid import uuid4

from flask import Flask, flash, redirect, render_template, request, url_for, session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# bokeh embed import
from bokeh.embed import server_document

# BIG TODO LIST:
# Allow password change feature, complete w/ email send to change password when forgotten 
# Error checking within prepare_data(), remember to rm saved file from disk and database if of incompatible format
# Password specifications (length, special characters, etc.)
# During web integration process, likely need to change cookie system
# Find solution if error in bokeh server? (May not be not necessary, as error checking in prepare data should ensure format of pickles are as needed)
# Recontact sql server in case of disconnect
# highlight current page


# Configure application
app = Flask(__name__)
app.secret_key = "lmao bro"
app.debug = True

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"


BOKEH_URL = f"http://{os.environ.get('APP_HOST')}:5007/bokeh_server"

@app.route("/", methods=['GET', 'POST'])
def index():
    script = server_document(url=BOKEH_URL)
    return render_template('index.html', script=script)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))