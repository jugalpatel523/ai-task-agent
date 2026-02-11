# app/tools/registry.py
from typing import Callable, Awaitable, Any, Dict, Type
from pydantic import BaseModel, ValidationError
import inspect

ToolFn = Callable[[dict[str, Any]], Awaitable[str]]

class ToolSpec:
    def __init__(
        self,
        name: str,
        fn: ToolFn,
        input_model: Type[BaseModel],
        description: str = "",
    ):
        self.name = name
        self.fn = fn
        self.input_model = input_model
        self.description = description

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec):
        self._tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name]

    def list(self) -> list[str]:
        return sorted(self._tools.keys())

    async def execute(self, name: str, payload: dict) -> str:
        tool = self.get(name)

        try:
            validated = tool.input_model(**(payload or {}))
        except ValidationError as e:
            return f"Error: tool_input_validation_failed: {e.errors()}"

        result = tool.fn(validated.model_dump())

        # 🔑 handle sync vs async
        if inspect.isawaitable(result):
            return await result
        return result