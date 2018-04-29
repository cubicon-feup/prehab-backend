import math
from functools import reduce

from django.db.models import Count

from prehab_app.models import WeekTaskSchedule
from prehab_app.models.Meal import Meal
from prehab_app.models.MealConstraintType import MealConstraintType


class DataHelper:
    @staticmethod
    def patient_task_schedule_work_load(task_schedule):
        patient_task_schedule_work_load = []  # Each must have: week_number, day_number, task_id, expected_repetitions
        week_task_schedule = WeekTaskSchedule.objects.filter(task_schedule=task_schedule)

        # Generate for each week
        for week_number in range(1, task_schedule.number_of_weeks + 1):
            week = [[], [], [], [], [], [], []]

            tasks_for_week = week_task_schedule.filter(week_number=week_number).all()  # get tasks per week
            # Equitively distribute tasks through the week
            for task_in_week in tasks_for_week:
                # Get Best Indexes
                indexes = DataHelper._best_indexes_to_put_tasks(week, task_in_week.times_per_week)
                for idx in indexes:
                    week[idx].append({
                        "week_number": week_number,
                        "day_number": idx + 1,
                        "task": task_in_week.task,
                        "expected_repetitions": task_in_week.repetition_number
                    })
            patient_task_schedule_work_load = patient_task_schedule_work_load + reduce(lambda x, y: x + y, week)

        return patient_task_schedule_work_load

    @staticmethod
    def patient_meal_schedule(number_of_weeks, constraint_types):
        if len(constraint_types) == 0:
            available_meals = Meal.objects.all()
        else:
            available_meals = MealConstraintType.objects.filter(constraint_type__in=constraint_types).values('meal__id', 'meal__meal_type').annotate(Count('meal')).filter(count=len(constraint_types)).all()

        return available_meals

    @staticmethod
    def _best_indexes_to_put_tasks(week, times):
        indexes = []
        rate = 7 / times

        if times < 1:
            return indexes

        index_with_min_tasks = 0
        for index, task_list in enumerate(week):
            if len(week[index_with_min_tasks]) > len(task_list):
                index_with_min_tasks = index

        # Put the first Task in the best position
        indexes.append(index_with_min_tasks)
        times = times - 1

        next_index = index_with_min_tasks
        total_times = times
        for time in range(total_times):
            if times == 0:
                return indexes
            next_index = math.ceil(rate) + next_index
            floor = math.floor(next_index) % 7
            ceil = math.ceil(next_index) % 7

            next_index = floor if len(week[floor]) <= len(week[ceil]) else ceil
            indexes.append(next_index)
            times = times - 1

        return indexes

    #
    # @staticmethod
    # def patient_task_schedule_work_load(task_schedule):
    #     # patient_task_schedule_work_load = []  # Each must have: week_number, day_number, task_id, expected_repetitions
    #     weeks = []
    #     week_task_schedule = WeekTaskSchedule.objects.filter(task_schedule=task_schedule)
    #
    #     # Generate for each week
    #     for week_number in range(1, task_schedule.number_of_weeks):
    #         week = []
    #         tasks_for_week = week_task_schedule.filter(week_number=week_number).all()  # get tasks per week
    #         task_types = [t.task.task_type.id for t in tasks_for_week]  # get task_types
    #         for task_type_id in task_types:
    #             tasks_for_week_by_task_type = [t for t in tasks_for_week if t.task.task_type.id == task_type_id]
    #
    #             # Equitively distribute tasks of the same type through the week
    #             for task in tasks_for_week_by_task_type:
    #                 start_index = DataHelper._best_indexes_to_put_tasks(week)
    #                 task_times_per_week = task.times_per_week
    #                 for
    #                 rate = 7 / task.times_per_week
    #                 week[start_index]
    #             continue
    #         continue
    #
    #     weeks = list()
    #     full_tasks = FullTaskScheduleSerializer(task_schedule, many=False).data
    #     for week in full_tasks['weeks']:
    #         continue
    #     days_in_week = 7
    #     week_work_load = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
    #
    #     # for each type of task (Respiratória, Muscular, Resistência)
    #     for task_type, tasks in tasks.items():
    #
    #         for task in tasks:
    #             day_with_min_tasks = DataHelper._best_indexes_to_put_tasks(week_work_load)
    #
    #     return None
