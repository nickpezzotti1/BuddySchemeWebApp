from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1> Hello World! </h1>"

# We only need this for local dev
if __name__ == '__main__':
    app.run(debug=True)
