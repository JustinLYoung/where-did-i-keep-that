import sqlite3
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from flask import Flask, request, redirect, url_for, render_template, send_file, send_from_directory, abort
from prototypes.qr_code.qr_prototype import generate_qr

from database.database import (
    DATABASE_PATH,
    get_all_locations,
    add_storage_location,
    update_storage_location,
    delete_storage_location,
    get_all_items,
    add_item,
    add_tags,
    update_item,
    delete_item,
    search_items
)

from prototypes.photo_upload.photo_storage import FOLDER, get_path, save_photo
from prototypes.ai_tagging.tag_test import error_message, get_photo_details

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

USER_ID = 1  # Temp until login is implemented

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        location_name = request.form["location_name"]
        description = request.form["description"]

        add_storage_location(1, location_name, description)

        return redirect(url_for("home"))

    locations = get_all_locations()

    search_term = request.args.get("search", "").strip()
    location_filter = request.args.get("location_id", "")

    # Empty means "All locations"
    if location_filter.isdigit():
        location_filter = int(location_filter)
    else:
        location_filter = None

    if search_term or location_filter:
        items = search_items(search_term, location_filter)
    else:
        items = get_all_items()

    return render_template(
        "index.html",
        locations=locations,
        items=items,
        search_term=search_term,
        location_filter=location_filter
    )

@app.route("/edit/<int:location_id>", methods=["GET", "POST"])
def edit_location(location_id):

    user_id = 1  # Temp until login is implemented

    if request.method == "POST":

        location_name = request.form["location_name"]
        description = request.form["description"]

        update_storage_location(
            user_id,
            location_id,
            location_name,
            description
        )

        return redirect(url_for("home"))

    locations = get_all_locations()

    # Find the location we want to edit
    location = next(
        (item for item in locations if item[0] == location_id),
        None
    )

    if location is None:
        return "Storage location not found", 404

    return render_template("edit_location.html", location=location)


@app.route("/delete/<int:location_id>", methods=["POST"])
def delete_location(location_id):

    user_id = 1  # Temp until login is implemented

    deleted = delete_storage_location(user_id, location_id)

    if not deleted:
        return "Cannot delete this location. It contains items or doesn't exist.", 400

    return redirect(url_for("home"))


@app.route("/add-item", methods=["POST"])
def add_new_item():

    user_id = 1  # Temp until login is implemented

    item_name = request.form["item_name"]
    description = request.form["description"]

    location_id = request.form["location_id"]

    # Convert the selected location ID to an integer
    # An empty selection means the item has no assigned location
    if location_id:
        location_id = int(location_id)
    else:
        location_id = None

    add_item(user_id, item_name, description, location_id)

    return redirect(url_for("home"))


@app.route("/edit-item/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):

    user_id = 1  # Temporary until login is implemented

    if request.method == "POST":

        item_name = request.form["item_name"]
        description = request.form["description"]
        location_id = request.form["location_id"]

        if location_id:
            location_id = int(location_id)
        else:
            location_id = None

        update_item(
            user_id,
            item_id,
            item_name,
            description,
            location_id
        )

        return redirect(url_for("home"))

    # Find the item being edited
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT item_id, item_name, description, location_id
        FROM items
        WHERE user_id = ? AND item_id = ?;
    """, (user_id, item_id))

    item = cursor.fetchone()
    connection.close()

    if item is None:
        return "Item not found", 404

    locations = get_all_locations()

    return render_template(
        "edit_item.html",
        item=item,
        locations=locations
    )


@app.route("/delete-item/<int:item_id>", methods=["POST"])
def delete_inventory_item(item_id):

    user_id = 1  # Temporary until login is implemented

    deleted = delete_item(user_id, item_id)

    if not deleted:
        return "Item not found or could not be deleted.", 404

    return redirect(url_for("home"))

@app.route("/qr/<int:location_id>")
def download_location_qr(location_id):
    # Check that the storage location exists
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT location_id
        FROM storage_locations
        WHERE location_id = ? AND user_id = ?
    """, (location_id, 1))

    location = cursor.fetchone()
    connection.close()

    if location is None:
        abort(404)

    # Build the URL that the QR code will contain
    location_url = f"{request.url_root.rstrip('/')}/locations/{location_id}"

    # Generate the QR code using our existing prototype
    with TemporaryDirectory() as temp_folder:
        qr_path = Path(temp_folder) / "location_qr.png"
        generate_qr(location_url, qr_path)
        qr_image = BytesIO(qr_path.read_bytes())

    # Return the QR code as a downloadable PNG
    return send_file(
        qr_image,
        mimetype="image/png",
        as_attachment=True,
        download_name=f"location_{location_id}_qr.png"
    )

@app.route("/items/new", methods=["GET", "POST"])
def add_item_page():
    if request.method == "GET":
        return render_template("add_item.html")

    photo = request.files.get("photo")

    if not photo or not photo.filename:
        return render_template(
            "add_item.html",
            message="Please choose a photo first."
        )

    try:
        filename = save_photo(photo)
    except ValueError as error:
        return render_template(
            "add_item.html",
            message=str(error)
        )

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
        message = error_message(error) + " Please enter the details manually."

    locations = get_all_locations()
    if not locations:
        message += " Please add a storage location first."

    return render_template(
        "add_item.html",
        filename=filename,
        name=name,
        description=description,
        tags=tags,
        locations=locations,
        message=message
    )

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
        return render_template(
            "add_item.html",
            message="Missing or invalid item details. Please try again."
        ), 400

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

    return redirect(url_for("home"))

@app.route("/uploads/<filename>")
def uploaded_photo(filename):
    return send_from_directory(FOLDER, filename)


@app.errorhandler(413)
def file_too_large(error):
    return render_template(
        "add_item.html",
        message="That photo is too large. Please upload a photo under 16 MB."
    ), 413


@app.errorhandler(sqlite3.OperationalError)
def database_error(error):
    print(f"Database error: {error}")
    return "The database isn't set up yet. See database/README.md.", 500

if __name__ == "__main__":
    app.run(debug=True)