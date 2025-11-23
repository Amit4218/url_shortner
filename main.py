from flask import Flask, render_template, request, redirect
from config import db, database_actions
from utils.env_provider import DATABASE_URL, HOST_URL
from utils import RequestExtractor
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
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

        extractor = RequestExtractor(requset=request)

        short_url = short_url.split("/")[-1]

        database_actions.increment_visit_count(
            short_url=short_url,
            ip_address=extractor.get("ip_address"),
            device_type=extractor.get("device_type"),
        )

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

        # Extract device types from UrlData list
        device_types = [d.device_type for d in url_info["data"]]

        device_count = {"android": 0, "linux": 0, "windows": 0, "macos": 0, "other": 0}

        for device in device_types:
            if not device:
                continue

            device = device.lower()

            if device == "android":
                device_count["android"] += 1
            elif device == "linux":
                device_count["linux"] += 1
            elif device == "windows":
                device_count["windows"] += 1
            elif device == "macos":
                device_count["macos"] += 1
            else:
                device_count["other"] += 1

        return render_template(
            "pages/analytics.html", url_info=url_info, data=url_info["data"]
        )
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


@app.route("/temp")
def temp():
    e = RequestExtractor(requset=request)

    return e.extract_request_details()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
