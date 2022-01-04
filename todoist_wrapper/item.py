from todoist.models import Item, Label

from typing import Optional, List, Dict

from todoist_wrapper.due import TDDue
from todoist_wrapper.project import TDProject


class TDItem(Item):
    def __init__(self, item: Item, projects: Dict[int, TDProject]):
        super(TDItem, self).__init__(item.data, item.api)
        self.added_by_uid: int = self.data.get("added_by_uid", None)
        self.assigned_by_uid: int = self.data.get("assigned_by_uid", None)
        self.checked: int = self.data.get("checked", None)
        self.child_order: int = self.data.get("child_order", None)
        self.collapsed: int = self.data.get("collapsed", None)
        self.content: str = self.data.get("content", None)
        self.date_added: str = self.data.get("date_added", None)
        self.date_completed: str = self.data.get("date_completed", None)
        self.day_order: int = self.data.get("day_order", None)
        self.description: str = self.data.get("description", None)
        self.due: Optional[TDDue] = TDDue(self.data["due"]) if "due" in self.data and self.data["due"] else None
        self.has_more_notes: bool = self.data.get("has_more_notes", None)
        self.id: int = self.data.get("id", None)
        self.in_history: int = self.data.get("in_history", None)
        self.is_deleted: int = self.data.get("is_deleted", None)
        self.labels: list = self.data.get("labels", None)
        self.legacy_id: int = self.data.get("legacy_id", None)
        self.legacy_project_id: int = self.data.get("legacy_project_id", None)
        self.parent_id: int = self.data.get("parent_id", None)
        self.priority: int = self.data.get("priority", None)
        self.project_id: int = self.data.get("project_id", None)
        self.project: TDProject = projects[self.project_id]
        self.responsible_uid: int = self.data.get("responsible_uid", None)
        self.section_id: int = self.data.get("section_id", None)
        self.sync_id: int = self.data.get("sync_id", None)
        self.user_id: int = self.data.get("user_id", None)
        self.legacy_parent_id: int = self.data.get("legacy_parent_id", None)

    @property
    def is_completed(self) -> bool:
        """Is item completed or invalid."""

        if self.checked == 1:
            return True
        if self.in_history != 0:
            return True
        if self.is_deleted != 0:
            return True
        if self.date_completed is not None:
            return True
        return False

    def update_labels(self, labels: List[Label]):
        self.update(labels=list(set([label["id"] for label in labels] + self.labels)))
        self.api.commit()

    def update_due_date(self, date: Optional[str]):
        if date is None:
            self.update(due=date)
        else:
            self.update(due={"string": date})
        self.api.commit()
