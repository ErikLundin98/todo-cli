from __future__ import annotations
import json
import os
from openai import OpenAI

from todo.commands.add import handle_add
from todo.commands.list import handle_list
from todo.commands.remove import handle_remove
from todo.commands.update import handle_update
from todo.constants import Frequency, TaskPriorityLevel, TaskStatus
from datetime import datetime

TOOL_DESCRIPTION = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task with details such as description, priority, status, subtasks, category, deadline, and scheduling options.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Description of the task",
                    },
                    "priority": {
                        "type": "integer",
                        "enum": list(TaskPriorityLevel),
                        "description": f"Priority level of the task ({min(list(TaskPriorityLevel))} = HIGHEST, {max(list(TaskPriorityLevel))} = LOWEST)",
                    },
                    "status": {
                        "type": "string",
                        "enum": list(TaskStatus),
                        "description": "Status of the task",
                    },
                    "subtasks": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of subtasks",
                    },
                    "category": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Categories of the task",
                    },
                    "eod": {
                        "type": ["boolean", "null"],
                        "description": "End of day flag. If true, deadline is end of day.",
                    },
                    "eow": {
                        "type": ["boolean", "null"],
                        "description": "End of week flag. If true, deadline is end of week",
                    },
                    "schedule": {
                        "type": ["string", "null"],
                        "enum": list(Frequency),
                        "description": "Optional scheduling frequency for the task",
                    },
                    "n_occurrences": {
                        "type": "integer",
                        "description": "Number of occurrences for the scheduled task. Required as integer if schedule is used",
                    },
                    "deadline": {
                        "type": ["string", "null"],
                        "format": "date-time",
                        "description": "Deadline for the task (ISO 8601 format). A valid datetime must be supplied if the schedule parameter is used.",
                    },
                },
                "required": ["description", "priority", "status", "n_occurrences"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List tasks based on status, priority, category, and time filters (today or this week).",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": ["array", "null"],
                        "items": {
                            "type": "string",
                            "enum": list(TaskStatus),
                        },
                        "description": "Filter tasks by status",
                    },
                    "priority": {
                        "type": ["array", "null"],
                        "items": {"type": "integer", "enum": list(TaskPriorityLevel)},
                        "description": "Filter tasks by priority",
                    },
                    "category": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter tasks by category",
                    },
                    "week": {
                        "type": ["boolean", "null"],
                        "description": "Filter tasks for the current week",
                    },
                    "today": {
                        "type": ["boolean", "null"],
                        "description": "Filter tasks for today",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remove_tasks",
            "description": "Remove tasks based on their IDs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tasks": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "List of task IDs to remove",
                    }
                },
                "required": ["tasks"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_tasks",
            "description": "Update details of existing tasks, including description, priority, category, deadline, and status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "List of task IDs to update",
                    },
                    "description": {
                        "type": ["string", "null"],
                        "description": "New description of the task",
                    },
                    "priority": {
                        "type": ["integer", "null"],
                        "enum": list(TaskPriorityLevel),
                        "description": f"Priority level of the task ({min(list(TaskPriorityLevel))} = HIGHEST, {max(list(TaskPriorityLevel))} = LOWEST)",
                    },
                    "category": {
                        "type": ["array", "null"],
                        "items": {"type": "string"},
                        "description": "New categories of the task",
                    },
                    "eod": {
                        "type": ["boolean", "null"],
                        "description": "Set deadline to end of day",
                    },
                    "eow": {
                        "type": ["boolean", "null"],
                        "description": "Set deadline to end of week",
                    },
                    "deadline": {
                        "type": ["string", "null"],
                        "format": "date-time",
                        "description": "New deadline for the task (ISO 8601 format)",
                    },
                    "done": {
                        "type": ["boolean", "null"],
                        "description": "Mark task as done",
                    },
                    "todo": {
                        "type": ["boolean", "null"],
                        "description": "Mark task as to do",
                    },
                    "in_progress": {
                        "type": ["boolean", "null"],
                        "description": "Mark task as in progress",
                    },
                    "status": {
                        "type": ["string", "null"],
                        "enum": list(TaskStatus),
                        "description": "New status of the task",
                    },
                    "subtasks": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "string",
                            "enum": list(TaskStatus),
                        },
                        "description": "Update statuses of subtasks, where key is subtask ID and value is new status",
                    },
                },
            },
        },
    },
]


def handle_ai(prompt: str) -> list[str]:
    """Generate a command using the command line interface."""
    _client = OpenAI(
        organization=os.environ.get("OPENAI_ORGANIZATION"),
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    completion = _client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful assistant. Your job is to use the provided functions to help the user manage their TODOs. The current time may be useful, and is {datetime.now()}",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        tools=TOOL_DESCRIPTION,
        tool_choice="required",
        model="gpt-3.5-turbo",
    )
    
    tool_calls = completion.choices[0].message.tool_calls
    for tool_call in tool_calls:
        kwargs = json.loads(tool_call.function.arguments)
        if kwargs.get("deadline"):
            kwargs["deadline"] = datetime.strptime(kwargs["deadline"], "%Y-%m-%dT%H:%M:%S")
        print(f"I inferred that you wanted to {tool_call.function.name} and used arguments {kwargs}")
        match tool_call.function.name:
            case "add_task":
                handle_add(**kwargs)
            case "update_tasks":
                handle_update(**kwargs)
            case "remove_tasks":
                handle_remove(**kwargs)
            case "list_tasks":
                handle_list(**kwargs)
            case _:
                print("I did not manage to perform any task. Please update your prompt and try again")
