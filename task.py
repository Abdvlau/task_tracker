"""Task class for managing individual tasks."""

from datetime import datetime
from typing import Optional


class Task:
    """Represents a task with an ID, description, status, and timestamps."""
    
    VALID_STATUSES = {"todo", "in-progress", "done"}
    
    def __init__(
        self,
        task_id: int,
        description: str,
        status: str = "todo",
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        """
        Initialize a task.
        
        Args:
            task_id: Unique identifier for the task
            description: Task description
            status: Task status (todo, in-progress, done)
            created_at: Creation timestamp (ISO format)
            updated_at: Last update timestamp (ISO format)
        """
        self.id = task_id
        self.description = description
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convert task to dictionary format."""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a task from dictionary data."""
        return cls(
            task_id=data["id"],
            description=data["description"],
            status=data.get("status", "todo"),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt")
        )
    
    def update_status(self, new_status: str) -> None:
        """Update task status and timestamp."""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {self.VALID_STATUSES}")
        self.status = new_status
        self.updated_at = datetime.now().isoformat()
    
    def update_description(self, new_description: str) -> None:
        """Update task description and timestamp."""
        self.description = new_description
        self.updated_at = datetime.now().isoformat()
    
    def __str__(self) -> str:
        """String representation of the task."""
        return f"[{self.id}] {self.description} - {self.status}"
