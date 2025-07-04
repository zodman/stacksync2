import requests
import sys
import faker
import unittest
import os
import zd_google

f = faker.Faker()

url = os.environ.get("URL", 'https://stacksync2.python3.ninja')


class Test(unittest.TestCase):

    def setUp(self):
        try:
            zd_google._cleanup_test()
        except Exception as e:
            pass
        self.name = 'test ' + f.name()

    def create(self, name):
        payload = {
            "data": {
                "zd_title": name
            }
        }
        r = requests.post(f"{url}/create_worksheet/v1/execute", json=payload)
        r.raise_for_status()
        data = r.json()
        self.assertTrue(data['metadata']['success'])

    def append(self, data):
        payload = {
            "data": {
                "zd_title": self.name,
                "zd_data": data
            }
        }
        r = requests.post(f"{url}/append_data/v1/execute", json=payload)
        r.raise_for_status()
        data = r.json()
        self.assertTrue(data['metadata']['success'])

    def pop(self):
        payload = {
            "data": {
                "zd_title": self.name,
            }
        }
        r = requests.post(f"{url}/pop_data/v1/execute", json=payload)
        r.raise_for_status()
        data = r.json()
        self.assertTrue(data['metadata']['success'])

    def test_functional_testing(self):

        self.create(self.name)

        self.append([1, 2])
        self.append([3, 4])
        self.append([5, 6])
        self.pop()
        self.append([7, 8])

    def test_delete_testing(self):
        name = 'test ' + f.name()
        self.create(name)

        payload = {"data": {
            "zd_title": name,
        }
        }

        r = requests.post(f"{url}/delete_worksheet/v1/execute", json=payload)
        r.raise_for_status()
        data = r.json()
        self.assertTrue(data['metadata']['success'], data)


if __name__ == "__main__":
    unittest.main()
