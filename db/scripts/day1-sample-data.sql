-- =============================================================================================
-- E-Commerce POC: "Day 1" sample data (DML) for all 14 tables in schema ecomm
--
-- The shop's first day, 2026-10-21 (US Central time). Chosen so every later stage has data to
-- test against: an out-of-stock product, the last unit of another, a draft and a discontinued
-- product, a price change after an item was added to a cart, and one order in each important
-- status with matching payments, stock holds, status history and idempotency records.
--
-- RE-RUNNABLE: it first EMPTIES every table in schema ecomm (TRUNCATE ... RESTART IDENTITY),
-- then inserts the same rows again, so ids are always the same (1, 2, 3 ...).
--
-- Run as postgres against ecomm_db, after ecomm-setup.sql (from the repo root):
--   $env:PGPASSWORD = 'password'
--   & "C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -p 5433 -U postgres -d ecomm_db -f db\scripts\day1-sample-data.sql
--
-- All users have the password  Password123!  (bcrypt hash below). LOCAL DEV data only.
--
-- Day 1 at a glance
--   Users     1 admin, 4 customers (dave has no address: checkout must ask for one [AD-3])
--   Products  12 in 5 categories; OFF-2003 out of stock; KIT-1003 last unit (held by order 3);
--             ACC-3102 DRAFT; BOK-4002 DISCONTINUED (still in carol's cart)
--   Carts     alice 2 items; bob 1 item whose price rose since he added it [SN-5]; carol 1
--   Orders    1 CONFIRMED, 2 SHIPPED, 3 PENDING_PAYMENT (payment timed out, holds active),
--             4 PAYMENT_FAILED (declined), 5 CANCELLED (refunded, stock returned), 6 DELIVERED
-- =============================================================================================

\set ON_ERROR_STOP on

-- Works however psql was started (Docker's init runs scripts connected to database postgres)
\connect ecomm_db

BEGIN;

SET LOCAL search_path = ecomm;
SET LOCAL timezone = 'America/Chicago';

-- Start from empty tables, ids from 1 again
TRUNCATE users, addresses, categories, products, inventory, stock_adjustments, carts, cart_items,
         orders, order_lines, order_status_history, stock_holds, payments, idempotency_records
         RESTART IDENTITY CASCADE;

-- ---------------------------------------------------------------------------------------------
-- Users (password for all: Password123!)
-- ids are given explicitly (OVERRIDING SYSTEM VALUE) so the rows below can reference them;
-- the identity sequences are moved past them at the end.
-- ---------------------------------------------------------------------------------------------
INSERT INTO users (id, email, password_hash, full_name, role, created_at, updated_at)
OVERRIDING SYSTEM VALUE VALUES
  (1, 'admin@example.com', '$2b$10$gfjDgRCT2k0MlGDGfaX8tepTNZqE1H2EfQr.D.IgMI6ALREzJEvju', 'Shop Admin',    'ADMIN',    '2026-10-21 07:00', '2026-10-21 07:00'),
  (2, 'alice@example.com', '$2b$10$gfjDgRCT2k0MlGDGfaX8tepTNZqE1H2EfQr.D.IgMI6ALREzJEvju', 'Alice Johnson', 'CUSTOMER', '2026-10-21 08:05', '2026-10-21 08:05'),
  (3, 'bob@example.com',   '$2b$10$gfjDgRCT2k0MlGDGfaX8tepTNZqE1H2EfQr.D.IgMI6ALREzJEvju', 'Bob Martinez',  'CUSTOMER', '2026-10-21 08:40', '2026-10-21 08:40'),
  (4, 'carol@example.com', '$2b$10$gfjDgRCT2k0MlGDGfaX8tepTNZqE1H2EfQr.D.IgMI6ALREzJEvju', 'Carol Nguyen',  'CUSTOMER', '2026-10-21 09:15', '2026-10-21 09:15'),
  (5, 'dave@example.com',  '$2b$10$gfjDgRCT2k0MlGDGfaX8tepTNZqE1H2EfQr.D.IgMI6ALREzJEvju', 'Dave Okafor',   'CUSTOMER', '2026-10-21 16:30', '2026-10-21 16:30');

-- ---------------------------------------------------------------------------------------------
-- Addresses (one default per user [AD-2]; dave has none)
-- ---------------------------------------------------------------------------------------------
INSERT INTO addresses (id, user_id, recipient_name, line1, line2, city, region, postal_code, country, phone, is_default, created_at)
OVERRIDING SYSTEM VALUE VALUES
  (1, 2, 'Alice Johnson', '12 Lakeview Drive', NULL,        'Austin',  'TX', '78701', 'US', '+1-512-555-0101', true,  '2026-10-21 08:07'),
  (2, 2, 'Alice Johnson', '400 Congress Ave',  'Suite 900', 'Austin',  'TX', '78701', 'US', '+1-512-555-0102', false, '2026-10-21 08:09'),
  (3, 3, 'Bob Martinez',  '77 Elm Street',     'Apt 3B',    'Dallas',  'TX', '75201', 'US', '+1-214-555-0103', true,  '2026-10-21 08:42'),
  (4, 4, 'Carol Nguyen',  '5 Harbor Road',     NULL,        'Houston', 'TX', '77002', 'US', '+1-713-555-0104', true,  '2026-10-21 09:16');

-- ---------------------------------------------------------------------------------------------
-- Categories (Accessories is nested under Electronics)
-- ---------------------------------------------------------------------------------------------
INSERT INTO categories (id, name, parent_id, created_at)
OVERRIDING SYSTEM VALUE VALUES
  (1, 'Kitchen',     NULL, '2026-10-21 07:05'),
  (2, 'Home Office', NULL, '2026-10-21 07:05'),
  (3, 'Electronics', NULL, '2026-10-21 07:05'),
  (4, 'Accessories', 3,    '2026-10-21 07:06'),
  (5, 'Books',       NULL, '2026-10-21 07:06');

-- ---------------------------------------------------------------------------------------------
-- Products (prices are today's prices; orders keep their own snapshot)
-- ---------------------------------------------------------------------------------------------
INSERT INTO products (id, sku, name, description, price, status, category_id, created_at, updated_at, version)
OVERRIDING SYSTEM VALUE VALUES
  ( 1, 'KIT-1001', 'Coffee mug',          'Ceramic, 350 ml',                       12.50, 'ACTIVE',       1, '2026-10-21 07:10', '2026-10-21 07:10', 0),
  ( 2, 'KIT-1002', 'French press',        'Glass and steel, 1 l',                  34.99, 'ACTIVE',       1, '2026-10-21 07:10', '2026-10-21 07:10', 0),
  ( 3, 'KIT-1003', 'Chef knife',          '20 cm, stainless steel',                59.00, 'ACTIVE',       1, '2026-10-21 07:11', '2026-10-21 07:11', 0),
  ( 4, 'OFF-2001', 'Notebook A5',         'Dotted, 120 pages',                      6.75, 'ACTIVE',       2, '2026-10-21 07:12', '2026-10-21 07:12', 0),
  ( 5, 'OFF-2002', 'Desk lamp',           'LED, dimmable',                         42.00, 'ACTIVE',       2, '2026-10-21 07:12', '2026-10-21 07:12', 0),
  ( 6, 'OFF-2003', 'Ergonomic chair',     'Mesh back, adjustable arms',           249.00, 'ACTIVE',       2, '2026-10-21 07:13', '2026-10-21 07:13', 0),
  ( 7, 'ELE-3001', 'Wireless mouse',      '2.4 GHz, silent click',                 24.99, 'ACTIVE',       3, '2026-10-21 07:14', '2026-10-21 07:14', 0),
  -- Price raised from 79.90 at 11:00, after bob added it to his cart [SN-5]
  ( 8, 'ELE-3002', 'Mechanical keyboard', 'Tenkeyless, brown switches',            89.90, 'ACTIVE',       3, '2026-10-21 07:14', '2026-10-21 11:00', 1),
  ( 9, 'ACC-3101', 'USB-C cable',         '2 m, braided',                           9.99, 'ACTIVE',       4, '2026-10-21 07:15', '2026-10-21 07:15', 0),
  (10, 'ACC-3102', 'Laptop stand',        'Aluminium (not yet released)',          39.50, 'DRAFT',        4, '2026-10-21 07:15', '2026-10-21 07:15', 0),
  (11, 'BOK-4001', 'Python for Beginners','Paperback, 2026 edition',               29.00, 'ACTIVE',       5, '2026-10-21 07:16', '2026-10-21 07:16', 0),
  (12, 'BOK-4002', 'Java Basics (old ed.)','Paperback, replaced by a new edition', 19.00, 'DISCONTINUED', 5, '2026-10-21 07:16', '2026-10-21 15:00', 1);

-- ---------------------------------------------------------------------------------------------
-- Inventory at the end of day 1
--   on_hand  = restocked + corrections - damage - sold (CONFIRMED and later; the cancelled
--              order's stock was returned)
--   reserved = quantity held for the PENDING_PAYMENT order 3
-- ---------------------------------------------------------------------------------------------
INSERT INTO inventory (sku, on_hand, reserved, version, updated_at) VALUES
  ('KIT-1001',  47, 0, 3, '2026-10-21 13:20'),  -- 50 restocked - 2 (order 1) - 1 (order 6)
  ('KIT-1002',  20, 0, 1, '2026-10-21 07:30'),
  ('KIT-1003',   1, 1, 2, '2026-10-21 17:30'),  -- the LAST unit, held by order 3
  ('OFF-2001', 196, 0, 2, '2026-10-21 10:05'),  -- 200 - 4 (order 1)
  ('OFF-2002',  15, 1, 4, '2026-10-21 17:30'),  -- 15 - 2 (order 5) + 2 (order 5 cancelled); 1 held by order 3
  ('OFF-2003',   0, 0, 0, '2026-10-21 07:30'),  -- out of stock, never delivered
  ('ELE-3001',  39, 0, 2, '2026-10-21 10:40'),  -- 40 - 1 (order 2)
  ('ELE-3002',  25, 0, 2, '2026-10-21 12:00'),  -- 24 + 1 correction; order 4 failed, nothing sold
  ('ACC-3101',  98, 0, 2, '2026-10-21 10:40'),  -- 100 - 2 (order 2)
  ('ACC-3102',  10, 0, 1, '2026-10-21 07:30'),  -- draft product, stocked early
  ('BOK-4001',  29, 0, 2, '2026-10-21 13:20'),  -- 30 - 1 (order 6)
  ('BOK-4002',   3, 0, 2, '2026-10-21 14:00');  -- 5 - 2 damaged

-- ---------------------------------------------------------------------------------------------
-- Stock adjustments (audit log of the admin's changes [ST-3])
-- ---------------------------------------------------------------------------------------------
INSERT INTO stock_adjustments (sku, change, reason, admin_id, created_at) VALUES
  ('KIT-1001',  50, 'RESTOCK',    1, '2026-10-21 07:30'),
  ('KIT-1002',  20, 'RESTOCK',    1, '2026-10-21 07:30'),
  ('KIT-1003',   1, 'RESTOCK',    1, '2026-10-21 07:30'),
  ('OFF-2001', 200, 'RESTOCK',    1, '2026-10-21 07:30'),
  ('OFF-2002',  15, 'RESTOCK',    1, '2026-10-21 07:30'),
  ('ELE-3001',  40, 'RESTOCK',    1, '2026-10-21 07:30'),
  ('ELE-3002',  24, 'RESTOCK',    1, '2026-10-21 07:30'),
  ('ACC-3101', 100, 'RESTOCK',    1, '2026-10-21 07:30'),
  ('ACC-3102',  10, 'RESTOCK',    1, '2026-10-21 07:30'),
  ('BOK-4001',  30, 'RESTOCK',    1, '2026-10-21 07:30'),
  ('BOK-4002',   5, 'RESTOCK',    1, '2026-10-21 07:30'),
  ('ELE-3002',   1, 'CORRECTION', 1, '2026-10-21 12:00'),  -- recount found one more
  ('BOK-4002',  -2, 'DAMAGE',     1, '2026-10-21 14:00');  -- water damage

-- ---------------------------------------------------------------------------------------------
-- Carts (open carts at the end of the day; dave has none yet)
-- ---------------------------------------------------------------------------------------------
INSERT INTO carts (id, user_id, created_at, updated_at)
OVERRIDING SYSTEM VALUE VALUES
  (1, 2, '2026-10-21 15:00', '2026-10-21 15:10'),
  (2, 3, '2026-10-21 09:30', '2026-10-21 09:30'),
  (3, 4, '2026-10-21 14:30', '2026-10-21 14:30');

INSERT INTO cart_items (cart_id, product_id, quantity, price_when_added, added_at) VALUES
  (1,  2, 1, 34.99, '2026-10-21 15:00'),  -- alice: French press
  (1,  9, 3,  9.99, '2026-10-21 15:10'),  -- alice: 3 USB-C cables
  (2,  8, 1, 79.90, '2026-10-21 09:30'),  -- bob: keyboard at the OLD price (now 89.90) [SN-5]
  (3, 12, 1, 19.00, '2026-10-21 14:30');  -- carol: product discontinued at 15:00 after she added it

-- ---------------------------------------------------------------------------------------------
-- Orders (address and totals are snapshots taken at checkout [SN-1, SN-2])
-- ---------------------------------------------------------------------------------------------
INSERT INTO orders (id, user_id, status,
                    ship_recipient_name, ship_line1, ship_line2, ship_city, ship_region, ship_postal_code, ship_country, ship_phone,
                    subtotal, grand_total, tracking_number, idempotency_key, created_at, updated_at, version)
OVERRIDING SYSTEM VALUE VALUES
  (1, 2, 'CONFIRMED',
      'Alice Johnson', '12 Lakeview Drive', NULL, 'Austin', 'TX', '78701', 'US', '+1-512-555-0101',
      52.00, 52.00, NULL, '8c1f2e8a-0001-4d1e-9a01-day1order01', '2026-10-21 10:00', '2026-10-21 10:05', 1),
  (2, 2, 'SHIPPED',
      'Alice Johnson', '400 Congress Ave', 'Suite 900', 'Austin', 'TX', '78701', 'US', '+1-512-555-0102',
      44.97, 44.97, 'TRK-1000001', '8c1f2e8a-0002-4d1e-9a01-day1order02', '2026-10-21 10:30', '2026-10-21 16:00', 3),
  (3, 3, 'PENDING_PAYMENT',
      'Bob Martinez', '77 Elm Street', 'Apt 3B', 'Dallas', 'TX', '75201', 'US', '+1-214-555-0103',
      101.00, 101.00, NULL, '8c1f2e8a-0003-4d1e-9a01-day1order03', '2026-10-21 17:30', '2026-10-21 17:30', 0),
  (4, 3, 'PAYMENT_FAILED',
      'Bob Martinez', '77 Elm Street', 'Apt 3B', 'Dallas', 'TX', '75201', 'US', '+1-214-555-0103',
      89.90, 89.90, NULL, '8c1f2e8a-0004-4d1e-9a01-day1order04', '2026-10-21 11:30', '2026-10-21 11:31', 1),
  (5, 4, 'CANCELLED',
      'Carol Nguyen', '5 Harbor Road', NULL, 'Houston', 'TX', '77002', 'US', '+1-713-555-0104',
      84.00, 84.00, NULL, '8c1f2e8a-0005-4d1e-9a01-day1order05', '2026-10-21 09:20', '2026-10-21 09:50', 2),
  (6, 4, 'DELIVERED',
      'Carol Nguyen', '5 Harbor Road', NULL, 'Houston', 'TX', '77002', 'US', '+1-713-555-0104',
      41.50, 41.50, 'TRK-1000002', '8c1f2e8a-0006-4d1e-9a01-day1order06', '2026-10-21 13:20', '2026-10-21 18:45', 4);

-- line_total = unit_price * quantity (a CHECK constraint enforces it)
INSERT INTO order_lines (order_id, product_id, sku, product_name, unit_price, quantity, line_total) VALUES
  (1,  1, 'KIT-1001', 'Coffee mug',           12.50, 2,  25.00),
  (1,  4, 'OFF-2001', 'Notebook A5',           6.75, 4,  27.00),
  (2,  7, 'ELE-3001', 'Wireless mouse',       24.99, 1,  24.99),
  (2,  9, 'ACC-3101', 'USB-C cable',           9.99, 2,  19.98),
  (3,  3, 'KIT-1003', 'Chef knife',           59.00, 1,  59.00),
  (3,  5, 'OFF-2002', 'Desk lamp',            42.00, 1,  42.00),
  (4,  8, 'ELE-3002', 'Mechanical keyboard',  89.90, 1,  89.90),
  (5,  5, 'OFF-2002', 'Desk lamp',            42.00, 2,  84.00),
  (6, 11, 'BOK-4001', 'Python for Beginners', 29.00, 1,  29.00),
  (6,  1, 'KIT-1001', 'Coffee mug',           12.50, 1,  12.50);

-- Every status change [SM-2]; changed_by NULL = the system (payment result)
INSERT INTO order_status_history (order_id, from_status, to_status, changed_by, reason, changed_at) VALUES
  (1, NULL,              'PENDING_PAYMENT', 2,    'Checkout',                     '2026-10-21 10:00'),
  (1, 'PENDING_PAYMENT', 'CONFIRMED',       NULL, 'Payment succeeded',            '2026-10-21 10:05'),
  (2, NULL,              'PENDING_PAYMENT', 2,    'Checkout',                     '2026-10-21 10:30'),
  (2, 'PENDING_PAYMENT', 'CONFIRMED',       NULL, 'Payment succeeded',            '2026-10-21 10:40'),
  (2, 'CONFIRMED',       'PACKED',          1,    NULL,                           '2026-10-21 14:00'),
  (2, 'PACKED',          'SHIPPED',         1,    'Tracking TRK-1000001',         '2026-10-21 16:00'),
  (3, NULL,              'PENDING_PAYMENT', 3,    'Checkout',                     '2026-10-21 17:30'),
  (4, NULL,              'PENDING_PAYMENT', 3,    'Checkout',                     '2026-10-21 11:30'),
  (4, 'PENDING_PAYMENT', 'PAYMENT_FAILED',  NULL, 'Payment declined',             '2026-10-21 11:31'),
  (5, NULL,              'PENDING_PAYMENT', 4,    'Checkout',                     '2026-10-21 09:20'),
  (5, 'PENDING_PAYMENT', 'CONFIRMED',       NULL, 'Payment succeeded',            '2026-10-21 09:22'),
  (5, 'CONFIRMED',       'CANCELLED',       4,    'Ordered by mistake',           '2026-10-21 09:50'),
  (6, NULL,              'PENDING_PAYMENT', 4,    'Checkout',                     '2026-10-21 13:20'),
  (6, 'PENDING_PAYMENT', 'CONFIRMED',       NULL, 'Payment succeeded',            '2026-10-21 13:21'),
  (6, 'CONFIRMED',       'PACKED',          1,    NULL,                           '2026-10-21 15:30'),
  (6, 'PACKED',          'SHIPPED',         1,    'Tracking TRK-1000002',         '2026-10-21 16:10'),
  (6, 'SHIPPED',         'DELIVERED',       1,    'Same-day courier',             '2026-10-21 18:45');

-- Holds exist only while an order waits for payment. Order 3's expired at 17:45, so the
-- hold-expiry job (Stage 14) should release them and fail the order when it first runs.
INSERT INTO stock_holds (order_id, sku, quantity, expires_at, created_at) VALUES
  (3, 'KIT-1003', 1, '2026-10-21 17:45', '2026-10-21 17:30'),
  (3, 'OFF-2002', 1, '2026-10-21 17:45', '2026-10-21 17:30');

-- Every payment attempt and refund [PM-2]; no card numbers are ever stored
INSERT INTO payments (order_id, kind, amount, status, provider_ref, created_at) VALUES
  (1, 'CHARGE', 52.00,  'SUCCEEDED', 'mock-ch-0001', '2026-10-21 10:05'),
  (2, 'CHARGE', 44.97,  'SUCCEEDED', 'mock-ch-0002', '2026-10-21 10:40'),
  (3, 'CHARGE', 101.00, 'TIMEOUT',   'mock-ch-0003', '2026-10-21 17:31'),  -- result unknown [PM-4]
  (4, 'CHARGE', 89.90,  'DECLINED',  'mock-ch-0004', '2026-10-21 11:31'),
  (5, 'CHARGE', 84.00,  'SUCCEEDED', 'mock-ch-0005', '2026-10-21 09:22'),
  (5, 'REFUND', 84.00,  'SUCCEEDED', 'mock-rf-0001', '2026-10-21 09:50'),  -- cancelled after payment
  (6, 'CHARGE', 41.50,  'SUCCEEDED', 'mock-ch-0006', '2026-10-21 13:21');

-- The stored response of each checkout, kept for 24 h so a retry gets the same order [ID-2]
INSERT INTO idempotency_records (user_id, idempotency_key, request_hash, order_id, response_status, response_body, created_at, expires_at)
SELECT o.user_id,
       o.idempotency_key,
       encode(sha256(convert_to('checkout:' || o.idempotency_key, 'UTF8')), 'hex'),
       o.id,
       201,
       jsonb_build_object('id', o.id, 'status', 'PENDING_PAYMENT', 'grandTotal', o.grand_total),
       o.created_at,
       o.created_at + interval '24 hours'
FROM orders o
ORDER BY o.id;

-- ---------------------------------------------------------------------------------------------
-- Move every identity sequence past the explicit ids, so the apps' next insert gets id max+1
-- (inventory has no id column: its key is the sku)
-- ---------------------------------------------------------------------------------------------
DO $$
DECLARE
  t text;
BEGIN
  FOREACH t IN ARRAY ARRAY['users', 'addresses', 'categories', 'products', 'stock_adjustments',
                           'carts', 'cart_items', 'orders', 'order_lines', 'order_status_history',
                           'stock_holds', 'payments', 'idempotency_records']
  LOOP
    EXECUTE format('SELECT setval(pg_get_serial_sequence(%L, ''id''), coalesce((SELECT max(id) FROM ecomm.%I), 0) + 1, false)',
                   'ecomm.' || t, t);
  END LOOP;
END $$;

COMMIT;

-- ---------------------------------------------------------------------------------------------
-- Summary
-- ---------------------------------------------------------------------------------------------
\echo ''
\echo 'Day 1 sample data loaded. Rows per table:'
SELECT 'users' AS "table", count(*) AS rows FROM ecomm.users
UNION ALL SELECT 'addresses',            count(*) FROM ecomm.addresses
UNION ALL SELECT 'categories',           count(*) FROM ecomm.categories
UNION ALL SELECT 'products',             count(*) FROM ecomm.products
UNION ALL SELECT 'inventory',            count(*) FROM ecomm.inventory
UNION ALL SELECT 'stock_adjustments',    count(*) FROM ecomm.stock_adjustments
UNION ALL SELECT 'carts',                count(*) FROM ecomm.carts
UNION ALL SELECT 'cart_items',           count(*) FROM ecomm.cart_items
UNION ALL SELECT 'orders',               count(*) FROM ecomm.orders
UNION ALL SELECT 'order_lines',          count(*) FROM ecomm.order_lines
UNION ALL SELECT 'order_status_history', count(*) FROM ecomm.order_status_history
UNION ALL SELECT 'stock_holds',          count(*) FROM ecomm.stock_holds
UNION ALL SELECT 'payments',             count(*) FROM ecomm.payments
UNION ALL SELECT 'idempotency_records',  count(*) FROM ecomm.idempotency_records;
