"""
Reusable Supabase client service.

Provides two client constructors:
  - get_supabase_client()  → uses SUPABASE_PUBLISHABLE_KEY (anon / public key)
    Safe for operations scoped to the authenticated user via RLS.

  - get_supabase_admin_client()  → uses SUPABASE_SECRET_KEY (service-role key)
    Bypasses RLS. Use only for trusted server-side operations.

Both clients are lazily initialised as module-level singletons so the
connection is reused across the application lifetime.
"""

from supabase import create_client, Client
from app.config import settings


# ---------------------------------------------------------------------------
# Module-level singletons (created on first access)
# ---------------------------------------------------------------------------
_client: Client | None = None
_admin_client: Client | None = None


def get_supabase_client() -> Client:
    """
    Return a Supabase client initialised with the **publishable** (anon) key.

    This client respects Row-Level Security policies and should be the default
    choice for most API operations.

    Raises
    ------
    ValueError
        If SUPABASE_URL or SUPABASE_PUBLISHABLE_KEY are not configured.
    """
    global _client

    if _client is not None:
        return _client

    if not settings.SUPABASE_URL or not settings.SUPABASE_PUBLISHABLE_KEY:
        raise ValueError(
            "Supabase configuration is incomplete. "
            "Set SUPABASE_URL and SUPABASE_PUBLISHABLE_KEY environment variables."
        )

    _client = create_client(settings.SUPABASE_URL, settings.SUPABASE_PUBLISHABLE_KEY)
    return _client


def get_supabase_admin_client() -> Client:
    """
    Return a Supabase client initialised with the **secret** (service-role) key.

    This client bypasses Row-Level Security and must NEVER be exposed to the
    frontend or to any untrusted context.

    Raises
    ------
    ValueError
        If SUPABASE_URL or SUPABASE_SECRET_KEY are not configured.
    """
    global _admin_client

    if _admin_client is not None:
        return _admin_client

    if not settings.SUPABASE_URL or not settings.SUPABASE_SECRET_KEY:
        raise ValueError(
            "Supabase admin configuration is incomplete. "
            "Set SUPABASE_URL and SUPABASE_SECRET_KEY environment variables."
        )

    _admin_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SECRET_KEY)
    return _admin_client
