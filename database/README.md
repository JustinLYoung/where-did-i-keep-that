# Database Setup and Testing

## Requirements
- Python 3
- SQLite
- DB Browser for SQLite (recommended for creating and inspecting the database)

## Setup Instructions
1. Open the `database` folder.
2. Open DB Browser for SQLite and create a new database named `where_did_i_keep_that.db` in the `database` folder.
3. Open `schema.sql` in the Execute SQL tab.
4. Execute the SQL statements to create the tables.
5. Save the changes.

## Run the Application
Open a terminal and navigate to the `database` folder. Run:

```bash
python database.py
```

## Available Features
- View all items
- Search items by name, description, or tag
- Add an item and choose its storage location
- Add a new storage location

## Notes
The database starts empty. Add a storage location before adding items. The current prototype uses a fixed user ID for adding items.
