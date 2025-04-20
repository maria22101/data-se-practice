import os.path

from lec02.hw.job2.dal.from_json_to_avro_on_local_disk_api import read_from_json, write_to_avro
from lec02.hw.utils.file_utils import clean_directory, create_file_path, list_in_directory


def convert_from_json_to_avro_and_write_to_local_disk(raw_dir: str, stg_dir: str) -> None:
    clean_directory(stg_dir)
    os.makedirs(stg_dir, exist_ok=True)

    for file_name in list_in_directory(raw_dir):
        raw_file_path = create_file_path(raw_dir, file_name)

        if not file_name.endswith('.json'):
            continue

        json_data = read_from_json(raw_file_path)

        avro_file_name = file_name.replace('.json', '.avro')
        avro_file_path = create_file_path(stg_dir, avro_file_name)
        write_to_avro(avro_file_path, json_data)

        print(f"Successfully converted from json file {raw_file_path} to avro file {avro_file_path}")
