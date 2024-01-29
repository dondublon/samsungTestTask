from dataclasses import dataclass


@dataclass
class Resources:
    ram: int
    cpu_cores: int
    gpu_count: int


@dataclass
class Task:
    id: int | None  # None for adding.
    priority: int
    resources: Resources
    content: str
    result: str

