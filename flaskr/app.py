from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html") 

# We only need this for local dev
if __name__ == '__main__':
    app.run(debug=True)
