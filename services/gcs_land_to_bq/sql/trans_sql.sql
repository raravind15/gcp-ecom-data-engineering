CREATE TABLE ds_admin.process_control
(
    table_name STRING,

    last_processed_timestamp TIMESTAMP,

    status STRING,

    updated_at TIMESTAMP
);


INSERT INTO ds_admin.process_control
VALUES
(
    'customers',
    TIMESTAMP('1900-01-01 00:00:00 UTC'),
    'SUCCESS',
    CURRENT_TIMESTAMP()
);

CREATE OR REPLACE PROCEDURE ds_trans.sp_transform_customers()
BEGIN

DECLARE v_start_time TIMESTAMP;
DECLARE v_end_time TIMESTAMP;
DECLARE v_source_count INT64;
DECLARE v_target_count INT64;

SET v_start_time = CURRENT_TIMESTAMP();

-- Count incremental rows
SET v_source_count =
(
SELECT COUNT(*)
FROM ds_raw.customers_raw
WHERE load_timestamp >
(
SELECT last_processed_timestamp
FROM ds_admin.process_control
WHERE table_name = 'customers'
)
);

-- No new data
IF v_source_count = 0 THEN

INSERT INTO ds_admin.transform_audit
(
  run_id,
  source_table,
  target_table,
  start_time,
  end_time,
  source_row_count,
  target_row_count,
  status,
  error_message
)
VALUES
(
  GENERATE_UUID(),
  'customers_raw',
  'customers_trans',
  v_start_time,
  CURRENT_TIMESTAMP(),
  0,
  0,
  'SUCCESS',
  'No new records found'
);


ELSE

MERGE ds_trans.customers_trans T

USING
(
  WITH incremental_customers AS
  (
    SELECT *
    FROM ds_raw.customers_raw

    WHERE load_timestamp >
    (
      SELECT last_processed_timestamp
      FROM ds_admin.process_control
      WHERE table_name = 'customers'
    )
  ),

  latest_customers AS
  (
    SELECT *
    FROM
    (
      SELECT
        customer_id,
        customer_name,
        city,
        created_date,
        source_file_name,
        load_timestamp,

        ROW_NUMBER() OVER
        (
          PARTITION BY customer_id
          ORDER BY load_timestamp DESC
        ) rn

      FROM incremental_customers
    )

    WHERE rn = 1
  )

  SELECT
    customer_id,
    UPPER(TRIM(customer_name)) AS customer_name,
    UPPER(TRIM(city)) AS city,
    created_date,
    'Y' AS is_active,
    source_file_name,
    load_timestamp AS raw_load_timestamp,
    CURRENT_TIMESTAMP() AS transformation_timestamp

  FROM latest_customers

) S

ON T.customer_id = S.customer_id

WHEN MATCHED THEN
  UPDATE SET
    customer_name = S.customer_name,
    city = S.city,
    created_date = S.created_date,
    is_active = S.is_active,
    source_file_name = S.source_file_name,
    raw_load_timestamp = S.raw_load_timestamp,
    transformation_timestamp = CURRENT_TIMESTAMP()

WHEN NOT MATCHED THEN
  INSERT
  (
    customer_id,
    customer_name,
    city,
    created_date,
    is_active,
    source_file_name,
    raw_load_timestamp,
    transformation_timestamp
  )
  VALUES
  (
    S.customer_id,
    S.customer_name,
    S.city,
    S.created_date,
    S.is_active,
    S.source_file_name,
    S.raw_load_timestamp,
    S.transformation_timestamp
  );

-- Update watermark
UPDATE ds_admin.process_control
SET
  last_processed_timestamp =
  (
    SELECT MAX(load_timestamp)
    FROM ds_raw.customers_raw
  ),
  status = 'SUCCESS',
  updated_at = CURRENT_TIMESTAMP()
WHERE table_name = 'customers';

SET v_end_time = CURRENT_TIMESTAMP();

SET v_target_count =
(
  SELECT COUNT(*)
  FROM ds_trans.customers_trans
);

-- Audit
INSERT INTO ds_admin.transform_audit
(
  run_id,
  source_table,
  target_table,
  start_time,
  end_time,
  source_row_count,
  target_row_count,
  status,
  error_message
)
VALUES
(
  GENERATE_UUID(),
  'customers_raw',
  'customers_trans',
  v_start_time,
  v_end_time,
  v_source_count,
  v_target_count,
  'SUCCESS',
  NULL
);


END IF;

END;

CREATE TABLE IF NOT EXISTS ds_trans.products_trans
(
    product_id INT64,

    product_name STRING,

    category STRING,

    unit_price NUMERIC,

    is_active STRING,

    source_file_name STRING,

    raw_load_timestamp TIMESTAMP,

    transformation_timestamp TIMESTAMP
);

INSERT INTO ds_admin.process_control
(
    table_name,
    last_processed_timestamp,
    status,
    updated_at
)
VALUES
(
    'products',
    TIMESTAMP('1900-01-01 00:00:00 UTC'),
    'SUCCESS',
    CURRENT_TIMESTAMP()
);


CREATE OR REPLACE PROCEDURE ds_trans.sp_transform_products()
BEGIN

  DECLARE v_start_time TIMESTAMP;
  DECLARE v_end_time TIMESTAMP;
  DECLARE v_source_count INT64;
  DECLARE v_target_count INT64;

  SET v_start_time = CURRENT_TIMESTAMP();

  SET v_source_count =
  (
    SELECT COUNT(*)
    FROM ds_raw.products_raw
    WHERE load_timestamp >
    (
      SELECT last_processed_timestamp
      FROM ds_admin.process_control
      WHERE table_name = 'products'
    )
  );

  IF v_source_count = 0 THEN

    INSERT INTO ds_admin.transform_audit
    (
      run_id,
      source_table,
      target_table,
      start_time,
      end_time,
      source_row_count,
      target_row_count,
      status,
      error_message
    )
    VALUES
    (
      GENERATE_UUID(),
      'products_raw',
      'products_trans',
      v_start_time,
      CURRENT_TIMESTAMP(),
      0,
      0,
      'SUCCESS',
      'No new records found'
    );

  ELSE

    MERGE ds_trans.products_trans T

    USING
    (
      WITH incremental_products AS
      (
        SELECT *
        FROM ds_raw.products_raw

        WHERE load_timestamp >
        (
          SELECT last_processed_timestamp
          FROM ds_admin.process_control
          WHERE table_name = 'products'
        )
      ),

      latest_products AS
      (
        SELECT *
        FROM
        (
          SELECT *,
                 ROW_NUMBER() OVER
                 (
                   PARTITION BY product_id
                   ORDER BY load_timestamp DESC
                 ) rn
          FROM incremental_products
        )
        WHERE rn = 1
      )

      SELECT
          product_id,
          UPPER(TRIM(product_name)) AS product_name,
          UPPER(TRIM(category)) AS category,
          unit_price,
          'Y' AS is_active,
          source_file_name,
          load_timestamp AS raw_load_timestamp,
          CURRENT_TIMESTAMP() AS transformation_timestamp
      FROM latest_products

    ) S

    ON T.product_id = S.product_id

    WHEN MATCHED THEN
      UPDATE SET
        product_name = S.product_name,
        category = S.category,
        unit_price = S.unit_price,
        is_active = S.is_active,
        source_file_name = S.source_file_name,
        raw_load_timestamp = S.raw_load_timestamp,
        transformation_timestamp = CURRENT_TIMESTAMP()

    WHEN NOT MATCHED THEN
      INSERT
      (
        product_id,
        product_name,
        category,
        unit_price,
        is_active,
        source_file_name,
        raw_load_timestamp,
        transformation_timestamp
      )
      VALUES
      (
        S.product_id,
        S.product_name,
        S.category,
        S.unit_price,
        S.is_active,
        S.source_file_name,
        S.raw_load_timestamp,
        S.transformation_timestamp
      );

    UPDATE ds_admin.process_control
    SET
      last_processed_timestamp =
      (
        SELECT MAX(load_timestamp)
        FROM ds_raw.products_raw
      ),
      status = 'SUCCESS',
      updated_at = CURRENT_TIMESTAMP()
    WHERE table_name = 'products';

    SET v_target_count =
    (
      SELECT COUNT(*)
      FROM ds_trans.products_trans
    );

    INSERT INTO ds_admin.transform_audit
    (
      run_id,
      source_table,
      target_table,
      start_time,
      end_time,
      source_row_count,
      target_row_count,
      status,
      error_message
    )
    VALUES
    (
      GENERATE_UUID(),
      'products_raw',
      'products_trans',
      v_start_time,
      CURRENT_TIMESTAMP(),
      v_source_count,
      v_target_count,
      'SUCCESS',
      NULL
    );

  END IF;

END;

CREATE TABLE IF NOT EXISTS ds_trans.orders_trans
(
    order_id INT64,

    customer_id INT64,

    product_id INT64,

    quantity INT64,

    order_amount NUMERIC,

    order_date DATE,

    order_year INT64,

    order_month INT64,

    order_status STRING,

    last_updated_date DATE,

    source_file_name STRING,

    raw_load_timestamp TIMESTAMP,

    transformation_timestamp TIMESTAMP
);

INSERT INTO ds_admin.process_control
(
    table_name,
    last_processed_timestamp,
    status,
    updated_at
)
VALUES
(
    'orders',
    TIMESTAMP('1900-01-01 00:00:00 UTC'),
    'SUCCESS',
    CURRENT_TIMESTAMP()
);

CREATE OR REPLACE PROCEDURE ds_trans.sp_transform_orders()
BEGIN

DECLARE v_start_time TIMESTAMP;
DECLARE v_end_time TIMESTAMP;
DECLARE v_source_count INT64;
DECLARE v_target_count INT64;

SET v_start_time = CURRENT_TIMESTAMP();

SET v_source_count =
(
SELECT COUNT(*)
FROM ds_raw.orders_raw
WHERE load_timestamp >
(
SELECT last_processed_timestamp
FROM ds_admin.process_control
WHERE table_name = 'orders'
)
);

IF v_source_count = 0 THEN


INSERT INTO ds_admin.transform_audit
(
  run_id,
  source_table,
  target_table,
  start_time,
  end_time,
  source_row_count,
  target_row_count,
  status,
  error_message
)
VALUES
(
  GENERATE_UUID(),
  'orders_raw',
  'orders_trans',
  v_start_time,
  CURRENT_TIMESTAMP(),
  0,
  0,
  'SUCCESS',
  'No new records found'
);


ELSE


MERGE ds_trans.orders_trans T

USING
(
  WITH incremental_orders AS
  (
    SELECT *
    FROM ds_raw.orders_raw

    WHERE load_timestamp >
    (
      SELECT last_processed_timestamp
      FROM ds_admin.process_control
      WHERE table_name = 'orders'
    )
  ),

  latest_orders AS
  (
    SELECT *
    FROM
    (
      SELECT
        *,
        ROW_NUMBER() OVER
        (
          PARTITION BY order_id
          ORDER BY load_timestamp DESC
        ) rn

      FROM incremental_orders
    )
    WHERE rn = 1
  )

  SELECT
    order_id,
    customer_id,
    product_id,
    quantity,
    order_amount,
    order_date,
    EXTRACT(YEAR FROM order_date) AS order_year,
    EXTRACT(MONTH FROM order_date) AS order_month,
    UPPER(TRIM(order_status)) AS order_status,
    last_updated_date,
    source_file_name,
    load_timestamp AS raw_load_timestamp,
    CURRENT_TIMESTAMP() AS transformation_timestamp

  FROM latest_orders

) S

ON T.order_id = S.order_id

WHEN MATCHED THEN

  UPDATE SET

    customer_id = S.customer_id,
    product_id = S.product_id,
    quantity = S.quantity,
    order_amount = S.order_amount,
    order_date = S.order_date,
    order_year = S.order_year,
    order_month = S.order_month,
    order_status = S.order_status,
    last_updated_date = S.last_updated_date,
    source_file_name = S.source_file_name,
    raw_load_timestamp = S.raw_load_timestamp,
    transformation_timestamp = CURRENT_TIMESTAMP()

WHEN NOT MATCHED THEN

  INSERT
  (
    order_id,
    customer_id,
    product_id,
    quantity,
    order_amount,
    order_date,
    order_year,
    order_month,
    order_status,
    last_updated_date,
    source_file_name,
    raw_load_timestamp,
    transformation_timestamp
  )

  VALUES
  (
    S.order_id,
    S.customer_id,
    S.product_id,
    S.quantity,
    S.order_amount,
    S.order_date,
    S.order_year,
    S.order_month,
    S.order_status,
    S.last_updated_date,
    S.source_file_name,
    S.raw_load_timestamp,
    S.transformation_timestamp
  );

UPDATE ds_admin.process_control
SET
  last_processed_timestamp =
  (
    SELECT MAX(load_timestamp)
    FROM ds_raw.orders_raw
  ),
  status = 'SUCCESS',
  updated_at = CURRENT_TIMESTAMP()

WHERE table_name = 'orders';

SET v_end_time = CURRENT_TIMESTAMP();

SET v_target_count =
(
  SELECT COUNT(*)
  FROM ds_trans.orders_trans
);

INSERT INTO ds_admin.transform_audit
(
  run_id,
  source_table,
  target_table,
  start_time,
  end_time,
  source_row_count,
  target_row_count,
  status,
  error_message
)
VALUES
(
  GENERATE_UUID(),
  'orders_raw',
  'orders_trans',
  v_start_time,
  v_end_time,
  v_source_count,
  v_target_count,
  'SUCCESS',
  NULL
);


END IF;

END;
