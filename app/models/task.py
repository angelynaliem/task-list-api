from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime, timezone
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(default=None)


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }

    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title=task_data["title"], description=task_data["description"], completed_at=task_data.get("completed_at"))

        return new_task

    def mark_complete(self):
        self.completed_at = datetime.now(timezone.utc)
    
    def mark_incomplete(self):
        self.completed_at = None

