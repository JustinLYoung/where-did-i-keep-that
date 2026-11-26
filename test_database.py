
import sqlite3
import pytest

import database.database as db


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    """Create a temporary database for testing."""

    database_path = tmp_path / "test_database.db"

    monkeypatch.setattr(db, "DATABASE_PATH", str(database_path))

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE storage_locations (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            location_name TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            location_id INTEGER,
            item_name TEXT NOT NULL,
            description TEXT,
            photo_path TEXT
        );
    """)

    connection.commit()
    connection.close()

    return str(database_path)


def test_add_item_wrong_user_location(test_db):
    """Test to make sure a user is not able to add an item to another
    users location"""

    # Create a storage location belonging to User 2
    connection = sqlite3.connect(test_db)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO storage_locations (user_id, location_name)
        VALUES (?, ?);
    """, (2, "User 2's Middle Desk Drawer"))

    other_users_location = cursor.lastrowid

    connection.commit()
    connection.close()

    # User 1 attempts to add an item to User 2's location
    result = db.add_item(
        1,
        "Flashlight",
        "Battery",
        other_users_location
    )

    # The database function should reject the request
    assert result is None



def test_update_item_wrong_user_location(test_db):
    """Test to make sure user can not move an item into another
    user's location"""

    connection = sqlite3.connect(test_db)
    cursor = connection.cursor()

    # Create User 1's storage location
    cursor.execute("""
        INSERT INTO storage_locations (user_id, location_name)
        VALUES (?, ?);
    """, (1, "User 1 top filing cabinet"))

    user_location = cursor.lastrowid

    # Create User 2's storage location
    cursor.execute("""
        INSERT INTO storage_locations (user_id, location_name)
        VALUES (?, ?);
    """, (2, "User 2 Blue Box"))

    other_users_location = cursor.lastrowid

    # Create an item belonging to User 1
    cursor.execute("""
        INSERT INTO items (
            user_id, location_id, item_name, description
        )
        VALUES (?, ?, ?, ?);
    """, (1, user_location, "lighter", "usb thumbdrive"))

    item = cursor.lastrowid

    connection.commit()
    connection.close()

    # User 1 attempts to move their item into User 2's location
    result = db.update_item(
        1,
        item,
        "lighter",
        "usb thumbdrive",
        other_users_location
    )

    assert result is False

def test_add_item_to_correct_user_location(test_db):
    """Test to verify that a user can add an item to their location"""

    connection = sqlite3.connect(test_db)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO storage_locations (user_id, location_name)
        VALUES (?, ?);
    """, (1, "User 1 shoe bin"))

    location_id = cursor.lastrowid

    connection.commit()
    connection.close()

    result = db.add_item(
        1,
        "Jordan 1s",
        "Slippers",
        location_id
    )

    assert result is not None


def test_update_item_to_correct_user_location(test_db):
    """Test that a user is able to move an item to their storage location."""

    connection = sqlite3.connect(test_db)
    cursor = connection.cursor()

    # Create two locations belonging to User 1
    cursor.execute("""
        INSERT INTO storage_locations (user_id, location_name)
        VALUES (?, ?);
    """, (1, "Dresser Top Drawer"))

    first_location = cursor.lastrowid

    cursor.execute("""
        INSERT INTO storage_locations (user_id, location_name)
        VALUES (?, ?);
    """, (1, "Winter Clothes Box"))

    second_location = cursor.lastrowid

    # Create an item in the first location
    cursor.execute("""
        INSERT INTO items (
            user_id, location_id, item_name, description
        )
        VALUES (?, ?, ?, ?);
    """, (1, first_location, "Scarf", "Long Johns"))

    item_id = cursor.lastrowid

    connection.commit()
    connection.close()

    # Move item from one location to the next location.
    result = db.update_item(
        1,
        item_id,
        "Scarf",
        "Long Johns",
        second_location
    )

    assert result is True