"""Session management with tmux integration and output buffering."""

import asyncio
import logging
import subprocess
from typing import Dict, List, Optional
from uuid import UUID

from .iterm_controller import get_controller
from .models import ControlMode, PaginatedOutput, SessionInfo, SessionState

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages terminal sessions with iTerm2 and tmux integration."""

    def __init__(self) -> None:
        self.sessions: Dict[UUID, SessionState] = {}
        self._tmux_available: Optional[bool] = None

    def _check_tmux(self) -> bool:
        """Check if tmux is installed and available."""
        if self._tmux_available is not None:
            return self._tmux_available

        try:
            result = subprocess.run(
                ["which", "tmux"],
                capture_output=True,
                text=True,
                timeout=2,
            )
            self._tmux_available = result.returncode == 0
            if self._tmux_available:
                logger.info("tmux is available")
            else:
                logger.warning("tmux is not installed. Install with: brew install tmux")
            return self._tmux_available
        except Exception as e:
            logger.error(f"Error checking for tmux: {e}")
            self._tmux_available = False
            return False

    async def create_session(
        self,
        command: Optional[str] = None,
        tmux_session: Optional[str] = None,
        profile: Optional[str] = None,
    ) -> Optional[SessionState]:
        """
        Create a new terminal session.

        Args:
            command: Command to run in the session.
            tmux_session: Optional tmux session name for persistence.
            profile: Optional iTerm2 profile name.

        Returns:
            SessionState if successful, None otherwise.
        """
        controller = await get_controller()
        if not controller.is_connected:
            logger.error("Cannot create session: not connected to iTerm2")
            return None

        # Prepare command with tmux if requested
        final_command = command
        if tmux_session:
            if not self._check_tmux():
                logger.error("tmux requested but not available")
                return None

            # Create tmux session and attach
            tmux_cmd = f"tmux new-session -A -s {tmux_session}"
            if command:
                tmux_cmd += f" '{command}'"
            final_command = tmux_cmd

        # Create iTerm2 tab
        iterm_session_id = await controller.create_tab(
            command=final_command,
            profile=profile,
        )

        if not iterm_session_id:
            logger.error("Failed to create iTerm2 tab")
            return None

        # Create session state
        session = SessionState(
            iterm_session_id=iterm_session_id,
            tmux_session=tmux_session,
            command=final_command or command,
            controlled_by=ControlMode.SHARED if tmux_session else ControlMode.CLAUDE,
        )

        # Store session
        self.sessions[session.session_id] = session
        logger.info(
            f"Created session {session.session_id} "
            f"(tmux: {tmux_session}, iterm: {iterm_session_id})"
        )

        return session

    async def send_to_session(self, session_id: UUID, text: str) -> bool:
        """
        Send text to a session.

        Args:
            session_id: Session UUID.
            text: Text to send.

        Returns:
            bool: True if successful, False otherwise.
        """
        session = self.sessions.get(session_id)
        if not session:
            logger.error(f"Session not found: {session_id}")
            return False

        # Send via tmux if available
        if session.tmux_session and self._check_tmux():
            try:
                # Ensure text ends with newline for command execution
                if not text.endswith("\n"):
                    text += "\n"

                result = subprocess.run(
                    ["tmux", "send-keys", "-t", session.tmux_session, text],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

                if result.returncode == 0:
                    logger.debug(f"Sent text via tmux to {session.tmux_session}")
                    return True
                else:
                    logger.error(
                        f"tmux send-keys failed: {result.stderr}"
                    )
            except Exception as e:
                logger.error(f"Error sending via tmux: {e}")

        # Fallback to iTerm2 API
        if session.iterm_session_id:
            controller = await get_controller()
            return await controller.send_text(session.iterm_session_id, text)

        logger.error(f"No method available to send to session {session_id}")
        return False

    def _read_tmux_output(self, tmux_session: str) -> Optional[List[str]]:
        """
        Read output from a tmux session.

        Args:
            tmux_session: tmux session name.

        Returns:
            List of output lines, or None if failed.
        """
        try:
            result = subprocess.run(
                ["tmux", "capture-pane", "-t", tmux_session, "-p"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                lines = result.stdout.split("\n")
                return lines
            else:
                logger.error(f"tmux capture-pane failed: {result.stderr}")
                return None

        except Exception as e:
            logger.error(f"Error reading tmux output: {e}")
            return None

    async def read_session_output(
        self,
        session_id: UUID,
        offset: int = 0,
        length: int = 1000,
    ) -> Optional[PaginatedOutput]:
        """
        Read session output with pagination.

        Args:
            session_id: Session UUID.
            offset: Starting line (0=from last read, positive=absolute, negative=tail).
            length: Maximum lines to return.

        Returns:
            PaginatedOutput if successful, None otherwise.
        """
        session = self.sessions.get(session_id)
        if not session:
            logger.error(f"Session not found: {session_id}")
            return None

        # Update buffer from tmux if available
        if session.tmux_session and self._check_tmux():
            lines = self._read_tmux_output(session.tmux_session)
            if lines is not None:
                session.output_buffer = lines

        # Calculate read range
        total_lines = len(session.output_buffer)

        if offset < 0:
            # Negative offset: read from end
            start_index = max(0, total_lines + offset)
            lines_to_read = session.output_buffer[start_index : start_index + length]
        elif offset == 0:
            # offset=0: read new output since last read
            start_index = session.last_read_index
            lines_to_read = session.output_buffer[start_index : start_index + length]
            # Update last read index
            session.last_read_index = min(start_index + len(lines_to_read), total_lines)
        else:
            # Positive offset: absolute position
            start_index = offset
            lines_to_read = session.output_buffer[start_index : start_index + length]

        read_count = len(lines_to_read)
        end_index = start_index + read_count
        remaining = max(0, total_lines - end_index)

        return PaginatedOutput(
            lines=lines_to_read,
            total_lines=total_lines,
            read_from=start_index,
            read_count=read_count,
            remaining=remaining,
            session_id=str(session_id),
            controlled_by=session.controlled_by.value,
        )

    def list_sessions(self) -> List[SessionInfo]:
        """
        List all active sessions.

        Returns:
            List of SessionInfo objects.
        """
        return [SessionInfo.from_state(session) for session in self.sessions.values()]

    def get_session_state(self, session_id: UUID) -> Optional[SessionState]:
        """
        Get session state by ID.

        Args:
            session_id: Session UUID.

        Returns:
            SessionState if found, None otherwise.
        """
        return self.sessions.get(session_id)

    async def terminate_session(self, session_id: UUID) -> bool:
        """
        Terminate a session.

        Args:
            session_id: Session UUID.

        Returns:
            bool: True if successful, False otherwise.
        """
        session = self.sessions.get(session_id)
        if not session:
            logger.error(f"Session not found: {session_id}")
            return False

        # Kill tmux session if present
        if session.tmux_session and self._check_tmux():
            try:
                result = subprocess.run(
                    ["tmux", "kill-session", "-t", session.tmux_session],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0:
                    logger.info(f"Killed tmux session: {session.tmux_session}")
                else:
                    logger.warning(
                        f"Failed to kill tmux session: {result.stderr}"
                    )
            except Exception as e:
                logger.error(f"Error killing tmux session: {e}")

        # Remove from tracking
        del self.sessions[session_id]
        logger.info(f"Terminated session {session_id}")
        return True

    def set_control_mode(self, session_id: UUID, mode: ControlMode) -> bool:
        """
        Set the control mode for a session.

        Args:
            session_id: Session UUID.
            mode: New control mode.

        Returns:
            bool: True if successful, False otherwise.
        """
        session = self.sessions.get(session_id)
        if not session:
            logger.error(f"Session not found: {session_id}")
            return False

        session.controlled_by = mode
        logger.info(f"Set session {session_id} control mode to {mode.value}")
        return True

    async def create_split_session(
        self,
        parent_session_id: UUID,
        vertical: bool = False,
        command: Optional[str] = None,
        pane_position: Optional[str] = None,
    ) -> Optional[SessionState]:
        """
        Create a new session by splitting an existing pane.

        Args:
            parent_session_id: UUID of the session to split.
            vertical: If True, split vertically; if False, split horizontally.
            command: Optional command to run in the new pane.
            pane_position: Optional position indicator (e.g., "right", "bottom").

        Returns:
            SessionState if successful, None otherwise.
        """
        parent_session = self.sessions.get(parent_session_id)
        if not parent_session:
            logger.error(f"Parent session not found: {parent_session_id}")
            return None

        if not parent_session.iterm_session_id:
            logger.error(f"Parent session has no iTerm2 session ID: {parent_session_id}")
            return None

        controller = await get_controller()
        if not controller.is_connected:
            logger.error("Cannot split pane: not connected to iTerm2")
            return None

        # Split the pane
        new_iterm_session_id = await controller.split_pane(
            parent_session.iterm_session_id,
            vertical=vertical,
            command=command,
        )

        if not new_iterm_session_id:
            logger.error("Failed to split pane")
            return None

        # Create new session state
        new_session = SessionState(
            iterm_session_id=new_iterm_session_id,
            command=command,
            controlled_by=parent_session.controlled_by,
            parent_session_id=parent_session_id,
            pane_position=pane_position,
            window_id=parent_session.window_id,
        )

        # Update parent's child list
        parent_session.child_session_ids.append(new_session.session_id)

        # Store new session
        self.sessions[new_session.session_id] = new_session

        logger.info(
            f"Created split session {new_session.session_id} "
            f"({'vertical' if vertical else 'horizontal'}) "
            f"from parent {parent_session_id}"
        )

        return new_session


# Global session manager instance
_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """
    Get or create the global session manager instance.

    Returns:
        SessionManager: The global manager instance.
    """
    global _manager
    if _manager is None:
        _manager = SessionManager()
    return _manager
