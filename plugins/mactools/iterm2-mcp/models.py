"""Data models and type definitions for iTerm2 MCP server."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4


class ControlMode(str, Enum):
    """Who currently controls the session."""
    CLAUDE = "claude"
    USER = "user"
    SHARED = "shared"


@dataclass
class SessionState:
    """Internal session state tracking."""

    session_id: UUID = field(default_factory=uuid4)
    iterm_session_id: Optional[str] = None
    tmux_session: Optional[str] = None
    pid: Optional[int] = None
    output_buffer: List[str] = field(default_factory=list)
    last_read_index: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    controlled_by: ControlMode = ControlMode.CLAUDE
    command: Optional[str] = None

    # Pane relationship tracking (for split panes)
    parent_session_id: Optional[UUID] = None
    child_session_ids: List[UUID] = field(default_factory=list)
    pane_position: Optional[str] = None  # "left", "right", "top", "bottom", etc.
    window_id: Optional[str] = None

    def __post_init__(self) -> None:
        """Ensure session_id is UUID."""
        if isinstance(self.session_id, str):
            self.session_id = UUID(self.session_id)


@dataclass
class SessionInfo:
    """Session information for API responses."""

    session_id: str
    tmux_session: Optional[str]
    pid: Optional[int]
    controlled_by: str
    created_at: str
    runtime_seconds: float
    line_count: int
    command: Optional[str]
    parent_session_id: Optional[str] = None
    pane_position: Optional[str] = None
    child_count: int = 0

    @classmethod
    def from_state(cls, state: SessionState) -> "SessionInfo":
        """Create SessionInfo from SessionState."""
        runtime = (datetime.now() - state.created_at).total_seconds()
        return cls(
            session_id=str(state.session_id),
            tmux_session=state.tmux_session,
            pid=state.pid,
            controlled_by=state.controlled_by.value,
            created_at=state.created_at.isoformat(),
            runtime_seconds=runtime,
            line_count=len(state.output_buffer),
            command=state.command,
            parent_session_id=str(state.parent_session_id) if state.parent_session_id else None,
            pane_position=state.pane_position,
            child_count=len(state.child_session_ids),
        )


@dataclass
class PaginatedOutput:
    """Paginated output response."""

    lines: List[str]
    total_lines: int
    read_from: int
    read_count: int
    remaining: int
    session_id: str
    controlled_by: str
