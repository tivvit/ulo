from todoist.api import TodoistAPI
from todoist.models import Item, Project, Label
from typing import Dict, List, Optional
from os import path
import datetime
import collections


class TodoistAPIWrapper:
    def __init__(self):
        self.api = TodoistAPI(self._get_token())
        self.api.sync()
        self.project_map = self._create_project_id_to_project_map()
        self.labels_map = self._create_label_name_to_label_map()

    @staticmethod
    def _get_token() -> str:
        with open(path.expanduser("~/.todoist-token")) as f:
            return f.read()

    def _create_project_id_to_project_map(self) -> Dict[int, Project]:
        return {p["id"]: p for p in self.api.state['projects']}

    def _create_label_name_to_label_map(self) -> Dict[str, Label]:
        return {label["name"]: label for label in self.api.state['labels']}

    def get_items(self) -> List[Item]:
        return self.api.state["items"]

    def get_projects(self) -> List[Project]:
        return self.api.state["projects"]

    def get_projects_with_nested_by_name(self, name: str) -> List[Project]:
        # find project
        project = None
        for p in self.get_projects():
            if p["name"] == name:
                project = p
                break

        if project is None:
            return []

        result = []
        todo = [project]
        while todo:
            pp = todo.pop()
            result.append(pp)
            for p in self.get_projects():
                if p["parent_id"] == pp["id"]:
                    todo.append(p)

        return result


def _item_is_completed(i: Item) -> bool:
    """Is item completed or invalid."""

    if i["checked"] == 1:
        return True
    if i["in_history"] != 0:
        return True
    if i["is_deleted"] != 0:
        return True
    if i["date_completed"] is not None:
        return True
    return False


class Counter:
    def __init__(self, condition, init=0):
        self.state = init
        self.condition = condition

    def __call__(self, *args, **kwargs) -> bool:
        self.state += 1
        return self.condition(self.state)

    def reset(self, state=0):
        self.state = state


def _item_due_date_parser(i: Item) -> Optional[datetime.date]:
    if i["due"] is None:
        return None
    return datetime.datetime.strptime(i["due"]["date"], "%Y-%m-%d").date()


def _item_update_labels(i: Item, labels: List[Label]):
    i.update(labels=list(set([label["id"] for label in labels] + i["labels"])))
    i.api.commit()


def _item_update_due_date(i: Item, date: Optional[str]):
    if date is None:
        i.update(due=date)
    else:
        i.update(due={"string": date})
    i.api.commit()


def main():
    print("Hello from ULO")

    api = TodoistAPIWrapper()
    today_date = datetime.datetime.now().date()
    # do not reschedule last n days
    no_reschedule_days_back = 7
    reschedule_date_limit = today_date - datetime.timedelta(days=no_reschedule_days_back)

    # cnt = Counter(lambda x: x >= 1)
    cnt = Counter(lambda x: False)

    due_items = []
    for i in api.get_items():
        if _item_is_completed(i):
            # Completed items with due date exist (if they are nested), we may ignore them.
            continue

        if i["due"] is None:
            continue
        if i["due"]["is_recurring"]:
            continue

        due_items.append(i)

    print(collections.Counter([api.project_map.get(i["project_id"], {})["name"] for i in due_items]).most_common())

    selected_project_ids = {p["id"] for p in api.get_projects_with_nested_by_name("seznam")}

    print("szn")
    cnt.reset()
    for i in due_items:
        if i["project_id"] not in selected_project_ids:
            continue
        due_date = _item_due_date_parser(i)
        print(i.data)
        project = api.project_map.get(i["project_id"], None)
        print(i["content"], due_date, project["name"], i["labels"])
        _item_update_labels(i, [api.labels_map["deprecated_automatically_had_due_date"]])
        _item_update_due_date(i, None)
        if cnt():
            break

    tasks_per_day_cntr = collections.Counter()
    for i in due_items:
        due_date = _item_due_date_parser(i)
        if due_date is None or due_date < today_date:
            continue
        tasks_per_day_cntr[due_date] += 1

    print(tasks_per_day_cntr)
    due_items.sort(key=lambda x: x["due"]["date"], reverse=True)

    new_distribution = collections.defaultdict(list)
    max_tasks_per_day = 7

    new_date = today_date

    for i in due_items:
        due_date = _item_due_date_parser(i)
        if due_date is None or due_date >= reschedule_date_limit:
            continue

        while tasks_per_day_cntr[new_date] >= max_tasks_per_day:
            new_date += datetime.timedelta(days=1)

        new_distribution[new_date].append(i)
        tasks_per_day_cntr[new_date] += 1

    print("rescheduling")
    for k, v in new_distribution.items():
        print(k)
        for i in v:
            print(f"\t{i['content']}")
            _item_update_labels(i, [api.labels_map["deprecated_automatically_had_due_date"]])
            _item_update_due_date(i, k.strftime("%m/%d/%Y"))


if __name__ == '__main__':
    main()
