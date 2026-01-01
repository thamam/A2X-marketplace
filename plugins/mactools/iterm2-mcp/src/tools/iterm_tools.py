"""MCP tool implementations for iTerm2 control."""

import logging
from typing import Any, Dict, List
from uuid import UUID

from pydantic import BaseModel, Field

from ..session_manager import get_session_manager
from ..models import ControlMode

logger = logging.getLogger(__name__)


# Tool Schemas
class CreateItermTabArgs(BaseModel):
    """Arguments for create_iterm_tab tool."""

    command: str | None = Field(
        default=None,
        description="Optional command to run in the new tab",
    )
    tmux_session: str | None = Field(
        default=None,
        description="Optional tmux session name for persistent, shareable sessions",
    )
    profile: str | None = Field(
        default=None,
        description="Optional iTerm2 profile name to use",
    )


class SendToSessionArgs(BaseModel):
    """Arguments for send_to_session tool."""

    session_id: str = Field(
        description="Session ID returned from create_iterm_tab",
    )
    text: str = Field(
        description="Text/command to send to the session",
    )


class ReadSessionOutputArgs(BaseModel):
    """Arguments for read_session_output tool."""

    session_id: str = Field(
        description="Session ID to read output from",
    )
    offset: int = Field(
        default=0,
        description=(
            "Starting line: 0=new output since last read, "
            "positive=absolute line number, negative=tail from end"
        ),
    )
    length: int = Field(
        default=1000,
        description="Maximum number of lines to return",
    )


class CreateSharedSessionArgs(BaseModel):
    """Arguments for create_shared_session tool."""

    tmux_session: str = Field(
        description="Name for the tmux session (user will attach with this name)",
    )
    command: str | None = Field(
        default=None,
        description="Optional command to run in the session",
    )


class AttachUserArgs(BaseModel):
    """Arguments for attach_user_to_session tool."""

    session_id: str = Field(
        description="Session ID to prepare for user attachment",
    )


class TerminateSessionArgs(BaseModel):
    """Arguments for terminate_session tool."""

    session_id: str = Field(
        description="Session ID to terminate",
    )


class SplitPaneArgs(BaseModel):
    """Arguments for split_pane tools."""

    session_id: str = Field(
        description="Session ID of the pane to split",
    )
    command: str | None = Field(
        default=None,
        description="Optional command to run in the new pane",
    )


class ClosePaneArgs(BaseModel):
    """Arguments for close_pane tool."""

    session_id: str = Field(
        description="Session ID of the pane to close",
    )


class FocusPaneArgs(BaseModel):
    """Arguments for focus_pane tool."""

    session_id: str = Field(
        description="Session ID of the pane to focus",
    )


class SendAndSubmitArgs(BaseModel):
    """Arguments for send_and_submit tool."""

    session_id: str = Field(
        description="Session ID to send text to",
    )
    text: str = Field(
        description="Text/prompt to send and submit",
    )
    verify: bool = Field(
        default=True,
        description="Whether to verify the text was submitted",
    )


class DetectClaudeArgs(BaseModel):
    """Arguments for detect_claude_session tool."""

    session_id: str = Field(
        description="Session ID to check for Claude Code",
    )


class GetSessionStateArgs(BaseModel):
    """Arguments for get_session_state tool."""

    session_id: str = Field(
        description="Session ID to get state for",
    )


# Tool Handlers
async def create_iterm_tab(args: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new iTerm2 tab, optionally with tmux."""
    try:
        parsed = CreateItermTabArgs(**args)
        manager = get_session_manager()

        session = await manager.create_session(
            command=parsed.command,
            tmux_session=parsed.tmux_session,
            profile=parsed.profile,
        )

        if not session:
            return {
                "success": False,
                "error": "Failed to create session. Is iTerm2 running?",
            }

        result: Dict[str, Any] = {
            "success": True,
            "session_id": str(session.session_id),
            "tmux_session": session.tmux_session,
            "command": session.command,
            "controlled_by": session.controlled_by.value,
        }

        if session.tmux_session:
            result["message"] = (
                f"Created shared session '{session.tmux_session}'. "
                f"User can attach with: tmux attach -t {session.tmux_session}"
            )

        return result

    except Exception as e:
        logger.error(f"Error in create_iterm_tab: {e}")
        return {"success": False, "error": str(e)}


async def send_to_session(args: Dict[str, Any]) -> Dict[str, Any]:
    """Send text to a session."""
    try:
        parsed = SendToSessionArgs(**args)
        manager = get_session_manager()

        session_id = UUID(parsed.session_id)
        success = await manager.send_to_session(session_id, parsed.text)

        if not success:
            return {
                "success": False,
                "error": "Failed to send text. Session may not exist.",
            }

        # Get session state for context
        session = manager.get_session_state(session_id)
        result: Dict[str, Any] = {
            "success": True,
            "session_id": parsed.session_id,
        }

        if session and session.controlled_by != ControlMode.CLAUDE:
            result["warning"] = (
                f"Session is in {session.controlled_by.value} mode. "
                f"User may also be typing commands."
            )

        return result

    except ValueError:
        return {"success": False, "error": "Invalid session_id format"}
    except Exception as e:
        logger.error(f"Error in send_to_session: {e}")
        return {"success": False, "error": str(e)}


async def read_session_output(args: Dict[str, Any]) -> Dict[str, Any]:
    """Read session output with pagination."""
    try:
        parsed = ReadSessionOutputArgs(**args)
        manager = get_session_manager()

        session_id = UUID(parsed.session_id)
        output = await manager.read_session_output(
            session_id,
            offset=parsed.offset,
            length=parsed.length,
        )

        if not output:
            return {
                "success": False,
                "error": "Session not found or output unavailable",
            }

        return {
            "success": True,
            "session_id": parsed.session_id,
            "output": "\n".join(output.lines),
            "total_lines": output.total_lines,
            "read_from": output.read_from,
            "read_count": output.read_count,
            "remaining": output.remaining,
            "controlled_by": output.controlled_by,
        }

    except ValueError:
        return {"success": False, "error": "Invalid session_id format"}
    except Exception as e:
        logger.error(f"Error in read_session_output: {e}")
        return {"success": False, "error": str(e)}


async def create_shared_session(args: Dict[str, Any]) -> Dict[str, Any]:
    """Create a tmux session for user/Claude sharing."""
    try:
        parsed = CreateSharedSessionArgs(**args)
        manager = get_session_manager()

        session = await manager.create_session(
            command=parsed.command,
            tmux_session=parsed.tmux_session,
        )

        if not session:
            return {
                "success": False,
                "error": (
                    "Failed to create shared session. "
                    "Make sure tmux is installed (brew install tmux)"
                ),
            }

        return {
            "success": True,
            "session_id": str(session.session_id),
            "tmux_session": session.tmux_session,
            "attach_command": f"tmux attach -t {session.tmux_session}",
            "message": (
                f"Created shared tmux session '{session.tmux_session}'. "
                f"User can attach with: tmux attach -t {session.tmux_session}"
            ),
        }

    except Exception as e:
        logger.error(f"Error in create_shared_session: {e}")
        return {"success": False, "error": str(e)}


async def attach_user_to_session(args: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare a session for user attachment."""
    try:
        parsed = AttachUserArgs(**args)
        manager = get_session_manager()

        session_id = UUID(parsed.session_id)
        session = manager.get_session_state(session_id)

        if not session:
            return {"success": False, "error": "Session not found"}

        if not session.tmux_session:
            return {
                "success": False,
                "error": (
                    "Session does not have a tmux session. "
                    "Create with tmux_session parameter for sharing."
                ),
            }

        # Set to shared mode
        manager.set_control_mode(session_id, ControlMode.SHARED)

        return {
            "success": True,
            "session_id": parsed.session_id,
            "tmux_session": session.tmux_session,
            "attach_command": f"tmux attach -t {session.tmux_session}",
            "message": (
                f"Session ready for user. They can attach with:\n"
                f"  tmux attach -t {session.tmux_session}\n\n"
                f"User can detach anytime with Ctrl+B then D"
            ),
        }

    except ValueError:
        return {"success": False, "error": "Invalid session_id format"}
    except Exception as e:
        logger.error(f"Error in attach_user_to_session: {e}")
        return {"success": False, "error": str(e)}


async def list_sessions(args: Dict[str, Any]) -> Dict[str, Any]:
    """List all active sessions."""
    try:
        manager = get_session_manager()
        sessions = manager.list_sessions()

        return {
            "success": True,
            "count": len(sessions),
            "sessions": [
                {
                    "session_id": s.session_id,
                    "tmux_session": s.tmux_session,
                    "command": s.command,
                    "controlled_by": s.controlled_by,
                    "runtime_seconds": s.runtime_seconds,
                    "line_count": s.line_count,
                }
                for s in sessions
            ],
        }

    except Exception as e:
        logger.error(f"Error in list_sessions: {e}")
        return {"success": False, "error": str(e)}


async def terminate_session(args: Dict[str, Any]) -> Dict[str, Any]:
    """Terminate a session."""
    try:
        parsed = TerminateSessionArgs(**args)
        manager = get_session_manager()

        session_id = UUID(parsed.session_id)
        success = await manager.terminate_session(session_id)

        if not success:
            return {"success": False, "error": "Session not found"}

        return {
            "success": True,
            "session_id": parsed.session_id,
            "message": "Session terminated successfully",
        }

    except ValueError:
        return {"success": False, "error": "Invalid session_id format"}
    except Exception as e:
        logger.error(f"Error in terminate_session: {e}")
        return {"success": False, "error": str(e)}


async def split_pane_horizontal(args: Dict[str, Any]) -> Dict[str, Any]:
    """Split pane horizontally."""
    try:
        parsed = SplitPaneArgs(**args)
        manager = get_session_manager()

        parent_session_id = UUID(parsed.session_id)
        new_session = await manager.create_split_session(
            parent_session_id=parent_session_id,
            vertical=False,
            command=parsed.command,
            pane_position="bottom",
        )

        if not new_session:
            return {
                "success": False,
                "error": "Failed to split pane. Session may not exist or iTerm2 error occurred.",
            }

        result: Dict[str, Any] = {
            "success": True,
            "parent_session_id": parsed.session_id,
            "new_session_id": str(new_session.session_id),
            "command": new_session.command,
            "message": f"Pane split horizontally. New pane: {new_session.session_id}",
        }

        return result

    except ValueError:
        return {"success": False, "error": "Invalid session_id format"}
    except Exception as e:
        logger.error(f"Error in split_pane_horizontal: {e}")
        return {"success": False, "error": str(e)}


async def split_pane_vertical(args: Dict[str, Any]) -> Dict[str, Any]:
    """Split pane vertically."""
    try:
        parsed = SplitPaneArgs(**args)
        manager = get_session_manager()

        parent_session_id = UUID(parsed.session_id)
        new_session = await manager.create_split_session(
            parent_session_id=parent_session_id,
            vertical=True,
            command=parsed.command,
            pane_position="right",
        )

        if not new_session:
            return {
                "success": False,
                "error": "Failed to split pane. Session may not exist or iTerm2 error occurred.",
            }

        result: Dict[str, Any] = {
            "success": True,
            "parent_session_id": parsed.session_id,
            "new_session_id": str(new_session.session_id),
            "command": new_session.command,
            "message": f"Pane split vertically. New pane: {new_session.session_id}",
        }

        return result

    except ValueError:
        return {"success": False, "error": "Invalid session_id format"}
    except Exception as e:
        logger.error(f"Error in split_pane_vertical: {e}")
        return {"success": False, "error": str(e)}


async def close_pane(args: Dict[str, Any]) -> Dict[str, Any]:
    """Close a specific pane."""
    try:
        parsed = ClosePaneArgs(**args)
        manager = get_session_manager()

        session_id = UUID(parsed.session_id)
        success = await manager.terminate_session(session_id)

        if not success:
            return {"success": False, "error": "Pane/session not found"}

        return {
            "success": True,
            "session_id": parsed.session_id,
            "message": "Pane closed successfully",
        }

    except ValueError:
        return {"success": False, "error": "Invalid session_id format"}
    except Exception as e:
        logger.error(f"Error in close_pane: {e}")
        return {"success": False, "error": str(e)}


async def focus_pane(args: Dict[str, Any]) -> Dict[str, Any]:
    """Focus/activate a specific pane."""
    try:
        parsed = FocusPaneArgs(**args)
        manager = get_session_manager()

        session_id = UUID(parsed.session_id)
        session = manager.get_session_state(session_id)

        if not session or not session.iterm_session_id:
            return {"success": False, "error": "Pane/session not found"}

        from ..iterm_controller import get_controller

        controller = await get_controller()
        success = await controller.activate_session(session.iterm_session_id)

        if not success:
            return {"success": False, "error": "Failed to focus pane"}

        return {
            "success": True,
            "session_id": parsed.session_id,
            "message": "Pane focused successfully",
        }

    except ValueError:
        return {"success": False, "error": "Invalid session_id format"}
    except Exception as e:
        logger.error(f"Error in focus_pane: {e}")
        return {"success": False, "error": str(e)}


async def send_and_submit(args: Dict[str, Any]) -> Dict[str, Any]:
    """Send text to a session and submit it, with verification."""
    try:
        parsed = SendAndSubmitArgs(**args)
        manager = get_session_manager()

        session_id = UUID(parsed.session_id)

        # Send the text
        await manager.send_to_session(session_id, parsed.text)

        # Submit with carriage return
        await manager.send_to_session(session_id, "\r")

        result: Dict[str, Any] = {
            "success": True,
            "session_id": parsed.session_id,
            "message": "Text sent and submitted",
        }

        # Verify if requested
        if parsed.verify:
            import asyncio
            await asyncio.sleep(0.5)

            # Read the screen to check if text was submitted
            from ..iterm_controller import get_controller
            controller = await get_controller()
            session = manager.get_session_state(session_id)

            if session and session.iterm_session_id:
                import iterm2
                app_session = controller.app.get_session_by_id(session.iterm_session_id)
                if app_session:
                    content = await app_session.async_get_screen_contents()
                    last_lines = []
                    for i in range(max(0, content.number_of_lines - 5), content.number_of_lines):
                        line = content.line(i)
                        last_lines.append(line.string)

                    # Check if the text appears in recent lines
                    recent_text = "\n".join(last_lines)
                    if parsed.text[:50] in recent_text:
                        result["verified"] = True
                        result["message"] += " (verified)"
                    else:
                        result["verified"] = False
                        result["warning"] = "Could not verify text submission"

        return result

    except ValueError:
        return {"success": False, "error": "Invalid session_id format"}
    except Exception as e:
        logger.error(f"Error in send_and_submit: {e}")
        return {"success": False, "error": str(e)}


async def detect_claude_session(args: Dict[str, Any]) -> Dict[str, Any]:
    """Detect if Claude Code is running in a session."""
    try:
        parsed = DetectClaudeArgs(**args)
        manager = get_session_manager()

        session_id = UUID(parsed.session_id)
        session = manager.get_session_state(session_id)

        if not session or not session.iterm_session_id:
            return {"success": False, "error": "Session not found"}

        from ..iterm_controller import get_controller
        controller = await get_controller()

        import iterm2
        app_session = controller.app.get_session_by_id(session.iterm_session_id)
        if not app_session:
            return {"success": False, "error": "iTerm session not found"}

        # Read screen content to detect Claude Code
        content = await app_session.async_get_screen_contents()
        screen_text = ""
        for i in range(content.number_of_lines):
            line = content.line(i)
            screen_text += line.string + "\n"

        # Look for Claude Code indicators
        is_claude = False
        claude_state = "unknown"

        if "claude" in screen_text.lower() or "anthropic" in screen_text.lower():
            is_claude = True

            # Determine state
            if "working" in screen_text.lower() or "thinking" in screen_text.lower():
                claude_state = "processing"
            elif ">" in screen_text[-100:]:  # Prompt visible
                claude_state = "waiting_for_input"
            elif "✓" in screen_text or "completed" in screen_text.lower():
                claude_state = "completed"
            else:
                claude_state = "active"

        return {
            "success": True,
            "session_id": parsed.session_id,
            "is_claude_code": is_claude,
            "state": claude_state,
            "message": f"Claude Code {'detected' if is_claude else 'not detected'} - state: {claude_state}",
        }

    except ValueError:
        return {"success": False, "error": "Invalid session_id format"}
    except Exception as e:
        logger.error(f"Error in detect_claude_session: {e}")
        return {"success": False, "error": str(e)}


async def get_session_state(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get current state and recent output of a session."""
    try:
        parsed = GetSessionStateArgs(**args)
        manager = get_session_manager()

        session_id = UUID(parsed.session_id)
        session = manager.get_session_state(session_id)

        if not session or not session.iterm_session_id:
            return {"success": False, "error": "Session not found"}

        from ..iterm_controller import get_controller
        controller = await get_controller()

        import iterm2
        app_session = controller.app.get_session_by_id(session.iterm_session_id)
        if not app_session:
            return {"success": False, "error": "iTerm session not found"}

        # Get current working directory
        path = await app_session.async_get_variable("path")

        # Get recent screen content
        content = await app_session.async_get_screen_contents()
        recent_lines = []
        for i in range(max(0, content.number_of_lines - 10), content.number_of_lines):
            line = content.line(i)
            if line.string.strip():
                recent_lines.append(line.string)

        return {
            "success": True,
            "session_id": parsed.session_id,
            "path": path,
            "recent_output": recent_lines,
            "pane_position": session.pane_position,
            "parent_session_id": str(session.parent_session_id) if session.parent_session_id else None,
            "child_count": len(session.child_session_ids),
            "message": "Session state retrieved",
        }

    except ValueError:
        return {"success": False, "error": "Invalid session_id format"}
    except Exception as e:
        logger.error(f"Error in get_session_state: {e}")
        return {"success": False, "error": str(e)}


# Tool Registry
TOOLS: List[Dict[str, Any]] = [
    {
        "name": "create_iterm_tab",
        "description": (
            "Create a new iTerm2 tab with optional tmux session for persistence. "
            "Returns session_id for future operations."
        ),
        "inputSchema": CreateItermTabArgs.model_json_schema(),
        "handler": create_iterm_tab,
    },
    {
        "name": "send_to_session",
        "description": "Send text or commands to an active session.",
        "inputSchema": SendToSessionArgs.model_json_schema(),
        "handler": send_to_session,
    },
    {
        "name": "read_session_output",
        "description": (
            "Read output from a session with pagination. "
            "offset=0 reads new output, negative offset reads tail."
        ),
        "inputSchema": ReadSessionOutputArgs.model_json_schema(),
        "handler": read_session_output,
    },
    {
        "name": "create_shared_session",
        "description": (
            "Create a tmux session that both Claude and the user can control. "
            "User can attach/detach freely."
        ),
        "inputSchema": CreateSharedSessionArgs.model_json_schema(),
        "handler": create_shared_session,
    },
    {
        "name": "attach_user_to_session",
        "description": (
            "Prepare a session for user attachment. "
            "Returns tmux attach command for the user."
        ),
        "inputSchema": AttachUserArgs.model_json_schema(),
        "handler": attach_user_to_session,
    },
    {
        "name": "list_sessions",
        "description": "List all active terminal sessions with their status.",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": list_sessions,
    },
    {
        "name": "terminate_session",
        "description": "Terminate a session and clean up resources.",
        "inputSchema": TerminateSessionArgs.model_json_schema(),
        "handler": terminate_session,
    },
    {
        "name": "split_pane_horizontal",
        "description": (
            "Split a pane horizontally (top/bottom). "
            "Creates a new pane below the existing one. "
            "Returns new pane's session_id."
        ),
        "inputSchema": SplitPaneArgs.model_json_schema(),
        "handler": split_pane_horizontal,
    },
    {
        "name": "split_pane_vertical",
        "description": (
            "Split a pane vertically (left/right). "
            "Creates a new pane to the right of the existing one. "
            "Returns new pane's session_id."
        ),
        "inputSchema": SplitPaneArgs.model_json_schema(),
        "handler": split_pane_vertical,
    },
    {
        "name": "close_pane",
        "description": "Close a specific pane/session.",
        "inputSchema": ClosePaneArgs.model_json_schema(),
        "handler": close_pane,
    },
    {
        "name": "focus_pane",
        "description": "Focus/activate a specific pane.",
        "inputSchema": FocusPaneArgs.model_json_schema(),
        "handler": focus_pane,
    },
    {
        "name": "send_and_submit",
        "description": (
            "Send text/prompt to a session and submit it (press Enter). "
            "Optionally verifies the text was actually submitted. "
            "Use this instead of send_to_session when you need to ensure the text is executed."
        ),
        "inputSchema": SendAndSubmitArgs.model_json_schema(),
        "handler": send_and_submit,
    },
    {
        "name": "detect_claude_session",
        "description": (
            "Detect if Claude Code is running in a session and determine its state. "
            "Returns whether Claude Code is detected and its current state: "
            "'processing', 'waiting_for_input', 'completed', or 'active'. "
            "Essential for monitoring Claude sessions."
        ),
        "inputSchema": DetectClaudeArgs.model_json_schema(),
        "handler": detect_claude_session,
    },
    {
        "name": "get_session_state",
        "description": (
            "Get comprehensive state information about a session including: "
            "current directory, recent output, pane position, parent/child relationships. "
            "Use this to monitor and verify session state."
        ),
        "inputSchema": GetSessionStateArgs.model_json_schema(),
        "handler": get_session_state,
    },
]
