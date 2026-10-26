CREATE TABLE "users" (
	"user_id"	INTEGER,
	"username"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"password_hash"	TEXT UNIQUE,
	PRIMARY KEY("user_id" AUTOINCREMENT)
);

CREATE TABLE "storage_locations" (
	"location_id"	INTEGER,
	"user_id"	INTEGER NOT NULL,
	"location_name"	TEXT NOT NULL,
	"description"	TEXT,
	PRIMARY KEY("location_id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "users"("user_id")
);

CREATE TABLE "items" (
	"item_id"	INTEGER,
	"user_id"	INTEGER NOT NULL,
	"location_id"	INTEGER,
	"item_name"	TEXT NOT NULL,
	"description"	TEXT,
	"photo_path"	TEXT,
	PRIMARY KEY("item_id" AUTOINCREMENT),
	FOREIGN KEY("location_id") REFERENCES "storage_locations"("location_id"),
	FOREIGN KEY("user_id") REFERENCES "users"("user_id")
);

CREATE TABLE "tags" (
	"tag_id"	INTEGER,
	"tag_name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("tag_id" AUTOINCREMENT)
);

CREATE TABLE "item_tags" (
	"item_id"	INTEGER NOT NULL,
	"tag_id"	INTEGER NOT NULL,
	PRIMARY KEY("item_id","tag_id"),
	FOREIGN KEY("item_id") REFERENCES "items"("item_id"),
	FOREIGN KEY("tag_id") REFERENCES "tags"("tag_id")
);