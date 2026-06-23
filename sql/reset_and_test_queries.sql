TRUNCATE TABLE ds_raw.customers_raw;
TRUNCATE TABLE ds_raw.products_raw;
TRUNCATE TABLE ds_raw.orders_raw;

TRUNCATE TABLE ds_trans.customers_trans;
TRUNCATE TABLE ds_trans.products_trans;
TRUNCATE TABLE ds_trans.orders_trans;

TRUNCATE TABLE ds_curated.dim_customer;
TRUNCATE TABLE ds_curated.dim_product;
TRUNCATE TABLE ds_curated.fact_sales;

TRUNCATE TABLE ds_admin.transform_audit;
truncate table ds_audit.load_audit;

UPDATE ds_admin.process_control
SET last_processed_timestamp =
TIMESTAMP('1900-01-01 00:00:00 UTC')
WHERE table_name = 'customers';

UPDATE ds_admin.process_control
SET last_processed_timestamp =
TIMESTAMP('1900-01-01 00:00:00 UTC')
WHERE table_name = 'products';

UPDATE ds_admin.process_control
SET last_processed_timestamp =
TIMESTAMP('1900-01-01 00:00:00 UTC')
WHERE table_name = 'orders';


SELECT COUNT(*) FROM ds_raw.customers_raw;
SELECT COUNT(*) FROM ds_raw.products_raw;
SELECT COUNT(*) FROM ds_raw.orders_raw;

SELECT COUNT(*) FROM ds_trans.customers_trans;
SELECT COUNT(*) FROM ds_trans.products_trans;
SELECT COUNT(*) FROM ds_trans.orders_trans;

SELECT COUNT(*) FROM ds_curated.dim_customer;
SELECT COUNT(*) FROM ds_curated.dim_product;
SELECT COUNT(*) FROM ds_curated.fact_sales;

select * from ds_admin.process_control;
select * from ds_admin.transform_audit;
select * from ds_audit.load_audit;