"""Storage management for tasks using JSON file."""

import json
import os
from typing import List, Optional
from task import Task


class TaskStorage:
    """Manages task persistence to JSON file."""
    
    def __init__(self, filename: str = "tasks.json"):
        """
        Initialize storage.
        
        Args:
            filename: Path to JSON file for storing tasks
        """
        self.filename = filename
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Create empty tasks file if it doesn't exist."""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)
    
    def load_tasks(self) -> List[Task]:
        """Load all tasks from storage."""
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [Task.from_dict(task_data) for task_data in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_tasks(self, tasks: List[Task]) -> None:
        """Save all tasks to storage."""
        with open(self.filename, 'w') as f:
            task_dicts = [task.to_dict() for task in tasks]
            json.dump(task_dicts, f, indent=2)
    
    def add_task(self, task: Task) -> None:
        """Add a new task to storage."""
        tasks = self.load_tasks()
        tasks.append(task)
        self.save_tasks(tasks)
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        tasks = self.load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, updated_task: Task) -> bool:
        """
        Update a task in storage.
        
        Returns:
            True if task was found and updated, False otherwise
        """
        tasks = self.load_tasks()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                tasks[i] = updated_task
                self.save_tasks(tasks)
                return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from storage.
        
        Returns:
            True if task was found and deleted, False otherwise
        """
        tasks = self.load_tasks()
        initial_length = len(tasks)
        tasks = [task for task in tasks if task.id != task_id]
        if len(tasks) < initial_length:
            self.save_tasks(tasks)
            return True
        return False
    
    def get_next_id(self) -> int:
        """Get the next available task ID."""
        tasks = self.load_tasks()
        if not tasks:
            return 1
        return max(task.id for task in tasks) + 1
