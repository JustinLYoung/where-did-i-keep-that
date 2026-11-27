# Database Setup and Testing

## Requirements
- Python 3
- SQLite
- DB Browser for SQLite (recommended for creating and inspecting the database)

## Setup Instructions
Create the database once before running the app. Use either option below.

### Option 1: Python (from the main project folder)

```bash
python -c "import sqlite3; c = sqlite3.connect('database/where_did_i_keep_that.db'); c.executescript(open('database/schema.sql').read()); c.close()"
```

### Option 2: DB Browser for SQLite
1. Open the `database` folder.
2. Open DB Browser for SQLite and create a new database named `where_did_i_keep_that.db` in the `database` folder.
3. Open `schema.sql` in the Execute SQL tab.
4. Execute the SQL statements to create the tables.
5. Save the changes.

## Run the Application
From the main project folder, run:

```bash
python app.py
```

Then go to http://127.0.0.1:5000, create an account and log in.

## Run the Tests
From the main project folder, run:

```bash
python -m pytest test_database.py
```

The tests use a temporary database, so they do not change `where_did_i_keep_that.db`.

## Notes
- The database starts empty. Create an account, then add a storage location before adding items.
- Each user only sees their own storage locations and items.
- To start over, delete `where_did_i_keep_that.db` and run the setup again.