
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "where_did_i_keep_that.db"


def get_all_items(user_id):
    """Get all items belonging to a specific user"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            items.item_name,
            items.description,
            storage_locations.location_name,
            items.item_id,
            items.photo_path
        FROM items
        LEFT JOIN storage_locations
            ON items.location_id = storage_locations.location_id
        WHERE items.user_id = ?;
    """, (user_id,))

    items = cursor.fetchall()
    connection.close()

    return items


def update_storage_location(user_id, location_id, location_name, description=None):
    """Update name or discription of storage location"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE storage_locations
        SET location_name = ?, description = ?
        WHERE user_id = ? AND location_id = ?;
    """, (location_name, description, user_id, location_id))

    connection.commit()
    connection.close()


def delete_storage_location(user_id, location_id):
    """Delete a certain storage location"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # Check to see if location contains any items.
    cursor.execute("""
        SELECT COUNT(*)
        FROM items
        WHERE user_id = ? AND location_id = ?;
    """, (user_id, location_id))

    item_count = cursor.fetchone()[0]

    # if items exists dont delete location
    if item_count > 0:
        connection.close()
        return False

    # delete location
    cursor.execute("""
        DELETE FROM storage_locations
        WHERE user_id = ? AND location_id = ?;
    """, (user_id, location_id))

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted


def search_items(search_term, location_id=None, user_id=None):
    """Search items belonging to a user by name, description or tag"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    search = '%' + search_term + '%'

    cursor.execute("""
        SELECT DISTINCT items.item_name,
               items.description,
               storage_locations.location_name,
               items.item_id,
               items.photo_path
        FROM items
        LEFT JOIN storage_locations
            ON items.location_id = storage_locations.location_id
        LEFT JOIN item_tags
            ON items.item_id = item_tags.item_id
        LEFT JOIN tags
            ON item_tags.tag_id = tags.tag_id
        WHERE items.user_id = ?
        AND (items.item_name LIKE ?
            OR items.description LIKE ?
            OR tags.tag_name LIKE ?)
        AND (? IS NULL OR items.location_id = ?);
    """, (user_id, search, search, search, location_id, location_id))

    results = cursor.fetchall()
    connection.close()

    return results


def add_item(user_id, item_name, description, location_id=None, photo_path=None):
    """Add an item to the database."""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO items (
            user_id,
            location_id,
            item_name,
            description,
            photo_path
        )
        VALUES (?, ?, ?, ?, ?);
    """, (user_id, location_id, item_name, description, photo_path))

    item_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return item_id


def add_tags(item_id, tags):
    """Add tags to an item"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    for tag in tags:
        cursor.execute("""
            INSERT OR IGNORE INTO tags (tag_name)
            VALUES (?);
        """, (tag,))

        cursor.execute("""
            SELECT tag_id
            FROM tags
            WHERE tag_name = ?;
        """, (tag,))

        tag_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT OR IGNORE INTO item_tags (item_id, tag_id)
            VALUES (?, ?);
        """, (item_id, tag_id))

    connection.commit()
    connection.close()


def update_item(user_id, item_id, item_name, description, location_id=None):
    """Update Item Name, Discription, and Location"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE items
        SET item_name = ?, description = ?, location_id = ?
        WHERE user_id = ? AND item_id = ?;
    """, (item_name, description, location_id, user_id, item_id))

    connection.commit()
    connection.close()


def add_storage_location(user_id, location_name, description=None):
    """Add a storage location to the database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO storage_locations (user_id, location_name, description)
        VALUES (?, ?, ?);
    """, (user_id, location_name, description))

    connection.commit()
    connection.close()


def get_all_locations(user_id):
    """Retrieve locations belonging to a specific user"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT location_id, location_name, description
        FROM storage_locations
        WHERE user_id = ?;
    """, (user_id,))

    locations = cursor.fetchall()
    connection.close()

    return locations


def delete_item(user_id, item_id):
    """Delete an item from a storage location"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM items
        WHERE user_id = ? AND item_id = ?;
    """, (user_id, item_id))

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted


# User Login 

def add_user(username, email, password_hash):
    """Create a new user account."""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # Check if username or email already exists
    cursor.execute("""
        SELECT user_id
        FROM users
        WHERE username = ? OR email = ?;
    """, (username, email))

    existing_user = cursor.fetchone()

    if existing_user:
        connection.close()
        return None

    # Save the new user
    cursor.execute("""
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?);
    """, (username, email, password_hash))

    user_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return user_id


def get_user_by_login(login):
    """Find a user account using their username or email."""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT user_id, username, email, password_hash
        FROM users
        WHERE username = ? OR email = ?;
    """, (login, login))

    user = cursor.fetchone()

    connection.close()

    return user
