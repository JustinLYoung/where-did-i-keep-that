# Storage Location and QR Code Workflow

The goal is to allow users to create storage locations, generate QR codes for them, and scan those codes to see what items are stored there. This document outlines how we plan to connect our existing database and QR code functionality.

## Creating a Storage Location

1. A user creates a storage location, such as a room, shelf, or box.
2. The application saves the location name, description, and user ID in our SQLite database.
3. SQLite assigns the location a unique `location_id`.
4. The application uses that ID to create a URL for the storage location.

For example, if a location has an ID of `12`, the URL could look like this:

`https://our-app.example/locations/12`

This is just an example. We'll need to agree on the actual URL structure and domain when we start integrating everything.

## Generating the QR Code

1. After the location is saved, the application retrieves its `location_id`.
2. That ID is used to build the location's URL.
3. The URL is passed to our existing QR code generator, which uses Python's `qrcode` library.
4. The generator creates a PNG image that the user can download and print.
5. The QR label can then be placed on the corresponding box, shelf, or storage location.

## Scanning the QR Code

1. A user scans the QR code with their phone.
2. The code opens the URL associated with that storage location.
3. If the user isn't signed in, they'll need to log in first.
4. The application checks whether the user has permission to access that location.
5. If authorized, the application retrieves and displays the items stored there.

One thing we'll need to be careful about is security. Just because someone scans a QR code doesn't mean they should automatically have access to another user's inventory.

## Database Integration

Justin's existing SQLite database already includes the `storage_locations` and `items` tables.

The `storage_locations` table contains:

- `location_id`
- `user_id`
- `location_name`
- `description`

The `items` table also contains a `location_id`, which connects an item to its storage location.

Right now, `add_storage_location()` creates a location but doesn't return its newly assigned ID. We'll need to update that functionality so the application knows which location to generate a QR code for.

We'll also need a way to retrieve items belonging to a specific location. Those database queries should check the user's access permissions rather than returning another user's inventory.

## Remaining Work

Before this feature is fully functional, we'll need to:

- Confirm the final URL structure with the team.
- Update the database functionality to return the new location ID.
- Connect our QR code generator to locations stored in SQLite.
- Create a Flask route for opening individual storage locations.
- Add authentication and ownership checks.
- Test that scanning a QR code opens the correct location and displays its items.
- Test invalid location IDs and unauthorized access.

