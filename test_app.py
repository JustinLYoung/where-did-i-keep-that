import sqlite3
from flask import Flask, request, redirect, url_for, render_template
from database.database import (
    DATABASE_PATH,
    get_all_locations,
    add_storage_location,
    update_storage_location,
    delete_storage_location,
    get_all_items,
    add_item,
    update_item,
    delete_item,
    search_items
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        location_name = request.form["location_name"]
        description = request.form["description"]

        add_storage_location(1, location_name, description)

        return redirect(url_for("home"))

    locations = get_all_locations()

    search_term = request.args.get("search", "").strip()

    if search_term:
        items = search_items(search_term)
    else:
        items = get_all_items()

    return render_template(
        "index.html",
        locations=locations,
        items=items,
        search_term=search_term
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


if __name__ == "__main__":
    app.run(debug=True)
