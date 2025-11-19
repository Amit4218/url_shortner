from flask import Flask, render_template

app = Flask(__name__)


@app.route("/healthz")
def health():
    return "website is working!"


# pages route

@app.route("/", methods=["GET"])
def home():
    return render_template("base.html")


@app.route("/url", methods=["POST"])
def get_url():
    return render_template("")


# action route


# post url


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
