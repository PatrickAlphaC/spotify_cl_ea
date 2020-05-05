import unittest
import json
import alpha_vantage_cl_ea as external_adapter
import requests


class TestSpotifyExternalAdapter(unittest.TestCase):

    def setUp(self):

        self.test_config_path = "./test_config.json"
        with open(self.test_config_path, 'r') as file:
            self.test_config = json.load(file)

        self.test_data_path = './test_data.json'
        with open(self.test_data_path, 'r') as file:
            self.test_data = json.load(file)

        external_adapter.client_id = self.test_config['config']['SPOTIPY_CLIENT_ID']
        external_adapter.client_id = self.test_config['config']['SPOTIPY_CLIENT_SECRET']

        self.smoke_test_data = {
            "id": "278c97ffadb54a5bbb93cfec5f7b5503",
            "data": {"artist": "246dkjvS1zLTtiykXe5h60"}
            # This is post malone
        }

    # def test_url_creation(self):
    #     print("testing url creation...")
    #     for test_name in self.test_data['tests']:
    #         data = self.test_data['tests'][test_name]['data']
    #         created_url = external_adapter.create_api_url(data)
    #         expected_url = self.test_data['tests'][test_name]['expected_url']
    #         print(test_name)
    #         if self.assertEqual(created_url, expected_url) is None:
    #             print("Parameters: " + str(data))
    #             print(created_url)

    def test_aws_post(self):
        test_url = self.test_config['config']['AWS_URL']
        r = requests.post(test_url, json=self.smoke_test_data)
        print(r.headers)
        print(r.json())
        self.assertEqual(r.status_code, 200)

    def test_gcs_post(self):
        test_url = self.test_config['config']['GCS_URL']
        r = requests.post(test_url, json=self.smoke_test_data)
        print(r.headers)
        print(r.json())
        self.assertEqual(r.status_code, 200)

    def test_docker_post(self):
        test_url = self.test_config['config']['DOCKER_URL']
        r = requests.post(test_url, json=self.smoke_test_data)
        print(r.headers)
        print(r.json())
        self.assertEqual(r.status_code, 200)
