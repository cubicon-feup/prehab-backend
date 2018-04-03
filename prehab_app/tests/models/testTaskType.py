from prehab_app.models.TaskType import TaskType
from prehab_app.tests.testSuit import TestSuit


class TaskTypeQuerySetTests(TestSuit):

    def test_task_type_queryset(self):
        queryset = TaskType.objects.task_type(10000)
        self.assertEquals(queryset.count(), 0)
        queryset = TaskType.objects.task_type(1)
        self.assertEquals(queryset.count(), 1)
        self.assertEquals(queryset.get().title, 'Respiratório')


class TaskTypeTests(TestSuit):
    def test_to_string_method(self):
        task_type = TaskType.objects.task_type(1).get()
        self.assertEquals(task_type.__str__(), task_type.title)
