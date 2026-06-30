import logging
import config

bq_client=config.get_bq_client()

def call_transform_procedure(entity):

    procedure_name = (
        f"ds_trans.sp_transform_{entity}"
    )

    bq_client.query(
        f"CALL {procedure_name}();"
    ).result()

    logging.info(
        f"Transformation completed: {procedure_name}"
    )

def call_curated_procedure(entity):

    procedure_map = {
        "customers": "ds_curated.sp_load_dim_customer",
        "products": "ds_curated.sp_load_dim_product",
        "orders": "ds_curated.sp_load_fact_sales"
    }

    procedure_name = procedure_map.get(entity)

    if procedure_name:

        bq_client.query(
            f"CALL {procedure_name}();"
        ).result()

        logging.info(
            f"Curated load completed: {procedure_name}"
        )