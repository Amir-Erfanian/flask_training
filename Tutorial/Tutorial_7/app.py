import os
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = "lajflkdj"
app.config["UPLOAD_FOLDER"] = os.path.join(
    "static",
    "uploads"
)

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif"
}

def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

@app.route("/upload", methods=["GET", "POST"])
def upload():

    filename = None

    if request.method == "POST":

        if "image" not in request.files:

            flash(
                "No file selected.",
                "danger"
            )

            return redirect(url_for("upload"))

        image = request.files["image"]

        if image.filename == "":

            flash(
                "Please choose a file.",
                "warning"
            )

            return redirect(url_for("upload"))

        if allowed_file(image.filename):

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            flash(
                "Upload successful!",
                "success"
            )

        else:

            flash(
                "Only PNG, JPG, JPEG and GIF are allowed.",
                "danger"
            )

    return render_template(
        "upload.html",
        filename=filename
    )




if __name__ == '__main__':
    app.run(debug=True)