from flask import Flask, request, send_from_directory
from photo_storage import FOLDER, save_photo

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
PAGE = """
<!doctype html>
<title>Photo Upload Test</title>
<h1>Upload a photo</h1>
<form method="post" enctype="multipart/form-data">
  <input type="file" name="photo" accept="image/*">
  <button type="submit">Upload</button>
</form>
{result}
"""


@app.route("/", methods=["GET", "POST"])
def upload():
    result = ""
    if request.method == "POST":
        photo = request.files.get("photo")
        if not photo or not photo.filename:
            result = "<p>Please choose a photo first.</p>"
        else:
            try:
                filename = save_photo(photo)
                result = f"""
                <p>Upload successful!</p>
                <img src="/uploads/{filename}" width="300">
                """
            except ValueError as error:
                result = f"<p>{error}</p>"
    return PAGE.format(result=result)


@app.route("/uploads/<filename>")
def uploaded_photo(filename):
    return send_from_directory(FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)