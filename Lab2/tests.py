import json
import os
import unittest
from unittest.mock import patch, Mock

from main import (
    CurrenciesProviderJSON,
    CSVDecorator,
    YAMLDecorator
)


MOCK_JSON = {
    "Valute": {
        "USD": {
            "CharCode": "USD",
            "Name": "Доллар США",
            "Nominal": 1,
            "Value": 90.0,
            "Previous": 89.5
        }
    }
}


class TestCurrenciesProviderJSON(unittest.TestCase):

    @patch("requests.get")
    def test_get_currencies(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = MOCK_JSON
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        provider = CurrenciesProviderJSON()
        result = provider.get_currencies()

        self.assertIsInstance(result, dict)
        self.assertIn("Valute", result)

    @patch("requests.get")
    def test_save_to_file(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = MOCK_JSON
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        provider = CurrenciesProviderJSON()
        filename = "test.json"
        provider.save_to_file(filename)

        self.assertTrue(os.path.exists(filename))

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data, MOCK_JSON)

        os.remove(filename)


class TestCSVDecorator(unittest.TestCase):

    @patch("requests.get")
    def test_get_currencies(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = MOCK_JSON
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        provider = CSVDecorator(CurrenciesProviderJSON())
        result = provider.get_currencies()

        self.assertEqual(result["format"], "csv")
        self.assertIn("USD", result["csv_text"])

    @patch("requests.get")
    def test_save_to_file(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = MOCK_JSON
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        provider = CSVDecorator(CurrenciesProviderJSON())
        filename = "test.csv"
        provider.save_to_file(filename)

        self.assertTrue(os.path.exists(filename))

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("USD", content)

        os.remove(filename)


class TestYAMLDecorator(unittest.TestCase):

    @patch("requests.get")
    def test_get_currencies(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = MOCK_JSON
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        provider = YAMLDecorator(CurrenciesProviderJSON())
        result = provider.get_currencies()

        self.assertEqual(result["format"], "yaml")
        self.assertIn("USD", result["yaml_text"])

    @patch("requests.get")
    def test_save_to_file(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = MOCK_JSON
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        provider = YAMLDecorator(CurrenciesProviderJSON())
        filename = "test.yaml"
        provider.save_to_file(filename)

        self.assertTrue(os.path.exists(filename))

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("USD", content)

        os.remove(filename)


if __name__ == "__main__":
    unittest.main()