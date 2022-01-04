from todoist import TodoistAPI
from todoist.models import Project, Label
from typing import Dict, List

from todoist_wrapper.item import TDItem
from todoist_wrapper.item import TDProject
from os import path


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

    def _create_project_id_to_project_map(self) -> Dict[int, TDProject]:
        return {p["id"]: p for p in self.get_projects()}

    def _create_label_name_to_label_map(self) -> Dict[str, Label]:
        return {label["name"]: label for label in self.api.state['labels']}

    def get_items(self) -> List[TDItem]:
        return [TDItem(i, self.project_map) for i in self.api.state["items"]]

    def get_projects(self) -> List[TDProject]:
        return [TDProject(i) for i in self.api.state["projects"]]

    def get_projects_with_nested_by_name(self, name: str) -> List[TDProject]:
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
