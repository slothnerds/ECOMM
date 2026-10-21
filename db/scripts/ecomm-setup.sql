-- =============================================================================================
-- E-Commerce POC: complete database setup in ONE file
--   1. database "ecomm_db"                          - only if it doesn't exist
--   2. schema "ecomm" + search_path                 - IF NOT EXISTS
--   3. all 14 tables, constraints and indexes       - IF NOT EXISTS, so re-running is safe
--   4. a summary of what exists
--
-- Everything uses the postgres superuser (no separate application login), password "password".
-- Run from the repo root (psql asks for the password, or set $env:PGPASSWORD = 'password'):
--   local Postgres (profile "local"):
--     & "C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -p 5433 -U postgres -f db\scripts\ecomm-setup.sql
--   Docker Postgres (profile "docker"):
--     & "C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -p 5432 -U postgres -f db\scripts\ecomm-setup.sql
--
-- Next: day1-sample-data.sql loads sample data. To start over: 99-drop-schema.sql, then this file again.
--
-- Source: ecommerce_poc_specification.docx, Part 3 (entities, endpoints) and Part 4 (must-have
-- scenarios; rule codes such as [ST-1] refer to it).
--
-- LOCAL DEV credentials only (postgres / password), committed on purpose for this POC.
--
-- Conventions
--   * Surrogate keys: bigint GENERATED ALWAYS AS IDENTITY (PostgreSQL's auto-increment)
--   * Money: numeric(12,2), never float [SN-3, Rule D]
--   * Fixed value sets (status, role, reason): varchar + CHECK, not PostgreSQL ENUM types;
--     adding a value later is a one-line constraint change, and both ORMs map it as a string
--   * Timestamps: timestamptz (stored in UTC)
--   * Every foreign key gets an index: PostgreSQL does not create them automatically
--   * Optimistic locking: a "version" column where concurrent updates are expected
-- =============================================================================================

\set ON_ERROR_STOP on

-- ---------------------------------------------------------------------------------------------
-- 1. Database. CREATE DATABASE has no IF NOT EXISTS and can't run inside a function, so
-- psql's \gexec runs the generated statement only when the SELECT returns a row.
-- ---------------------------------------------------------------------------------------------

SELECT 'CREATE DATABASE ecomm_db'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'ecomm_db') \gexec

-- ---------------------------------------------------------------------------------------------
-- 2. Schema (everything below runs inside ecomm_db)
-- ---------------------------------------------------------------------------------------------

\connect ecomm_db

CREATE SCHEMA IF NOT EXISTS ecomm;
COMMENT ON SCHEMA ecomm IS 'E-Commerce POC: catalog, inventory, carts, orders and payments';

-- Unqualified names (e.g. "products") resolve to ecomm.products for postgres in this database,
-- so the apps can use plain table names. Applies to NEW connections.
ALTER ROLE postgres IN DATABASE ecomm_db SET search_path = ecomm, public;

-- ---------------------------------------------------------------------------------------------
-- 3. Tables, in one transaction (all or nothing)
-- ---------------------------------------------------------------------------------------------

BEGIN;

SET LOCAL search_path = ecomm;

-- =============================================================================================
-- Auth: users and their addresses
-- =============================================================================================

CREATE TABLE IF NOT EXISTS users (
    id             bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email          varchar(254) NOT NULL,
    password_hash  varchar(255) NOT NULL,
    full_name      varchar(200) NOT NULL,
    role           varchar(20)  NOT NULL DEFAULT 'CUSTOMER',
    enabled        boolean      NOT NULL DEFAULT true,
    created_at     timestamptz  NOT NULL DEFAULT now(),
    updated_at     timestamptz  NOT NULL DEFAULT now(),
    CONSTRAINT users_role_chk CHECK (role IN ('CUSTOMER', 'ADMIN')),
    -- Emails are stored lower-case, so a plain unique constraint is case-insensitive in practice
    CONSTRAINT users_email_lower_chk CHECK (email = lower(email)),
    CONSTRAINT users_email_uq UNIQUE (email)
);
COMMENT ON TABLE users IS 'Accounts. Public registration always creates CUSTOMER [OW-4]';
COMMENT ON COLUMN users.password_hash IS 'BCrypt/Argon2 hash; plain passwords are never stored';

CREATE TABLE IF NOT EXISTS addresses (
    id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id         bigint       NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    recipient_name  varchar(200) NOT NULL,
    line1           varchar(200) NOT NULL,
    line2           varchar(200),
    city            varchar(100) NOT NULL,
    region          varchar(100) NOT NULL,
    postal_code     varchar(20)  NOT NULL,
    country         char(2)      NOT NULL,
    phone           varchar(30)  NOT NULL,
    is_default      boolean      NOT NULL DEFAULT false,
    created_at      timestamptz  NOT NULL DEFAULT now(),
    CONSTRAINT addresses_country_chk CHECK (country ~ '^[A-Z]{2}$')
);
COMMENT ON TABLE addresses IS 'Customer address book [AD-1..AD-4]';
CREATE INDEX IF NOT EXISTS addresses_user_idx ON addresses (user_id);
-- At most one default address per user [AD-2]
CREATE UNIQUE INDEX IF NOT EXISTS addresses_one_default_per_user_uq ON addresses (user_id) WHERE is_default;

-- =============================================================================================
-- Catalog: categories and products
-- =============================================================================================

CREATE TABLE IF NOT EXISTS categories (
    id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        varchar(100) NOT NULL,
    parent_id   bigint REFERENCES categories (id) ON DELETE RESTRICT,
    created_at  timestamptz  NOT NULL DEFAULT now(),
    CONSTRAINT categories_name_uq UNIQUE (name),
    CONSTRAINT categories_not_own_parent_chk CHECK (parent_id IS NULL OR parent_id <> id)
);
COMMENT ON TABLE categories IS 'Product categories; parent_id allows nesting';
CREATE INDEX IF NOT EXISTS categories_parent_idx ON categories (parent_id);

CREATE TABLE IF NOT EXISTS products (
    id           bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sku          varchar(32)   NOT NULL,
    name         varchar(200)  NOT NULL,
    description  text          NOT NULL DEFAULT '',
    price        numeric(12,2) NOT NULL,
    status       varchar(20)   NOT NULL DEFAULT 'ACTIVE',
    category_id  bigint REFERENCES categories (id) ON DELETE SET NULL,
    created_at   timestamptz   NOT NULL DEFAULT now(),
    updated_at   timestamptz   NOT NULL DEFAULT now(),
    version      bigint        NOT NULL DEFAULT 0,
    CONSTRAINT products_sku_uq UNIQUE (sku),
    CONSTRAINT products_price_positive_chk CHECK (price > 0),
    CONSTRAINT products_status_chk CHECK (status IN ('DRAFT', 'ACTIVE', 'DISCONTINUED'))
);
COMMENT ON TABLE products IS 'Catalog. Never hard-deleted once ordered: set status DISCONTINUED [SN-4]';
COMMENT ON COLUMN products.sku IS 'Stock keeping unit; unique and fixed after creation';
CREATE INDEX IF NOT EXISTS products_category_idx ON products (category_id);
CREATE INDEX IF NOT EXISTS products_status_idx ON products (status);

-- =============================================================================================
-- Inventory: stock per SKU and its audit log
-- =============================================================================================

CREATE TABLE IF NOT EXISTS inventory (
    sku         varchar(32) PRIMARY KEY REFERENCES products (sku) ON DELETE RESTRICT,
    on_hand     integer     NOT NULL DEFAULT 0,
    reserved    integer     NOT NULL DEFAULT 0,
    version     bigint      NOT NULL DEFAULT 0,
    updated_at  timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT inventory_on_hand_chk  CHECK (on_hand  >= 0),
    CONSTRAINT inventory_reserved_chk CHECK (reserved >= 0),
    -- Available stock = on_hand - reserved, never negative [ST-4]
    CONSTRAINT inventory_reserved_le_on_hand_chk CHECK (reserved <= on_hand)
);
COMMENT ON TABLE inventory IS 'Stock per SKU: on_hand (in warehouse), reserved (held for unpaid orders)';
COMMENT ON COLUMN inventory.version IS 'Incremented by every reservation and adjustment (optimistic locking)';

CREATE TABLE IF NOT EXISTS stock_adjustments (
    id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sku         varchar(32) NOT NULL REFERENCES inventory (sku) ON DELETE RESTRICT,
    change      integer     NOT NULL,
    reason      varchar(20) NOT NULL,
    admin_id    bigint      NOT NULL REFERENCES users (id) ON DELETE RESTRICT,
    created_at  timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT stock_adjustments_change_chk CHECK (change <> 0),
    CONSTRAINT stock_adjustments_reason_chk CHECK (reason IN ('RESTOCK', 'DAMAGE', 'CORRECTION'))
);
COMMENT ON TABLE stock_adjustments IS 'Audit log of admin stock changes [ST-3]';
CREATE INDEX IF NOT EXISTS stock_adjustments_sku_idx ON stock_adjustments (sku);
CREATE INDEX IF NOT EXISTS stock_adjustments_admin_idx ON stock_adjustments (admin_id);

-- =============================================================================================
-- Cart: one per customer
-- =============================================================================================

CREATE TABLE IF NOT EXISTS carts (
    id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id     bigint      NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    created_at  timestamptz NOT NULL DEFAULT now(),
    updated_at  timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT carts_one_per_user_uq UNIQUE (user_id)
);
COMMENT ON TABLE carts IS 'One cart per customer; totals are computed, never stored';

CREATE TABLE IF NOT EXISTS cart_items (
    id                bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cart_id           bigint        NOT NULL REFERENCES carts (id) ON DELETE CASCADE,
    product_id        bigint        NOT NULL REFERENCES products (id) ON DELETE RESTRICT,
    quantity          integer       NOT NULL,
    price_when_added  numeric(12,2) NOT NULL,
    added_at          timestamptz   NOT NULL DEFAULT now(),
    CONSTRAINT cart_items_quantity_chk CHECK (quantity BETWEEN 1 AND 10),
    CONSTRAINT cart_items_price_chk CHECK (price_when_added > 0),
    -- Adding the same product again increases the quantity instead of a new line
    CONSTRAINT cart_items_product_once_uq UNIQUE (cart_id, product_id)
);
COMMENT ON COLUMN cart_items.price_when_added IS 'Used to flag price changes before checkout [SN-5]';
CREATE INDEX IF NOT EXISTS cart_items_product_idx ON cart_items (product_id);

-- =============================================================================================
-- Orders: header with snapshots, lines, status history
-- =============================================================================================

CREATE TABLE IF NOT EXISTS orders (
    id                   bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id              bigint        NOT NULL REFERENCES users (id) ON DELETE RESTRICT,
    status               varchar(20)   NOT NULL DEFAULT 'PENDING_PAYMENT',
    -- Shipping address COPIED at checkout; later address-book edits don't change the order [SN-2]
    ship_recipient_name  varchar(200)  NOT NULL,
    ship_line1           varchar(200)  NOT NULL,
    ship_line2           varchar(200),
    ship_city            varchar(100)  NOT NULL,
    ship_region          varchar(100)  NOT NULL,
    ship_postal_code     varchar(20)   NOT NULL,
    ship_country         char(2)       NOT NULL,
    ship_phone           varchar(30)   NOT NULL,
    subtotal             numeric(12,2) NOT NULL,
    grand_total          numeric(12,2) NOT NULL,
    tracking_number      varchar(100),
    idempotency_key      varchar(100)  NOT NULL,
    created_at           timestamptz   NOT NULL DEFAULT now(),
    updated_at           timestamptz   NOT NULL DEFAULT now(),
    version              bigint        NOT NULL DEFAULT 0,
    CONSTRAINT orders_status_chk CHECK (status IN (
        'PENDING_PAYMENT', 'CONFIRMED', 'PACKED', 'SHIPPED', 'DELIVERED',
        'PAYMENT_FAILED', 'CANCELLED')),
    CONSTRAINT orders_totals_chk CHECK (subtotal >= 0 AND grand_total >= 0),
    -- SHIPPED requires a tracking number [SM-3]; it stays set once delivered
    CONSTRAINT orders_tracking_when_shipped_chk CHECK (
        status NOT IN ('SHIPPED', 'DELIVERED') OR tracking_number IS NOT NULL),
    -- One order per idempotency key and caller [ID-2]
    CONSTRAINT orders_idempotency_uq UNIQUE (user_id, idempotency_key)
);
COMMENT ON TABLE orders IS 'Order header; allowed status changes are enforced by the apps (state machine)';
CREATE INDEX IF NOT EXISTS orders_user_created_idx ON orders (user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS orders_status_idx ON orders (status);

CREATE TABLE IF NOT EXISTS order_lines (
    id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id      bigint        NOT NULL REFERENCES orders (id) ON DELETE CASCADE,
    product_id    bigint        NOT NULL REFERENCES products (id) ON DELETE RESTRICT,
    -- Product data COPIED at checkout [SN-1]
    sku           varchar(32)   NOT NULL,
    product_name  varchar(200)  NOT NULL,
    unit_price    numeric(12,2) NOT NULL,
    quantity      integer       NOT NULL,
    line_total    numeric(12,2) NOT NULL,
    CONSTRAINT order_lines_quantity_chk CHECK (quantity > 0),
    CONSTRAINT order_lines_unit_price_chk CHECK (unit_price > 0),
    -- unit_price has 2 decimals and quantity is whole, so the product is exact
    CONSTRAINT order_lines_total_chk CHECK (line_total = unit_price * quantity)
);
COMMENT ON TABLE order_lines IS 'Price snapshot per item; never changes after checkout';
CREATE INDEX IF NOT EXISTS order_lines_order_idx ON order_lines (order_id);
CREATE INDEX IF NOT EXISTS order_lines_product_idx ON order_lines (product_id);

CREATE TABLE IF NOT EXISTS order_status_history (
    id           bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id     bigint      NOT NULL REFERENCES orders (id) ON DELETE CASCADE,
    from_status  varchar(20),
    to_status    varchar(20) NOT NULL,
    -- NULL when the system made the change (e.g. the hold-expiry job)
    changed_by   bigint REFERENCES users (id) ON DELETE SET NULL,
    reason       varchar(500),
    changed_at   timestamptz NOT NULL DEFAULT now()
);
COMMENT ON TABLE order_status_history IS 'Audit trail of every status change [SM-2]; from_status is NULL for the first entry';
CREATE INDEX IF NOT EXISTS order_status_history_order_idx ON order_status_history (order_id, changed_at);
CREATE INDEX IF NOT EXISTS order_status_history_changed_by_idx ON order_status_history (changed_by);

-- =============================================================================================
-- Checkout support: stock holds, payments, idempotency
-- =============================================================================================

CREATE TABLE IF NOT EXISTS stock_holds (
    id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id    bigint      NOT NULL REFERENCES orders (id) ON DELETE CASCADE,
    sku         varchar(32) NOT NULL REFERENCES inventory (sku) ON DELETE RESTRICT,
    quantity    integer     NOT NULL,
    expires_at  timestamptz NOT NULL,
    created_at  timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT stock_holds_quantity_chk CHECK (quantity > 0),
    CONSTRAINT stock_holds_one_per_order_sku_uq UNIQUE (order_id, sku)
);
COMMENT ON TABLE stock_holds IS 'Temporary reservation per order line; released on payment failure or expiry';
CREATE INDEX IF NOT EXISTS stock_holds_sku_idx ON stock_holds (sku);
-- The expiry job looks up holds by expiry time
CREATE INDEX IF NOT EXISTS stock_holds_expires_idx ON stock_holds (expires_at);

CREATE TABLE IF NOT EXISTS payments (
    id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id      bigint        NOT NULL REFERENCES orders (id) ON DELETE RESTRICT,
    kind          varchar(10)   NOT NULL DEFAULT 'CHARGE',
    amount        numeric(12,2) NOT NULL,
    status        varchar(20)   NOT NULL,
    provider_ref  varchar(100),
    created_at    timestamptz   NOT NULL DEFAULT now(),
    CONSTRAINT payments_kind_chk CHECK (kind IN ('CHARGE', 'REFUND')),
    CONSTRAINT payments_amount_chk CHECK (amount > 0),
    CONSTRAINT payments_status_chk CHECK (status IN ('PENDING', 'SUCCEEDED', 'DECLINED', 'TIMEOUT'))
);
COMMENT ON TABLE payments IS 'Every charge attempt and refund [PM-2]. Card numbers are never stored';
CREATE INDEX IF NOT EXISTS payments_order_idx ON payments (order_id);

CREATE TABLE IF NOT EXISTS idempotency_records (
    id               bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id          bigint       NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    idempotency_key  varchar(100) NOT NULL,
    request_hash     char(64)     NOT NULL,
    order_id         bigint REFERENCES orders (id) ON DELETE SET NULL,
    response_status  integer      NOT NULL,
    response_body    jsonb        NOT NULL,
    created_at       timestamptz  NOT NULL DEFAULT now(),
    expires_at       timestamptz  NOT NULL,
    -- A second request with the same key collides here, so only one checkout succeeds [ID-1..ID-4]
    CONSTRAINT idempotency_records_key_uq UNIQUE (user_id, idempotency_key),
    CONSTRAINT idempotency_records_hash_chk CHECK (request_hash ~ '^[0-9a-f]{64}$')
);
COMMENT ON TABLE idempotency_records IS 'Stored checkout responses for 24 h; request_hash is SHA-256 of the body';
CREATE INDEX IF NOT EXISTS idempotency_records_order_idx ON idempotency_records (order_id);
CREATE INDEX IF NOT EXISTS idempotency_records_expires_idx ON idempotency_records (expires_at);

COMMIT;

-- ---------------------------------------------------------------------------------------------
-- 4. Summary
-- ---------------------------------------------------------------------------------------------

\echo ''
\echo 'Setup complete. Tables in schema ecomm:'
SELECT tablename AS "table", tableowner AS owner
FROM pg_tables WHERE schemaname = 'ecomm' ORDER BY tablename;
