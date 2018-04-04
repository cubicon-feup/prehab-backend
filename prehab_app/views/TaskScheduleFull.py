from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.permissions import Permission
from prehab_app.models import TaskSchedule, ScheduleWeekTask, Task, User


class TaskScheduleFullViewSet(GenericViewSet):

    @staticmethod
    def create_task_schedule_full(request):
        try:
            if not Permission.verify(request, ['Admin', 'Doctor']):
                raise HttpException(401)

            # Add Task Schedule

            task_schedule = TaskSchedule(
                title=request.data['title'],
                number_of_weeks=request.data['number_of_weeks'],
                created_by=User.objects.get(id=request.USER_ID),
                is_active=True
            )

            task_schedule.save()

            # For Each Week, add them
            for week in request.data['weeks']:
                week_number = week['week_number']
                if 0 > week_number > request.data['number_of_weeks']:
                    raise HttpException(400, 'Number of week is not allowed.')

                for week_task in week['tasks']:
                    try:
                        task = Task.objects.get(id=week_task['task_id'])
                    except Task.DoesNotExist:
                        raise HttpException(404, 'Task with id {} does not exist.'.format(str(week_task['task_id'])))

                    schedule_week_task = ScheduleWeekTask(
                        task_schedule=task_schedule,
                        week_number=week_number,
                        task=task,
                        times_per_week=week_task['times_per_week']
                    )

                    schedule_week_task.save()

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred.')

        data = {
            'task_schedule_id': task_schedule.id
        }

        return HTTP.response(201, '', data)
