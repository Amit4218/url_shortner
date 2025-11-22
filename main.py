from flask import Flask, render_template, request, redirect
from config import db, database_actions
from utils.env_provider import DATABASE_URL, HOST_URL


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/healthz", methods=["GET"])
def health():
    return "website is working!"


@app.route("/", methods=["GET"])
def home():
    return render_template("pages/home.html")


@app.route("/url", methods=["POST"])
def get_url():

    try:

        original_url = request.form["original_url"]

        if not original_url:
            raise Exception("Please provide a url, No url provided!")

        short_url = database_actions.store_url_to_db(original_url=original_url)

        full_short_url = f"{HOST_URL}/{short_url}"

        return render_template("pages/home.html", short_url=full_short_url)

    except Exception as error:
        return render_template("pages/home.html", message=error)


@app.route("/<short_url>", methods=["GET"])
def url_redirect(short_url: str):

    try:

        short_url = short_url.split("/")[-1]

        database_actions.increment_visit_count(short_url=short_url)

        redirect_url = database_actions.get_redirect_url(short_url=short_url)

        if not redirect_url:
            raise Exception("Error redirecting... Please check the url.")

        return redirect(f"{redirect_url}")

    except Exception as error:
        return render_template("pages/home.html", message=error)


@app.route("/analytics", methods=["GET"])
def analytics():
    return render_template("pages/analytics.html")


@app.route("/analytics", methods=["POST"])
def get_url_data():
    try:

        full_url = request.form["url"]

        if not full_url:
            raise Exception("Please provide a url, No url provided!")

        short_url = full_url.split("/")[-1]

        url_info = database_actions.get_url_data(short_url=short_url)

        if not url_info:
            raise Exception(
                "No data was found for the url, Are you sure the url is correct?"
            )

        return render_template("pages/analytics.html", url_info=url_info)
    except Exception as error:
        return render_template(
            "pages/analytics.html",
            message=error,
        )


@app.route("/<short_url>/analytics", methods=["GET", "POST"])
def pre_fetch_data(short_url):

    url_info = database_actions.get_url_data(short_url=short_url)

    if not url_info:
        return render_template(
            "pages/analytics.html",
            message="No data was found for the url, Are you sure the url is correct?",
        )

    return render_template("pages/analytics.html", url_info=url_info)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
