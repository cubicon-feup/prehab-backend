from rest_framework import serializers
import datetime

from prehab_app.models import TaskSchedule
from prehab_app.models.Prehab import Prehab
from prehab_app.serializers.Meal import MealSerializer
from prehab_app.serializers.PatientMealSchedule import PatientMealScheduleSerializer
from prehab_app.serializers.PatientTaskSchedule import PatientTaskScheduleSerializer
from prehab_app.serializers.Task import TaskSerializer


class PrehabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prehab
        fields = '__all__'


class FullPrehabSerializer(serializers.ModelSerializer):
    patient_task_schedule = PatientTaskScheduleSerializer(many=True, read_only=True)
    patient_meal_schedule = PatientMealScheduleSerializer(many=True, read_only=True)
    task_schedule = serializers.SerializerMethodField()
    meal_schedule = serializers.SerializerMethodField()

    def to_representation(self, obj):
        data = super(FullPrehabSerializer, self).to_representation(obj)  # the original data

        # data['task']['expected_repetitions'] = data['expected_repetitions']
        del data['patient_task_schedule']
        del data['patient_meal_schedule']
        data['status_id'] = data['status']
        data['status'] = obj.get_status_display()

        return data

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related(
            'patient_task_schedule',
            'patient_task_schedule__task',
            'patient_meal_schedule',
            'patient_meal_schedule__meal'
        )
        return queryset

    class Meta:
        model = Prehab
        fields = '__all__'

    @staticmethod
    def get_task_schedule(obj):
        task_schedule = {}
        for patient_task in obj.patient_task_schedule.all():
            date = str(obj.init_date + datetime.timedelta(days=7*(patient_task.week_number - 1)) + datetime.timedelta(days=(patient_task.day_number - 1)))

            if date not in task_schedule:
                task_schedule[date] = []

            # task_info = TaskSerializer(task.task, many=False).data
            #             # task_info['id'] = task.id
            #             # task_info['status'] = task.get_status_name()
            #             # task_schedule[date].append(task_info)
            patient_task_info = {
                'id': patient_task.id,
                'task_title': patient_task.task.title,
                'task_description': patient_task.task.description,
                'task_multimedia_link': patient_task.task.multimedia_link,
                'status_id': patient_task.status,
                'status': patient_task.get_status_display(),
                'task_type_id': patient_task.task.task_type,
                'task_type': patient_task.task.get_task_type_display()
            }

            task_schedule[date].append(patient_task_info)

        return task_schedule

    @staticmethod
    def get_meal_schedule(obj):
        meal_schedule = {}
        for patient_meal in obj.patient_meal_schedule.all():
            date = str(obj.init_date + datetime.timedelta(days=7*(patient_meal.week_number - 1)) + datetime.timedelta(days=(patient_meal.day_number - 1)))

            if date not in meal_schedule:
                meal_schedule[date] = []

            # meal_info = MealSerializer(patient_meal.meal, many=False).data
            patient_meal_info = {
                'id': patient_meal.id,
                'meal_title': patient_meal.meal.title,
                'meal_description': patient_meal.meal.description,
                'meal_multimedia_link': patient_meal.meal.multimedia_link,
                'meal_order_id': patient_meal.meal_order,
                'meal_order': patient_meal.get_meal_order_display()
            }

            meal_schedule[date].append(patient_meal_info)

        return meal_schedule
