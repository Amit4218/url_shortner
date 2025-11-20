from flask import Flask, render_template, request
from config import db
from utils.env_provider import DATABASE_URL


app = Flask(__name__)
app.config["DATABASE_URL"] = DATABASE_URL

db.init_app(app)


@app.route("/healthz")
def health():
    return "website is working!"


# pages route


@app.route("/", methods=["GET"])
def home():
    return render_template("base.html")


@app.route("/url", methods=["POST"])
def get_url():

    original_url = request.form["original_url"]

    if not original_url:
        return "No url provides", 404

    return render_template("")


# action route


# post url


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
