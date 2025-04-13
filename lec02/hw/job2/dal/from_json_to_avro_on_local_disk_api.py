import json

from fastavro import writer

AVRO_SCHEMA = {
    "type": "record",
    "name": "SalesRecord",
    "fields": [
        {"name": "client", "type": "string"},
        {"name": "purchase_date", "type": "string"},
        {"name": "product", "type": "string"},
        {"name": "price", "type": "int"}
    ]
}


def read_from_json(raw_file_path: str) -> str:
    with open(raw_file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    return json_data


def write_to_avro(avro_file_path: str, json_data: str) -> None:
    with open(avro_file_path, 'wb') as avro_file:
        writer(avro_file, AVRO_SCHEMA, json_data)
