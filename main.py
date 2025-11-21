from flask import Flask, render_template, request, redirect
from config import db, database_actions
from utils.env_provider import DATABASE_URL, HOST_URL


app = Flask(__name__)
app.config["SQLALCHEMY_ENGINES"] = {"default": DATABASE_URL}

db.init_app(app)


@app.route("/healthz", methods=["GET"])
def health():
    return "website is working!"


@app.route("/", methods=["GET"])
def home():
    return render_template("pages/home.html")


@app.route("/url", methods=["POST"])
def get_url():

    original_url = request.form["original_url"]

    short_url = database_actions.store_url_to_db(original_url=original_url)

    full_short_url = f"{HOST_URL}/{short_url}"

    if not original_url:
        return "No url provides", 404

    return render_template("pages/home.html", short_url=full_short_url)


@app.route("/<short_url>", methods=["GET"])
def url_redirect(short_url: str):

    short_url = short_url.split("/")[-1]

    database_actions.increment_visit_count(short_url=short_url)

    redirect_url = database_actions.get_redirect_url(short_url=short_url)

    return redirect(f"{redirect_url}")


@app.route("/analytics", methods=["GET"])
def analytics():
    return render_template("pages/analytics.html")


@app.route("/analytics", methods=["POST"])
def get_url_data():

    full_url = request.form["url"]

    if not full_url:
        return "No url provided", 404

    short_url = full_url.split("/")[-1]

    url_info = database_actions.get_url_data(short_url=short_url)

    return render_template("pages/analytics.html", url_info=url_info)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
