
import sqlite3


def get_all_items():
    """Get all items and storage locations from database"""
    connection = sqlite3.connect("where_did_i_keep_that.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            items.item_name,
            items.description,
            storage_locations.location_name
        FROM items
        JOIN storage_locations
            ON items.location_id = storage_locations.location_id;""")

    items = cursor.fetchall()
    connection.close()

    return items

def search_items(search_term):
    """Search function for items in database.  Search by item"""
    connection = sqlite3.connect("where_did_i_keep_that.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            items.item_name,
            items.description,
            storage_locations.location_name
        FROM items
        LEFT JOIN storage_locations
            ON items.location_id = storage_locations.location_id
        WHERE items.item_name LIKE ?;""", (f"%{search_term}%",))

    items = cursor.fetchall()
    connection.close()

    return items

def add_item(user_id, item_name, description, location_id=None):
    """Add items to the database."""
    connection = sqlite3.connect("where_did_i_keep_that.db")
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

def add_storage_location(user_id, location_name, description=None):
    """Add a storage location to the database"""
    connection = sqlite3.connect("where_did_i_keep_that.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO storage_locations (user_id, location_name, description)
        VALUES (?, ?, ?);
    """, (user_id, location_name, description))

    connection.commit()
    connection.close()

def get_all_locations():
    """Retrieve all locations in the database"""
    connection = sqlite3.connect("where_did_i_keep_that.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT location_id, location_name
        FROM storage_locations;
    """)

    locations = cursor.fetchall()
    connection.close()

    return locations


def main():
    """Test functions of the app through user's selections"""
    while True:
        print("\n=== Where Did I Keep That? ===")
        print("1. View all items")
        print("2. Search items")
        print("3. Add an item")
        print("4. Add a storage location")
        print("5. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            items = get_all_items()

            for item in items:
                print(
                    f"{item[0]} | {item[1]} | Stored in: {item[2]}"
                )

        elif choice == "2":
            search_term = input("Enter item name or tag: ")
            items = search_items(search_term)

            if items:
                for item in items:
                    print(
                        f"{item[0]} | {item[1]} | Stored in: {item[2]}"
                    )
            else:
                print("No matching items found.")

        elif choice == "3":
            item_name = input("Enter item name: ")
            description = input("Enter description: ")

            locations = get_all_locations()

            print("\nAvailable storage locations:")

            for location in locations:
                print(f"{location[0]}. {location[1]}")

            location_id = int(input("Choose a location ID: "))

            add_item(1, item_name, description, location_id)

            print("Item added successfully!")

        elif choice == "4":
            location_name = input("Enter the storage location name: ")
            description = input("Enter a description (optional): ")

            add_storage_location(1, location_name, description)

            print("Storage location added successfully!")

        elif choice == "5":
            print("Thank you, goodbye!")
            break

        else:
            print("Invalid choice. Please choose 1-5.")

if __name__ == "__main__":
    main()