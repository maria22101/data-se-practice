"""
Tests lec02.hw.job1.dal.local_disk module
"""
import os
from unittest import TestCase, mock

from lec02.hw.job1.dal.local_disk import save_to_disk


class SaveToDiskTestCase(TestCase):
    """
    Test dal.save_to_disk function.
    """

    @mock.patch('lec02.hw.job1.dal.local_disk.os.makedirs')
    @mock.patch('lec02.hw.job1.dal.local_disk.open', new_callable=mock.mock_open)
    def test_save_to_disk_mini(self, open_mock: mock.MagicMock, makedirs_mock: mock.MagicMock):
        dir_path = 'mock_dir/raw/sales'
        file_name = 'sales_2022-08-09.json'
        json_content = [
            {"client": "John Doe", "purchase_date": "2022-08-09", "product": "Laptop", "price": 1200}
        ]

        save_to_disk(json_content=json_content, dir_path=dir_path, file_name=file_name)

        makedirs_mock.assert_called_once_with(dir_path, exist_ok=True)

        expected_file_path = os.path.join(dir_path, file_name)
        open_mock.assert_called_once_with(expected_file_path, 'w', encoding='utf-8')

        open_mock().write.assert_called()
