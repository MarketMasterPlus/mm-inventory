-- mm-inventory/db/mm-inventory.sql

-- Create the marketmaster database
CREATE DATABASE marketmaster;

\connect marketmaster;


CREATE TABLE IF NOT EXISTS productitem (
    id SERIAL PRIMARY KEY,
    productid INTEGER NOT NULL,
    storeid INTEGER NOT NULL, -- soft reference to a store in the mm-store service
    price FLOAT NOT NULL,
    stock INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_productitems_id ON productitem(id);
CREATE INDEX IF NOT EXISTS idx_productitems_storeid ON productitem(storeid);
