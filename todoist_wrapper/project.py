from todoist.models import Project


class TDProject(Project):
    def __init__(self, project: Project):
        super(TDProject, self).__init__(project.data, project.api)
        self.child_order: int = self.data.get("child_order", None)
        self.collapsed: int = self.data.get("collapsed", None)
        self.color: int = self.data.get("color", None)
        self.has_more_notes: bool = self.data.get("has_more_notes", None)
        self.id: int = self.data.get("id", None)
        self.inbox_project: bool = self.data.get("inbox_project", None)
        self.is_archived: int = self.data.get("is_archived", None)
        self.is_deleted: int = self.data.get("is_deleted", None)
        self.is_favorite: int = self.data.get("is_favorite", None)
        self.legacy_id: int = self.data.get("legacy_id", None)
        self.name: str = self.data.get("name", None)
        self.parent_id: int = self.data.get("parent_id", None)
        self.shared: bool = self.data.get("shared", None)
        self.sync_id: int = self.data.get("sync_id", None)
        self.legacy_parent_id: int = self.data.get("legacy_parent_id", None)

    # todo get_children
