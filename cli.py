"""Command-line interface for task tracker."""

import sys
from typing import List
from task import Task
from storage import TaskStorage


class TaskTrackerCLI:
    """Command-line interface for managing tasks."""
    
    def __init__(self):
        """Initialize CLI with storage."""
        self.storage = TaskStorage()
    
    def add_task(self, description: str) -> None:
        """Add a new task."""
        task_id = self.storage.get_next_id()
        task = Task(task_id, description)
        self.storage.add_task(task)
        print(f"Task added successfully (ID: {task_id})")
    
    def update_task(self, task_id: int, description: str) -> None:
        """Update task description."""
        task = self.storage.get_task(task_id)
        if task:
            task.update_description(description)
            self.storage.update_task(task_id, task)
            print(f"Task {task_id} updated successfully")
        else:
            print(f"Task {task_id} not found")
    
    def delete_task(self, task_id: int) -> None:
        """Delete a task."""
        if self.storage.delete_task(task_id):
            print(f"Task {task_id} deleted successfully")
        else:
            print(f"Task {task_id} not found")
    
    def mark_in_progress(self, task_id: int) -> None:
        """Mark task as in progress."""
        self._update_status(task_id, "in-progress")
    
    def mark_done(self, task_id: int) -> None:
        """Mark task as done."""
        self._update_status(task_id, "done")
    
    def _update_status(self, task_id: int, status: str) -> None:
        """Update task status."""
        task = self.storage.get_task(task_id)
        if task:
            task.update_status(status)
            self.storage.update_task(task_id, task)
            print(f"Task {task_id} marked as {status}")
        else:
            print(f"Task {task_id} not found")
    
    def list_tasks(self, status: str = None) -> None:
        """List all tasks or filter by status."""
        tasks = self.storage.load_tasks()
        
        if status:
            tasks = [task for task in tasks if task.status == status]
        
        if not tasks:
            print("No tasks found")
            return
        
        print("\nTasks:")
        print("-" * 60)
        for task in tasks:
            print(f"ID: {task.id}")
            print(f"Description: {task.description}")
            print(f"Status: {task.status}")
            print(f"Created: {task.created_at}")
            print(f"Updated: {task.updated_at}")
            print("-" * 60)
    
    def show_help(self) -> None:
        """Display help message."""
        help_text = """
Task Tracker CLI - Usage:

  python cli.py add <description>          - Add a new task
  python cli.py update <id> <description>  - Update a task
  python cli.py delete <id>                - Delete a task
  python cli.py mark-in-progress <id>      - Mark task as in progress
  python cli.py mark-done <id>             - Mark task as done
  python cli.py list                       - List all tasks
  python cli.py list <status>              - List tasks by status (todo, in-progress, done)
  python cli.py help                       - Show this help message

Examples:
  python cli.py add "Buy groceries"
  python cli.py mark-in-progress 1
  python cli.py mark-done 1
  python cli.py list done
        """
        print(help_text)
    
    def run(self, args: List[str]) -> None:
        """Run CLI with provided arguments."""
        if len(args) < 1:
            self.show_help()
            return
        
        command = args[0].lower()
        
        if command == "add":
            if len(args) < 2:
                print("Error: Description required")
                return
            description = " ".join(args[1:])
            self.add_task(description)
        
        elif command == "update":
            if len(args) < 3:
                print("Error: Task ID and description required")
                return
            try:
                task_id = int(args[1])
                description = " ".join(args[2:])
                self.update_task(task_id, description)
            except ValueError:
                print("Error: Invalid task ID")
        
        elif command == "delete":
            if len(args) < 2:
                print("Error: Task ID required")
                return
            try:
                task_id = int(args[1])
                self.delete_task(task_id)
            except ValueError:
                print("Error: Invalid task ID")
        
        elif command == "mark-in-progress":
            if len(args) < 2:
                print("Error: Task ID required")
                return
            try:
                task_id = int(args[1])
                self.mark_in_progress(task_id)
            except ValueError:
                print("Error: Invalid task ID")
        
        elif command == "mark-done":
            if len(args) < 2:
                print("Error: Task ID required")
                return
            try:
                task_id = int(args[1])
                self.mark_done(task_id)
            except ValueError:
                print("Error: Invalid task ID")
        
        elif command == "list":
            status = args[1] if len(args) > 1 else None
            if status and status not in Task.VALID_STATUSES:
                print(f"Error: Invalid status '{status}'. Must be one of: {', '.join(Task.VALID_STATUSES)}")
                return
            self.list_tasks(status)
        
        elif command == "help":
            self.show_help()
        
        else:
            print(f"Unknown command: {command}")
            self.show_help()


def main():
    """Main entry point for CLI."""
    cli = TaskTrackerCLI()
    cli.run(sys.argv[1:])


if __name__ == "__main__":
    main()
