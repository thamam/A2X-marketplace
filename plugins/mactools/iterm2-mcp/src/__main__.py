"""Entry point for running the iTerm2 MCP server as a module."""

from .server import main
import asyncio
import logging
import sys

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutdown by user")
    except Exception as e:
        logger.exception("Server error")
        sys.exit(1)
