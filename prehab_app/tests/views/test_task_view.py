from prehab_app.models import Task
from prehab_app.tests.TestSuit import TestSuit


class AuthViewTests(TestSuit):
    url_path = '/api/task/'

    def test_task_create(self):
        # ERROR - test creation of Task without body parameters
        body = {}
        res = self.http_request('post', self.url_path, body)
        self.assertEqual(res.status_code, 400)

        # ERROR - test creation of Task without required parameters: title, multimedia_link
        body = {
            "task_type_id": 1
        }
        res = self.http_request('post', self.url_path, body)
        self.assertEqual(res.status_code, 400)
        body = {
            "title": "task1"
        }
        res = self.http_request('post', self.url_path, body)
        self.assertEqual(res.status_code, 400)

        # ERROR - test creation of Task with task_id not valid
        body = {
            "title": "task1",
            "task_type_id": 100000,
            "description": "This is the task 1",
            "multimedia_link": "prehab.pt/task1.jpg"
        }
        res = self.http_request('post', self.url_path, body)
        self.assertEqual(res.status_code, 400)

        # SUCCESS
        body = {
            "title": "task1",
            "task_type_id": 1,
            "description": "This is the task 1",
            "multimedia_link": "prehab.pt/task1.jpg"
        }
        res = self.http_request('post', self.url_path, body)
        self.assertEqual(res.status_code, 201)
        self.assertTrue('task_id' in res.json()['data'])

        # Assert New Task in Database
        task = Task.objects.filter(id=res.json()['data']['task_id'])
        self.assertEqual(task.count(), 1)
        task = task.get()
        self.assertEqual(task.title, body['title'])
        self.assertEqual(task.task_type.id, body['task_type_id'])
        self.assertEqual(task.description, body['description'])
        self.assertEqual(task.multimedia_link, body['multimedia_link'])

    def test_task_list(self):
        res = self.http_request('get', self.url_path)
        self.assertEqual(res.status_code, 200)

    def test_task_retrieve(self):
        pass
        # ERROR - test retrieve task with inexistent id
        # response = self.client.get(self.url_path + '10000000')
        # self.assertEqual(response.status_code, 404)
        #
        # # ERROR - test retrieve task with existent id
        # body = {
        #     "title": "task1",
        #     "task_type_id": 1,
        #     "description": "This is the task 1",
        #     "multimedia_link": "prehab.pt/task1.jpg"
        # }
        # response = self.client.post(self.url_path, body)
        # task_id = response.json()['data']['task_id']
        # response = self.client.get(self.url_path + str(task_id))
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json()['data'].title, body['title'])
        # self.assertEqual(response.json()['data'].task_type_id, body['task_type_id'])
        # self.assertEqual(response.json()['data'].description, body['description'])
        # self.assertEqual(response.json()['data'].multimedia_link, body['multimedia_link'])
