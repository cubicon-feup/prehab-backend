from prehab_app.models.Task import Task
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
        task = Task.objects.filter(pk=res.json()['data']['task_id'])
        self.assertEqual(task.count(), 1)
        task = task.get()
        self.assertEqual(task.title, body['title'])
        self.assertEqual(task.task_type, body['task_type_id'])
        self.assertEqual(task.description, body['description'])
        self.assertEqual(task.multimedia_link, body['multimedia_link'])

    def test_task_list(self):
        res = self.http_request('get', self.url_path)
        self.assertEqual(res.status_code, 200)

    def test_task_retrieve(self):
        # ERROR - test retrieve task with not existent id
        response = self.http_request('get', self.url_path + '10000')
        self.assertEqual(response.status_code, 404)

        # SUCCESS - test retrieve task with existent id
        task = Task(
            title="task1",
            task_type=1,
            description="This is the task 1",
            multimedia_link="prehab.pt/task1.jpg"
        )
        task.save()

        response = self.http_request('get', self.url_path + str(task.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['title'], task.title)
        self.assertEqual(response.json()['data']['task_type'], task.task_type)
        self.assertEqual(response.json()['data']['description'], task.description)
        self.assertEqual(response.json()['data']['multimedia_link'], task.multimedia_link)
