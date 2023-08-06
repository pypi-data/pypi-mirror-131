import unittest
import waveletai
import os
from waveletai.app import App
from waveletai.model import Model
from waveletai.feature import Feature


class AppTestCase(unittest.TestCase):
    global app_id
    global dataset_id

    def setUp(self):
        globals()["app_id"] = "d857f8b29eef4a96b1a53cb593d061a7"
        super(AppTestCase, self).setUp()
        waveletai.init(
            api_token="eyJhcGlfdXJsIjogImh0dHA6Ly9mYXQuYWkueGlhb2JvZGF0YS5jb20vYXBpIiwgInVzZXJfaWQiOiAiODhmNmJmODY2NTU2NGI0ZDgxODc1NmMzNTc4YzI0MjIiLCAiYXBpX3Rva2VuIjogImE3NTQ4NmUyNDY1NzliY2I2YTlkMTc4ODAyMjYxNjNiNDA2YTA2OTMxYmYyYmE0NzczMTc3NDY3ZTQxMTg0NWUifQ==")

    def test_1_download_feature_zip(self):
        waveletai.set_app(app_id)
        res = waveletai.download_dataset_artifacts('6ac8b63ee0bc48ed809f248540799931', './feature_zip')

if __name__ == '__main__':
    unittest.main()
