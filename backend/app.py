from flaskr import create_app
from flask import Flask,render_template

app = create_app()

@app.route("/index")
def index():
    return render_template("../frontend/index.html")


app.run( debug=True, host="0.0.0.0", port=50000)