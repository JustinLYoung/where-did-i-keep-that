
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "where_did_i_keep_that.db"


def get_all_items():
    """Get all items and storage locations from database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            items.item_name,
            items.description,
            storage_locations.location_name,
            items.item_id
        FROM items
        JOIN storage_locations
            ON items.location_id = storage_locations.location_id;""")

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


def search_items(search_term):
    """Search for a item"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT items.item_name,
               items.description,
               storage_locations.location_name,
               items.item_id
        FROM items
        LEFT JOIN storage_locations
            ON items.location_id = storage_locations.location_id
        WHERE items.item_name LIKE ?;
    """, ('%' + search_term + '%',))

    results = cursor.fetchall()
    connection.close()

    return results


def add_item(user_id, item_name, description, location_id=None):
    """Add items to the database."""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO items (
            user_id,
            location_id,
            item_name,
            description
        )
        VALUES (?, ?, ?, ?);
    """, (user_id, location_id, item_name, description))

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


def get_all_locations():
    """Retrieve all locations in the database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT location_id, location_name, description
        FROM storage_locations;
    """)

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
