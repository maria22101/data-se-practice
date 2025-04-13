"""
Tests lec02.hw.job1.bll.sales_api module
"""
from unittest import TestCase, mock

from lec02.hw.job1.bll.sales_api import save_sales_to_local_disk


class SaveSalesToLocalDiskTestCase(TestCase):

    @mock.patch('lec02.hw.job1.bll.sales_api.rename_file')
    @mock.patch('lec02.hw.job1.bll.sales_api.create_file_path')
    @mock.patch('lec02.hw.job1.bll.sales_api.save_to_disk')
    @mock.patch('lec02.hw.job1.bll.sales_api.get_sales')
    @mock.patch('lec02.hw.job1.bll.sales_api.clean_directory')
    def test_single_page_handling(
        self,
        clean_directory_mock: mock.MagicMock,
        get_sales_mock: mock.MagicMock,
        save_to_disk_mock: mock.MagicMock,
        create_file_path_mock: mock.MagicMock,
        rename_file_mock: mock.MagicMock
    ):
        """
        Test behavior when only a single page of data exists.
        """
        raw_dir = '/foo/raw'
        date = '2022-08-09'

        # Mock `get_sales` to return one page
        get_sales_mock.side_effect = [
            [{"client": "John Doe"}],  # Page 1
            []  # Page 2 (end of data)
        ]

        # Call the function
        save_sales_to_local_disk(date=date, raw_dir=raw_dir)

        # Verify clean_directory is called once
        clean_directory_mock.assert_called_once_with(raw_dir)

        # Verify get_sales is called twice (page 1 + empty page)
        get_sales_mock.assert_any_call(date, 1)
        get_sales_mock.assert_any_call(date, 2)

        # Verify save_to_disk is called correctly
        save_to_disk_mock.assert_called_once_with(
            json_content=[{"client": "John Doe"}],
            dir_path=raw_dir,
            file_name="sales_2022-08-09.json"
        )

        # Verify rename_file is not called for single page
        rename_file_mock.assert_not_called()

    @mock.patch('lec02.hw.job1.bll.sales_api.rename_file')
    @mock.patch('lec02.hw.job1.bll.sales_api.create_file_path')
    @mock.patch('lec02.hw.job1.bll.sales_api.save_to_disk')
    @mock.patch('lec02.hw.job1.bll.sales_api.get_sales')
    @mock.patch('lec02.hw.job1.bll.sales_api.clean_directory')
    def test_multiple_pages_handling(
        self,
        clean_directory_mock: mock.MagicMock,
        get_sales_mock: mock.MagicMock,
        save_to_disk_mock: mock.MagicMock,
        create_file_path_mock: mock.MagicMock,
        rename_file_mock: mock.MagicMock
    ):
        """
        Test behavior when multiple pages of data exist.
        """
        raw_dir = '/foo/raw'
        date = '2022-08-09'

        # Mock `get_sales` to return two pages
        get_sales_mock.side_effect = [
            [{"client": "John Doe"}],  # Page 1
            [{"client": "Jane Smith"}],  # Page 2
            []  # Page 3 (end of data)
        ]

        # Mock create_file_path to generate file paths for rename_file
        create_file_path_mock.side_effect = lambda dir_path, file_name: f"{dir_path}/{file_name}"

        # Call the function
        save_sales_to_local_disk(date=date, raw_dir=raw_dir)

        # Verify clean_directory is called once
        clean_directory_mock.assert_called_once_with(raw_dir)

        # Verify get_sales is called three times (2 pages with data + 1 empty page)
        get_sales_mock.assert_any_call(date, 1)
        get_sales_mock.assert_any_call(date, 2)
        get_sales_mock.assert_any_call(date, 3)

        # Verify data is saved correctly for page 1
        save_to_disk_mock.assert_any_call(
            json_content=[{"client": "John Doe"}],
            dir_path=raw_dir,
            file_name="sales_2022-08-09.json"
        )

        # Verify data is saved correctly for page 2
        save_to_disk_mock.assert_any_call(
            json_content=[{"client": "Jane Smith"}],
            dir_path=raw_dir,
            file_name="sales_2022-08-09_2.json"
        )

        # Verify rename_file is called for multiple pages
        rename_file_mock.assert_called_once_with(
            file_path_from="/foo/raw/sales_2022-08-09.json",
            file_path_to="/foo/raw/sales_2022-08-09_1.json"
        )