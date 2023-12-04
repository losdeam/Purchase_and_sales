from flaskr import create_app
from flask import Flask,render_template

app = create_app()

app.run( debug=True, host="0.0.0.0", port=50000)