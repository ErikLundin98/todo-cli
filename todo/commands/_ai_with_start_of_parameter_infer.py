# from __future__ import annotations
# import inspect
# from enum import Enum, StrEnum, auto
# import os
# from typing import Any, get_args, get_origin
# from openai import BaseModel, OpenAI

# from todo.commands.add import handle_add
# from todo.commands.list import handle_list
# from todo.commands.remove import handle_remove
# from todo.commands.sync import handle_sync
# from todo.commands.update import handle_update

# class OpenAIDataType(StrEnum):
#     """Supported OpenAI datatypes."""
#     STRING = auto()
#     INTEGER = auto()
#     BOOLEAN = auto()
#     FLOAT = auto()
#     ARRAY = auto()
#     OBJECT = auto()

# class ParameterSpecification(BaseModel):
#     """OpenAI/Mistral tool parameter specification schema."""
#     type: OpenAIDataType
#     enum: Enum
#     items: ParameterSpecification | None = None
#     default: Any = None


# class ToolSpecification(BaseModel):
#     """OpenAI/Mistral tool specification schema."""
#     name: str
#     description: str
#     parameters: ParameterSpecification

# def _create_function_description(
#     func: callable,
# ) -> ToolSpecification:
#     """Parse OpenAI tool specification from a callable."""
#     signature = inspect.signature(func)
#     parameter_specifications: dict[str, ParameterSpecification] = {}
#     breakpoint()
#     for name, param in signature.parameters.items():
#         parameter_specifications[name] = _parse_parameter_specification(param)
#     return parameter_specifications

# def _parse_parameter_specification(param) -> ParameterSpecification:
#     """Parse parameter specification from parameter annotation."""
#     type_hint = param.annotation
#     default = param.default if param.default is not inspect.Parameter.empty else None

#     if type_hint == str:
#         return ParameterSpecification(
#             type=OpenAIDataType.STRING,
#             default=default,
#         )
#     elif type_hint == int:
#         return ParameterSpecification(
#             type=OpenAIDataType.INTEGER,
#             default=default,
#         )
#     elif type_hint == bool:
#         return ParameterSpecification(
#             type=OpenAIDataType.BOOLEAN,
#             default=default,
#         )
#     elif type_hint == float:
#         return ParameterSpecification(
#             type=OpenAIDataType.FLOAT,
#             default=default,
#         )
#     elif type_hint == Enum:
#         pass
#     elif type_hint == list:
#         inner_type = get_args(type_hint)[0]
#         open_ai_data_type = OpenAIDataType.ARRAY
#     elif type_hint == dict:
#         inner_key_type = get_args(type_hint)[0]
#         inner_value_type = get_args(type_hint)[1]
        



#     parameter_specifications[name] = ParameterSpecification(
#         type=None,
#         enum=None,
#         items=None,
#         default=None,
#     )

# _create_function_description(handle_update)

# def handle_ai(prompt: str) -> list[str]:
#     """Generate a command using the command line interface."""
#     _client = OpenAI(
#         organization=os.environ.get("OPENAI_ORGANIZATION"),
#         api_key=os.environ.get("OPENAI_API_KEY"),
#     )
#     chat_completion = _client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": "Say this is a test",
#             }
#         ],
#         tools=[
#             {
#                 "name": "add_task",
#                 "description": "add a task with specified description, deadline, priority, categories & subtasks",
#                 "function": handle_add,
#             },
#             {
#                 "name": "update_task",
#                 "description": "update specific fields of a task",
#                 "function": handle_update,
#             },
#             {
#                 "name": "remove_task",
#                 "description": "remove one or more tasks by id",
#                 "function": handle_remove,
#             },
#             {
#                 "name": "list_tasks",
#                 "description": "list tasks matching a set of criteria",
#                 "function": handle_list,
#             },
#         ],
#         tool_choice="required",
#         model="gpt-3.5-turbo",
#     )
#     breakpoint()