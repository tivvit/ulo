from todoist.api import TodoistAPI
from todoist.models import Item, Project, Label
from typing import Dict, List, Optional, Tuple

import datetime
import collections

from todoist_wrapper.field_analyzer import field_analyzer
from todoist_wrapper.item import TDItem
from todoist_wrapper.api_wrapper import TodoistAPIWrapper


class Counter:
    def __init__(self, condition, init=0):
        self.state = init
        self.condition = condition

    def __call__(self, *args, **kwargs) -> bool:
        self.state += 1
        return self.condition(self.state)

    def reset(self, state=0):
        self.state = state


def analyze_projects(api: TodoistAPI):
    """Get projects objects and analyze the fields."""
    field_analyzer([p.data for p in api.state["projects"]])


def main():
    print("Hello from ULO")

    api = TodoistAPIWrapper()
    today_date = datetime.datetime.now().date()
    # do not reschedule last n days
    no_reschedule_days_back = 7
    reschedule_date_limit = today_date - datetime.timedelta(days=no_reschedule_days_back)

    # cnt = Counter(lambda x: x >= 1)
    cnt = Counter(lambda x: False)

    non_completed_items = [i for i in api.get_items() if not i.is_completed]
    due_items = [i for i in non_completed_items if i.due]

    print(f"total incomplete todos: {len(non_completed_items)}")
    recurring_items = [i for i in due_items if i.due.is_recurring]
    print()

    print("RECURRING STATS")
    for project_name, cnt in collections.Counter([i.project.name for i in
                                                  recurring_items]).most_common():
        print(f"{project_name}: {cnt}")
    print()

    print("STATS")
    for project_name, cnt in collections.Counter([i.project.name for i in
                                                  [j for j in due_items if not j.due.is_recurring]]).most_common():
        print(f"{project_name}: {cnt}")
    print()

    # selected_project_ids = {p["id"] for p in api.get_projects_with_nested_by_name("seznam")}
    #
    # print("szn")
    # cnt.reset()
    # for i in due_items:
    #     if i["project_id"] not in selected_project_ids:
    #         continue
    #     due_date = _item_due_date_parser(i)
    #     print(i.data)
    #     project = api.project_map.get(i["project_id"], None)
    #     print(i["content"], due_date, project["name"], i["labels"])
    #     _item_update_labels(i, [api.labels_map["deprecated_automatically_had_due_date"]])
    #     _item_update_due_date(i, None)
    #     if cnt():
    #         break
    #
    # tasks_per_day_cntr = collections.Counter()
    # for i in due_items:
    #     due_date = _item_due_date_parser(i)
    #     if due_date is None or due_date < today_date:
    #         continue
    #     tasks_per_day_cntr[due_date] += 1
    #
    # print(tasks_per_day_cntr)
    # due_items.sort(key=lambda x: x["due"]["date"], reverse=True)
    #
    # new_distribution = collections.defaultdict(list)
    # max_tasks_per_day = 7
    #
    # new_date = today_date
    #
    # for i in due_items:
    #     due_date = _item_due_date_parser(i)
    #     if due_date is None or due_date >= reschedule_date_limit:
    #         continue
    #
    #     while tasks_per_day_cntr[new_date] >= max_tasks_per_day:
    #         new_date += datetime.timedelta(days=1)
    #
    #     new_distribution[new_date].append(i)
    #     tasks_per_day_cntr[new_date] += 1
    #
    # print("rescheduling")
    # for k, v in new_distribution.items():
    #     print(k)
    #     for i in v:
    #         print(f"\t{i['content']}")
    #         _item_update_labels(i, [api.labels_map["deprecated_automatically_had_due_date"]])
    #         _item_update_due_date(i, k.strftime("%m/%d/%Y"))


if __name__ == '__main__':
    main()
