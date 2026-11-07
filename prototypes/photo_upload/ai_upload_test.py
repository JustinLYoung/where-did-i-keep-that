import sys
from html import escape
from pathlib import Path
from flask import Flask, request, send_from_directory

sys.path.append(str(Path(__file__).parent.parent / "ai_tagging"))
from photo_storage import FOLDER, get_path, save_photo
from tag_test import get_photo_details

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

PAGE = """
<!doctype html>
<title>AI Upload Test</title>
<h1>Add Item</h1>

<form method="post" enctype="multipart/form-data">
    <input type="file" name="photo" accept="image/*">
    <button type="submit">Upload</button>
</form>
{result}
"""


ITEM_FORM = """
<img src="/uploads/{filename}" width="300">
<p>{message}</p>
<form>
    <p>Name:<br>
    <input name="name" value="{name}"></p>
    <p>Description:<br>
    <textarea name="description">{description}</textarea></p>
    <p>Tags:<br>
    <input name="tags" value="{tags}"></p>
    <button disabled>Save item (coming soon)</button>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def add_item():
    result = ""

    if request.method == "POST":
        photo = request.files.get("photo")
        if not photo or not photo.filename:
            result = "<p>Please choose a photo first.</p>"
        else:
            try:
                filename = save_photo(photo)
            except ValueError as error:
                return PAGE.format(result=f"<p>{error}</p>")
            name = description = tags = ""

            try:
                details = get_photo_details(get_path(filename))
                name = details.name
                description = details.description
                tags = ", ".join(details.tags)
                message = "AI suggestions are ready. You can edit them below."
            except Exception as error:
                print(f"AI tagging failed: {error}")
                message = "AI tagging failed. Please enter the details manually."

            result = ITEM_FORM.format(
                filename=filename,
                message=message,
                name=escape(name),
                description=escape(description),
                tags=escape(tags)
            )

    return PAGE.format(result=result)


@app.route("/uploads/<filename>")
def uploaded_photo(filename):
    return send_from_directory(FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)
