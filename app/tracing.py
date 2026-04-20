from __future__ import annotations

import logging
import os
from typing import Any

_log = logging.getLogger(__name__)

try:
    from langfuse.decorators import observe, langfuse_context
except Exception:  # pragma: no cover
    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func
        return decorator

    class _DummyContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            _log.debug("trace (langfuse unavailable): %s", kwargs)

        def update_current_observation(self, **kwargs: Any) -> None:
            _log.debug("observation (langfuse unavailable): %s", kwargs)

    langfuse_context = _DummyContext()


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))


def tag_trace(tags: list[str]) -> None:
    """Attach tags to the active Langfuse trace."""
    langfuse_context.update_current_trace(tags=tags)


def set_trace_user(user_id: str, session_id: str) -> None:
    """Attach hashed user ID and session ID to the active Langfuse trace."""
    langfuse_context.update_current_trace(user_id=user_id, session_id=session_id)


def annotate_observation(
    metadata: dict[str, Any],
    usage: dict[str, int] | None = None,
) -> None:
    """Attach metadata and optional token usage to the active Langfuse observation."""
    kwargs: dict[str, Any] = {"metadata": metadata}
    if usage is not None:
        kwargs["usage_details"] = usage
    langfuse_context.update_current_observation(**kwargs)
