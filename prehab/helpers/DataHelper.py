class DataHelper:
    @staticmethod
    def task_schedule_week_work_load(tasks):
        for task_type, tasks in tasks.items():
            continue
        return None

    @staticmethod
    def __index_with_min_tasks_in_day(week_dict):
        index_with_min_tasks = 1

        for week_day, task_list in week_dict.items():
            if len(week_dict[index_with_min_tasks]) > len(task_list):
                index_with_min_tasks = week_day

        return index_with_min_tasks
