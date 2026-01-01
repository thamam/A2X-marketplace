"""iTerm2 API controller for creating and managing sessions."""

import asyncio
import logging
from typing import Optional

import iterm2

logger = logging.getLogger(__name__)


class ITerm2Controller:
    """Wrapper around iTerm2 Python API."""

    def __init__(self) -> None:
        self.connection: Optional[iterm2.Connection] = None
        self.app: Optional[iterm2.App] = None
        self._connected = False

    async def connect(self) -> bool:
        """
        Connect to iTerm2.

        Returns:
            bool: True if connected successfully, False otherwise.
        """
        try:
            self.connection = await iterm2.Connection.async_create()
            self.app = await iterm2.async_get_app(self.connection)
            self._connected = True
            logger.info("Successfully connected to iTerm2")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to iTerm2: {e}")
            logger.error(
                "Make sure iTerm2 is running and Python API is enabled "
                "(Preferences > General > Magic > Enable Python API)"
            )
            self._connected = False
            return False

    @property
    def is_connected(self) -> bool:
        """Check if connected to iTerm2."""
        return self._connected and self.connection is not None

    async def create_tab(
        self,
        command: Optional[str] = None,
        profile: Optional[str] = None,
    ) -> Optional[str]:
        """
        Create a new tab in the current iTerm2 window.

        Args:
            command: Optional command to run in the new tab.
            profile: Optional profile name to use.

        Returns:
            str: iTerm2 session ID if successful, None otherwise.
        """
        if not self.is_connected or self.app is None:
            logger.error("Not connected to iTerm2")
            return None

        try:
            # Get current window or create new one
            window = self.app.current_terminal_window
            if window is None:
                logger.info("No current window, creating new window...")
                window = await iterm2.Window.async_create(
                    self.connection,
                    profile=profile,
                    command=command,
                )
                if window is None:
                    logger.error("Failed to create window")
                    return None
                # Get the session from the new window
                tabs = window.tabs
                if tabs and tabs[0].sessions:
                    session = tabs[0].sessions[0]
                    return session.session_id
                return None

            # Create tab in existing window
            tab = await window.async_create_tab(
                profile=profile,
                command=command,
            )
            if tab and tab.sessions:
                session = tab.sessions[0]
                logger.info(f"Created tab with session ID: {session.session_id}")
                return session.session_id

            logger.error("Failed to create tab - no session returned")
            return None

        except Exception as e:
            logger.error(f"Error creating tab: {e}")
            return None

    async def send_text(self, session_id: str, text: str) -> bool:
        """
        Send text to an iTerm2 session.

        Args:
            session_id: iTerm2 session ID.
            text: Text to send.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.is_connected or self.app is None:
            logger.error("Not connected to iTerm2")
            return False

        try:
            session = self.app.get_session_by_id(session_id)
            if session is None:
                logger.error(f"Session not found: {session_id}")
                return False

            await session.async_send_text(text)
            logger.debug(f"Sent text to session {session_id}: {text[:50]}...")
            return True

        except Exception as e:
            logger.error(f"Error sending text to session {session_id}: {e}")
            return False

    async def get_session(self, session_id: str) -> Optional[iterm2.Session]:
        """
        Get an iTerm2 session by ID.

        Args:
            session_id: iTerm2 session ID.

        Returns:
            Session object if found, None otherwise.
        """
        if not self.is_connected or self.app is None:
            logger.error("Not connected to iTerm2")
            return None

        try:
            session = self.app.get_session_by_id(session_id)
            return session
        except Exception as e:
            logger.error(f"Error getting session {session_id}: {e}")
            return None

    async def split_pane(
        self,
        session_id: str,
        vertical: bool = False,
        command: Optional[str] = None,
    ) -> Optional[str]:
        """
        Split a pane horizontally or vertically.

        Args:
            session_id: iTerm2 session ID to split.
            vertical: If True, split vertically; if False, split horizontally.
            command: Optional command to run in the new pane.

        Returns:
            str: New pane's session ID if successful, None otherwise.
        """
        if not self.is_connected or self.app is None:
            logger.error("Not connected to iTerm2")
            return None

        try:
            session = self.app.get_session_by_id(session_id)
            if session is None:
                logger.error(f"Session not found: {session_id}")
                return None

            # Split the pane
            new_session = await session.async_split_pane(vertical=vertical)

            if new_session is None:
                logger.error("Failed to split pane - no session returned")
                return None

            # Run command in new pane if provided
            if command:
                await new_session.async_send_text(command + "\n")

            logger.info(
                f"Split pane {'vertically' if vertical else 'horizontally'}, "
                f"new session ID: {new_session.session_id}"
            )
            return new_session.session_id

        except Exception as e:
            logger.error(f"Error splitting pane: {e}")
            return None

    async def close_session(self, session_id: str) -> bool:
        """
        Close a specific session/pane.

        Args:
            session_id: iTerm2 session ID to close.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.is_connected or self.app is None:
            logger.error("Not connected to iTerm2")
            return False

        try:
            session = self.app.get_session_by_id(session_id)
            if session is None:
                logger.error(f"Session not found: {session_id}")
                return False

            await session.async_close()
            logger.info(f"Closed session: {session_id}")
            return True

        except Exception as e:
            logger.error(f"Error closing session {session_id}: {e}")
            return False

    async def activate_session(self, session_id: str) -> bool:
        """
        Activate/focus a specific session/pane.

        Args:
            session_id: iTerm2 session ID to activate.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.is_connected or self.app is None:
            logger.error("Not connected to iTerm2")
            return False

        try:
            session = self.app.get_session_by_id(session_id)
            if session is None:
                logger.error(f"Session not found: {session_id}")
                return False

            await session.async_activate()
            logger.info(f"Activated session: {session_id}")
            return True

        except Exception as e:
            logger.error(f"Error activating session {session_id}: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from iTerm2."""
        if self.connection:
            try:
                # Note: Connection cleanup is automatic
                self._connected = False
                logger.info("Disconnected from iTerm2")
            except Exception as e:
                logger.error(f"Error during disconnect: {e}")


# Global controller instance
_controller: Optional[ITerm2Controller] = None


async def get_controller() -> ITerm2Controller:
    """
    Get or create the global iTerm2 controller instance.

    Returns:
        ITerm2Controller: The global controller instance.
    """
    global _controller
    if _controller is None:
        _controller = ITerm2Controller()
        await _controller.connect()
    return _controller
