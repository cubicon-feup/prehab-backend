import math
import random
from functools import reduce

from django.db.models import Count

from prehab.helpers.HttpException import HttpException
from prehab_app.models import WeekTaskSchedule
from prehab_app.models.Meal import Meal
from prehab_app.models.MealConstraintType import MealConstraintType


class DataHelper:
    @staticmethod
    def patient_task_schedule_work_load(task_schedule):
        patient_task_schedule_work_load = []  # Each must have: week_number, day_number, meal_id
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
        patient_meal_schedule = []  # Each must have: week_number, day_number, meal_order, meal_id
        available_meals = DataHelper._get_available_meals(constraint_types)

        breakfasts = available_meals.filter(meal_type=1).all()
        snacks = available_meals.filter(meal_type=2).all()
        full_meals = available_meals.filter(meal_type=3).all()

        # Generate for each week
        for week_number in range(1, number_of_weeks + 1):
            breakfast_for_week = DataHelper._get_meals(breakfasts, 7)
            snacks_for_week = DataHelper._get_meals(snacks, 14)
            full_meals_for_week = DataHelper._get_meals(full_meals, 14)
            for day_number in range(7):
                patient_meal_schedule.append({
                    "week_number": week_number,
                    "day_number": day_number + 1,
                    "meal_order": 1,
                    "meal": breakfast_for_week[day_number]
                })
                patient_meal_schedule.append({
                    "week_number": week_number,
                    "day_number": day_number + 1,
                    "meal_order": 2,
                    "meal": snacks_for_week[day_number * 2]
                })
                patient_meal_schedule.append({
                    "week_number": week_number,
                    "day_number": day_number + 1,
                    "meal_order": 3,
                    "meal": full_meals_for_week[day_number * 2]
                })
                patient_meal_schedule.append({
                    "week_number": week_number,
                    "day_number": day_number + 1,
                    "meal_order": 4,
                    "meal": snacks_for_week[day_number * 2 + 1]
                })
                patient_meal_schedule.append({
                    "week_number": week_number,
                    "day_number": day_number + 1,
                    "meal_order": 5,
                    "meal": full_meals_for_week[day_number * 2 + 1]
                })

        return patient_meal_schedule

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

    @staticmethod
    def _get_available_meals(constraint_types):
        if len(constraint_types) == 0:
            available_meals = Meal.objects
        else:
            ids = []
            tmp = {}
            tmp_available_meals = MealConstraintType.objects.values('meal_id').annotate(total=Count('meal')).all()
            for available_meal in tmp_available_meals:
                if available_meal['meal_id'] not in tmp:
                    tmp[available_meal['meal_id']] = 0
                tmp[available_meal['meal_id']] = tmp[available_meal['meal_id']] + available_meal['total']
                if tmp[available_meal['meal_id']] == len(constraint_types):
                    ids.append(available_meal['meal_id'])
            available_meals = Meal.objects.filter(id__in=ids)

        return available_meals

    @staticmethod
    def _get_meals(meals, times):
        meals_bulk = []
        if len(meals) == 0:
            raise HttpException(401, 'Não existem refeições para este tipo de paciente.', 'Number of meals for this type of patient is zero.')

        for i in range(math.ceil(times / len(meals))):
            meals_bulk = meals_bulk + list(meals)

        return random.sample(meals_bulk, times)
