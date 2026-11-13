
import sys
from html import escape
from pathlib import Path
from flask import Flask, request, send_from_directory

prototypes = Path(__file__).parent.parent
sys.path.append(str(prototypes / "ai_tagging"))
sys.path.append(str(prototypes.parent))

from photo_storage import FOLDER, get_path, save_photo
from tag_test import get_photo_details
from database.database import add_item, add_tags, get_all_locations

USER_ID = 1 # hardcoded for now until login page is done

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

PAGE = """
<!doctype html>
<title>AI Upload Test</title>
<h1>Add Item</h1>
<form method="post" enctype="multipart/form-data" action="/items/new">
    <input type="file" name="photo" accept="image/*">
    <button type="submit">Upload</button>
</form>

{result}
"""

ITEM_FORM = """
<img src="/uploads/{filename}" width="300">
<p>{message}</p>
<form method="post" action="/items/save">
    <input type="hidden" name="filename" value="{filename}">
    <p>Name:<br>
    <input name="name" value="{name}" required></p>
    <p>Description:<br>
    <textarea name="description">{description}</textarea></p>
    <p>Tags (comma separated):<br>
    <input name="tags" value="{tags}"></p>
    <p>Location:<br>
    <select name="location_id" required>
        {locations}
    </select></p>
    <button type="submit">Save Item</button>
</form>
"""


def location_options():
    options = ""
    for location_id, name, _ in get_all_locations():
        options += f'<option value="{location_id}">{escape(name)}</option>'
    return options


@app.route("/", methods=["GET", "POST"])
@app.route("/items/new", methods=["GET", "POST"])
def add_item_page():
    result = ""
    if request.method == "POST":
        photo = request.files.get("photo")
        if not photo or not photo.filename:
            result = "<p>Please choose a photo first.</p>"
        else:
            try:
                filename = save_photo(photo)
            except ValueError as error:
                return PAGE.format(result=f"<p>{escape(str(error))}</p>")
            name = ""
            description = ""
            tags = ""

            try:
                details = get_photo_details(get_path(filename))

                name = details.name
                description = details.description
                tags = ", ".join(details.tags)
                message = "AI suggestions are ready. You can edit them below."
            except Exception as error:
                print(f"AI tagging failed: {error}")
                message = "AI tagging failed. Please enter the details manually."

            locations = location_options()
            if not locations:
                message += " Please add a storage location first."

            result = ITEM_FORM.format(
                filename=escape(filename, quote=True),
                message=message,
                name=escape(name, quote=True),
                description=escape(description),
                tags=escape(tags, quote=True),
                locations=locations
            )

    return PAGE.format(result=result)


@app.route("/items/save", methods=["POST"])
def save_item():
    filename = request.form.get("filename", "")
    name = request.form.get("name", "").strip()
    location_id = request.form.get("location_id", "")
    valid_photo = (
        "/" not in filename
        and "\\" not in filename
        and get_path(filename).is_file()
    )
    if not name or not location_id.isdigit() or not valid_photo:
        return PAGE.format(
            result="<p>Missing or invalid item details. Please try again.</p>"
        )
    description = request.form.get("description", "")

    tags = []
    for tag in request.form.get("tags", "").split(","):
        tag = tag.strip().lower()
        if tag:
            tags.append(tag)

    item_id = add_item(
        USER_ID,
        name,
        description,
        int(location_id),
        photo_path=filename
    )
    add_tags(item_id, tags)

    return PAGE.format(result=f"<p>Saved {escape(name)}!</p>")


@app.route("/uploads/<filename>")
def uploaded_photo(filename):
    return send_from_directory(FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
