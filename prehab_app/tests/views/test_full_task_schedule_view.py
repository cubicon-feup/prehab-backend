from prehab_app.tests.TestSuit import TestSuit
from prehab_app.models import Task


class FullTaskViewTests(TestSuit):
    full_task_path_url = '/api/schedule/task/full/'

    def test_register_full_task(self):
        # Error in schema
        body = {}
        res = self.http_request('post', self.full_task_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter title is a required property')

        # Send only title and fail
        body = {
            "title": "nice_title"
        }
        res = self.http_request('post', self.full_task_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter number_of_weeks is a required property')

        # Need missing weeks - fail
        body = {
            "title": "nice_title",
            "number_of_weeks": 2
        }
        res = self.http_request('post', self.full_task_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter weeks is a required property')

        # Send plan with wrong weeks array
        body = {
            "title": "SomeTitle",
            "number_of_weeks": 2,
            "weeks": [1, 2]
        }
        res = self.http_request('post', self.full_task_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. 1 is not of type object. Review: weeks')

        # Send plan with wrong week_number array
        body = {
            "title": "SomeTitle",
            "number_of_weeks": 2,
            "weeks": [{
                "week_number": "this_should_be_a_number",
                "tasks": [{
                    "task_id": 2,
                    "times_per_week": 2
                }]
            }]
        }
        res = self.http_request('post', self.full_task_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. this_should_be_a_number is not of type integer. Review: weeks')

        # Send plan without week_number
        body = {
            "title": "SomeTitle",
            "number_of_weeks": 2,
            "weeks":
                [{
                    "tasks": [{
                        "task_id": 2,
                        "times_per_week": 2
                    }]
                }]
        }
        res = self.http_request('post', self.full_task_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter week_number is a required property')

        # Send plan without tasks
        body = {
            "title": "SomeTitle",
            "number_of_weeks": 2,
            "weeks":
                [{
                    "week_number": 1,
                    "tasks": {}
                }]
        }
        res = self.http_request('post', self.full_task_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. {} is not of type array. Review: weeks')

        # Send plan without task_id
        body = {
            "title": "SomeTitle",
            "number_of_weeks": 2,
            "weeks":
                [{
                    "week_number": 1,
                    "tasks":
                        [{
                            "times_per_week": 2

                        },
                            {
                                "task_id": 2,
                        }
                        ]},
                    {
                        "week_number": 2,
                        "tasks": [{
                            "times_per_week": 2
                        }]
                }]
        }
        res = self.http_request('post', self.full_task_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter task_id is a required property')

        # Send plan without times_per_week
        body = {
            "title": "SomeTitle",
            "number_of_weeks": 2,
            "weeks":
                [{
                    "week_number": 1,
                    "tasks":
                        [{
                            "task_id": 2,

                        },
                            {
                                "task_id": 2,
                        }
                        ]},
                    {
                        "week_number": 2,
                        "tasks": [{
                            "task_id": 2,
                        }]
                }]
        }
        res = self.http_request('post', self.full_task_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter times_per_week is a required property')

        # Send wrong task_id
        body = {
            "title": "SomeTitle",
            "number_of_weeks": 2,
            "weeks":
                [{
                    "week_number": 1,
                    "tasks":
                        [{
                            "task_id": 2,
                            "times_per_week": 2

                        },
                            {
                                "task_id": 2,
                                "times_per_week": 1
                        }
                        ]},
                    {
                        "week_number": 2,
                        "tasks": [{
                            "task_id": 2,
                            "times_per_week": 2
                        }]
                }]
        }
        res = self.http_request('post', self.full_task_path_url, body)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json()['details'], 'Task with id 2 does not exist.')

        # Test to pass
        task = Task(
            title="taskToPass",
            description="This task is for testing only",
            multimedia_link="link to pass",
            task_type=1
        )
        task.save()

        body = {
            "title": "SomeTitle",
            "number_of_weeks": 2,
            "weeks":
                [{
                    "week_number": 1,
                    "tasks":
                        [{
                            "task_id": 1,
                            "times_per_week": 2

                        },
                            {
                                "task_id": 1,
                                "times_per_week": 1
                        }
                        ]},
                    {
                        "week_number": 2,
                        "tasks": [{
                            "task_id": 1,
                            "times_per_week": 2
                        }]
                }]
        }
        res = self.http_request('post', self.full_task_path_url, body)
        self.assertEqual(res.status_code, 201)

    def test_update_full_task(self):
        # Test Update
        res = self.http_request('put', self.full_task_path_url + '1', auth_user='patient')
        self.assertEqual(res.status_code, 405)

    def test_delete_full_task(self):
        # Test Delete
        res = self.http_request('delete', self.full_task_path_url + '1', auth_user='patient')
        self.assertEqual(res.status_code, 405)
