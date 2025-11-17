"""
System Type Definitions
"""

from enum import Enum
from dataclasses import dataclass
from typing import Any, Callable, List, Optional

class ProcessState(Enum):
    READY = 1
    RUNNING = 2
    BLOCKED = 3
    TERMINATED = 4

class FileType(Enum):
    FILE = 1
    DIRECTORY = 2
    DEVICE = 3

class InterruptType(Enum):
    HARDWARE = 1
    SOFTWARE = 2
    EXCEPTION = 3

@dataclass
class Process:
    pid: int
    name: str
    entry_point: Callable
    state: ProcessState = ProcessState.READY
    priority: int = 1
    program_counter: int = 0
    memory_address: Optional[int] = None
    created_time: float = 0
    user_id: int = 1000
    group_id: int = 1000

@dataclass
class MemoryBlock:
    address: int
    size: int
    process_id: int
    data: List[int]
    description: str = ""
    permissions: int = 0x7  # RWX

@dataclass
class File:
    inode: int
    path: str
    content: str
    size: int
    file_type: FileType
    created: float
    modified: float
    accessed: float = 0
    permissions: int = 0o644
    owner: int = 0
    group: int = 0

@dataclass
class Interrupt:
    vector: int
    type: InterruptType
    timestamp: float
    error_code: int = 0
    cpu_state: Any = None

@dataclass
class SystemInfo:
    kernel_version: str
    total_memory: int
    free_memory: int
    process_count: int
    uptime: float
    load_average: List[float]