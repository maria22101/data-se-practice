"""
Tests lec02.hw.job1.dal.sales_api module.
"""
from unittest import TestCase, mock

from lec02.hw.job1.dal.sales_api import get_sales


class GetSalesTestCase(TestCase):
    """
    Test sales_api.get_sales function.
    """

    @mock.patch('lec02.hw.job1.dal.sales_api.requests.get')
    @mock.patch('lec02.hw.job1.dal.sales_api.API_AUTH_TOKEN', "fake_token")
    def test_get_sales_successful_response(self, requests_get_mock: mock.MagicMock):
        """
        Test get_sales function when API returns successful response (status code 200).
        """
        # Mocking the response returned by requests.get
        requests_get_mock.return_value.status_code = 200
        requests_get_mock.return_value.json.return_value = [
            {"client": "John Doe", "purchase_date": "2022-08-09", "product": "Laptop", "price": 1200}
        ]

        # Call function
        result = get_sales(date="2022-08-09", page=1)

        # Verify results
        self.assertEqual(
            result,
            [{"client": "John Doe", "purchase_date": "2022-08-09", "product": "Laptop", "price": 1200}],
        )

        # Ensure API call was made with the correct parameters
        requests_get_mock.assert_called_once_with(
            'https://fake-api-vycpfa6oca-uc.a.run.app/sales',
            headers={"Authorization": "fake_token"},
            params={"date": "2022-08-09", "page": 1}
        )

    @mock.patch('lec02.hw.job1.dal.sales_api.requests.get')
    @mock.patch('lec02.hw.job1.dal.sales_api.API_AUTH_TOKEN', "fake_token")
    def test_get_sales_not_found(self, requests_get_mock: mock.MagicMock):
        """
        Test get_sales function when API returns 404 (page not found).
        """
        # Mocking the response returned by requests.get
        requests_get_mock.return_value.status_code = 404

        # Call function
        result = get_sales(date="2022-08-09", page=2)

        # Verify that function returns an empty list for 404 status code
        self.assertEqual(result, [])

    @mock.patch('lec02.hw.job1.dal.sales_api.requests.get')
    @mock.patch('lec02.hw.job1.dal.sales_api.API_AUTH_TOKEN', "fake_token")
    def test_get_sales_api_error(self, requests_get_mock: mock.MagicMock):
        """
        Test get_sales function when API returns an error status (e.g., 500).
        """
        # Mocking the response returned by requests.get
        requests_get_mock.return_value.status_code = 500
        requests_get_mock.return_value.text = "Internal server error"

        # Call function and verify exception is raised
        with self.assertRaises(Exception) as context:
            get_sales(date="2022-08-09", page=3)

        self.assertEqual(str(context.exception), "Failed to fetch data from API, error: 500, Internal server error")

    @mock.patch('lec02.hw.job1.dal.sales_api.requests.get')
    def test_get_sales_no_auth_token(self, requests_get_mock: mock.MagicMock):
        """
        Test get_sales function when AUTH_TOKEN is not set.
        """
        with mock.patch('lec02.hw.job1.dal.sales_api.API_AUTH_TOKEN', None):
            with self.assertRaises(Exception) as context:
                get_sales(date="2022-08-09", page=1)

            self.assertEqual(str(context.exception), "AUTH_TOKEN environment variable must be set")
