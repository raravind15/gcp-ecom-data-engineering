CREATE TABLE IF NOT EXISTS ds_curated.dim_customer
(
    customer_key INT64,

    customer_id INT64,

    customer_name STRING,

    city STRING,

    created_date DATE,

    is_active STRING,

    effective_from TIMESTAMP,

    effective_to TIMESTAMP,

    current_flag STRING
);

CREATE OR REPLACE PROCEDURE ds_curated.sp_load_dim_customer()
BEGIN

  -- Update existing customers

  UPDATE ds_curated.dim_customer D

  SET
      customer_name = T.customer_name,
      city = T.city,
      created_date = T.created_date,
      is_active = T.is_active,
      current_flag = 'Y'

  FROM ds_trans.customers_trans T

  WHERE D.customer_id = T.customer_id;

  -- Insert new customers

  INSERT INTO ds_curated.dim_customer
  (
      customer_key,
      customer_id,
      customer_name,
      city,
      created_date,
      is_active,
      effective_from,
      effective_to,
      current_flag
  )

  SELECT

      (
          SELECT COALESCE(MAX(customer_key),0)
          FROM ds_curated.dim_customer
      )
      +
      ROW_NUMBER() OVER
      (
          ORDER BY customer_id
      ) AS customer_key,

      customer_id,
      customer_name,
      city,
      created_date,
      is_active,

      CURRENT_TIMESTAMP(),

      TIMESTAMP('9999-12-31 23:59:59 UTC'),

      'Y'

  FROM ds_trans.customers_trans T

  WHERE NOT EXISTS
  (
      SELECT 1
      FROM ds_curated.dim_customer D
      WHERE D.customer_id = T.customer_id
  );

END;


CALL ds_curated.sp_load_dim_customer();

CREATE TABLE IF NOT EXISTS ds_curated.dim_product
(
    product_key INT64,

    product_id INT64,

    product_name STRING,

    category STRING,

    unit_price NUMERIC,

    is_active STRING,

    effective_from TIMESTAMP,

    effective_to TIMESTAMP,

    current_flag STRING
);

CREATE OR REPLACE PROCEDURE ds_curated.sp_load_dim_product()
BEGIN

  -- Update existing products

  UPDATE ds_curated.dim_product D

  SET
      product_name = T.product_name,
      category = T.category,
      unit_price = T.unit_price,
      is_active = T.is_active,
      current_flag = 'Y'

  FROM ds_trans.products_trans T

  WHERE D.product_id = T.product_id;

  -- Insert new products

  INSERT INTO ds_curated.dim_product
  (
      product_key,
      product_id,
      product_name,
      category,
      unit_price,
      is_active,
      effective_from,
      effective_to,
      current_flag
  )

  SELECT

      (
          SELECT COALESCE(MAX(product_key),0)
          FROM ds_curated.dim_product
      )
      +
      ROW_NUMBER() OVER
      (
          ORDER BY product_id
      ) AS product_key,

      product_id,
      product_name,
      category,
      unit_price,
      is_active,

      CURRENT_TIMESTAMP(),

      TIMESTAMP('9999-12-31 23:59:59 UTC'),

      'Y'

  FROM ds_trans.products_trans T

  WHERE NOT EXISTS
  (
      SELECT 1
      FROM ds_curated.dim_product D
      WHERE D.product_id = T.product_id
  );

END;


call ds_curated.sp_load_dim_product();


CREATE TABLE ds_curated.fact_sales
(
    order_id INT64,

    customer_key INT64,

    product_key INT64,

    quantity INT64,

    order_amount NUMERIC,

    order_date DATE,

    order_year INT64,

    order_month INT64,

    order_status STRING,

    load_timestamp TIMESTAMP
);


CREATE OR REPLACE PROCEDURE ds_curated.sp_load_fact_sales()
BEGIN

  MERGE ds_curated.fact_sales T

  USING
  (
      SELECT

          O.order_id,

          C.customer_key,

          P.product_key,

          O.quantity,

          O.order_amount,

          O.order_date,

          O.order_year,

          O.order_month,

          O.order_status,

          CURRENT_TIMESTAMP() AS load_timestamp

      FROM ds_trans.orders_trans O

      INNER JOIN ds_curated.dim_customer C
          ON O.customer_id = C.customer_id

      INNER JOIN ds_curated.dim_product P
          ON O.product_id = P.product_id

  ) S

  ON T.order_id = S.order_id

  WHEN MATCHED THEN

    UPDATE SET

      customer_key = S.customer_key,
      product_key = S.product_key,
      quantity = S.quantity,
      order_amount = S.order_amount,
      order_date = S.order_date,
      order_year = S.order_year,
      order_month = S.order_month,
      order_status = S.order_status,
      load_timestamp = CURRENT_TIMESTAMP()

  WHEN NOT MATCHED THEN

    INSERT
    (
        order_id,
        customer_key,
        product_key,
        quantity,
        order_amount,
        order_date,
        order_year,
        order_month,
        order_status,
        load_timestamp
    )

    VALUES
    (
        S.order_id,
        S.customer_key,
        S.product_key,
        S.quantity,
        S.order_amount,
        S.order_date,
        S.order_year,
        S.order_month,
        S.order_status,
        S.load_timestamp
    );

END;

CALL ds_curated.sp_load_fact_sales();