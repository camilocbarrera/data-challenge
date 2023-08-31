import unittest
from unittest.mock import MagicMock, patch
from app.elt import Extraction


class TestExtraction(unittest.TestCase):

    def setUp(self):
        self.extraction = Extraction("test_file.xlsx", "test/remote/path")

    def test_extract_and_load(self):
        # Mock the necessary objects and methods
        mock_sftpclient = MagicMock()
        mock_s3storage = MagicMock()

        with patch("app.elt.SFTPClient", return_value=mock_sftpclient):
            with patch("app.elt.S3Storage", return_value=mock_s3storage):
                # Mock the connect and disconnect methods
                mock_sftpclient.connect.return_value = None
                mock_sftpclient.disconnect.return_value = None

                # Mock the download_xlsx_to_csv and put_csv_to_s3 methods
                mock_sftpclient.download_xlsx_to_csv.return_value = None
                mock_s3storage.put_csv_to_s3.return_value = None

                result = self.extraction.extract_and_load()

        self.assertEqual(result, {"message:": "success"})

        # Assert that the methods were called as expected
        mock_sftpclient.connect.assert_called_once()
        mock_sftpclient.download_xlsx_to_csv.assert_called_once()
        mock_s3storage.put_csv_to_s3.assert_called_once()
        mock_sftpclient.disconnect.assert_called_once()


if __name__ == '__main__':
    unittest.main()
