from utils import helper

def test_get_entity_customer():

    file_name=(
        "oracle/orders_app/customers/"
        "2026/06/30/customers_20260630.parquet"
    )

    entity=helper.get_entity_name(file_name)

    assert entity=="customers"

