"""
This file contains the controller that accepts command via HTTP
and trigger business logic layer
"""
from flask import Flask, request
from flask import typing as flask_typing

from lec02.hw.job2.bll.from_json_to_avro_on_local_disk_api import convert_from_json_to_avro_and_write_to_local_disk

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main() -> flask_typing.ResponseReturnValue:
    """
    Controller that accepts command via HTTP and triggers business logic layer

    body in JSON:
    {
      "raw_dir": "/path/to/my_dir/raw/sales/2022-08-09",
      "stg_dir": "/path/to/my_dir/stg/sales/2022-08-09"
    }
    """
    input_data: dict = request.json
    raw_dir = input_data.get('raw_dir')
    stg_dir = input_data.get('stg_dir')

    if not raw_dir:
        return {
            "message": "raw_dir parameter missed",
        }, 400

    if not stg_dir:
        return {
            "message": "stg_dir parameter missed"
        }, 400

    convert_from_json_to_avro_and_write_to_local_disk(raw_dir=raw_dir, stg_dir=stg_dir)

    return {
        "message": "Data converted successfully from json to avro",
    }, 200


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8082)
