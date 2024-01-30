from dataclasses import dataclass


@dataclass
class Resources:
    ram: int
    cpu_cores: int
    gpu_count: int


@dataclass
class Task:
    id: int | None  # None for adding, int for retrieving.
    priority: int
    resources: Resources
    content: str
    result: str
