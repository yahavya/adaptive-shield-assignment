from flask import Flask, request, send_from_directory, abort, render_template

app = Flask(__name__, static_folder="tmp")

STATIC_DIRECTORY = "/tmp/"


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/images")
def images():
    img_url = request.args.get("animal")
    if img_url:
        try:
            print("found the url" + img_url)
            print("static directory: ", STATIC_DIRECTORY)
            return send_from_directory(STATIC_DIRECTORY, img_url)
        except FileNotFoundError:
            abort(404, description="Resource not found")
    else:
        return "<p>No image specified</p>"


@app.route("/<path:filename>")
def send_file(filename):
    return send_from_directory(app.static_folder, filename)
