"""
open_brain.py — Python utility for reading and writing memories
in the YAPPYVERSE-FACTORY Open Brain (second_brain database).

Connection method: Supabase pg meta /pg/query API endpoint.
No direct PostgreSQL access required.

Usage:
    from tools.open_brain import OpenBrain
    brain = OpenBrain()
    mem_id = brain.save_memory("Title", "Content text", memory_type="insight")
    results = brain.search("query text")
"""

from __future__ import annotations
import json
import os
import urllib.request
import urllib.error
from typing import Any

_VPS_API = os.environ.get("PG_META_URL", "http://31.220.58.212:8001")
_SVC_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", os.environ.get("PG_META_KEY", ""))
_DB_CONN = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:072090156d28a9df6502d94083e47990@localhost:5432/second_brain",
)

MEMORY_TYPES = ("note", "insight", "conversation", "document", "code", "reference", "task", "idea")
MEMORY_STATUSES = ("active", "archived", "draft", "deleted")


class OpenBrain:
    """Persistent memory interface for the second_brain database."""

    def __init__(
        self,
        api_url: str = _VPS_API,
        service_key: str = _SVC_KEY,
        db_conn: str = _DB_CONN,
    ):
        self.api_url = api_url.rstrip("/")
        self.service_key = service_key
        self.db_conn = db_conn
        self._headers = {
            "apikey": service_key,
            "Authorization": f"Bearer {service_key}",
            "Content-Type": "application/json",
        }

    def query(self, sql: str) -> list[dict[str, Any]]:
        body = json.dumps({"query": sql, "connection_string": self.db_conn}).encode()
        req = urllib.request.Request(
            f"{self.api_url}/pg/query", data=body, headers=self._headers, method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"DB query failed (HTTP {e.code}): {e.read().decode()[:300]}")

    def save_memory(
        self,
        title: str,
        content: str,
        *,
        summary: str = "",
        memory_type: str = "note",
        status: str = "active",
        importance: int = 3,
        category_slug: str = "general",
        source: str = "",
        metadata: dict | None = None,
        embedding: list[float] | None = None,
    ) -> str:
        if memory_type not in MEMORY_TYPES:
            raise ValueError(f"type must be one of {MEMORY_TYPES}")
        if importance not in range(1, 6):
            raise ValueError("importance must be 1-5")
        meta_json = json.dumps(metadata or {}).replace("'", "''")
        summary_s = (summary or "").replace("'", "''")
        source_s = (source or "").replace("'", "''")
        title_s = title.replace("'", "''")
        content_s = content.replace("'", "''")
        cats = self.query(f"SELECT id FROM public.categories WHERE slug = '{category_slug}' LIMIT 1")
        cat_id = f"'{cats[0]['id']}'" if cats else "NULL"
        emb_clause = f"'{json.dumps(embedding)}'::vector" if embedding else "NULL"
        rows = self.query(
            f"INSERT INTO public.memories (title, content, summary, type, status, importance, "
            f"category_id, source, metadata, embedding) VALUES ('{title_s}', '{content_s}', "
            f"'{summary_s}', '{memory_type}', '{status}', {importance}, {cat_id}, "
            f"'{source_s}', '{meta_json}'::jsonb, {emb_clause}) RETURNING id"
        )
        return rows[0]["id"]

    def get_memory(self, memory_id: str) -> dict | None:
        rows = self.query(
            f"SELECT m.*, c.name AS category_name, c.slug AS category_slug "
            f"FROM public.memories m LEFT JOIN public.categories c ON c.id = m.category_id "
            f"WHERE m.id = '{memory_id}' LIMIT 1"
        )
        return rows[0] if rows else None

    def update_memory(self, memory_id: str, **fields) -> bool:
        allowed = {"title", "content", "summary", "type", "status",
                   "importance", "source", "metadata", "embedding"}
        updates = []
        for key, val in fields.items():
            if key not in allowed:
                raise ValueError(f"Field '{key}' is not updatable via this method")
            if key == "metadata":
                v = json.dumps(val).replace("'", "''")
                updates.append(f"{key} = '{v}'::jsonb")
            elif key == "embedding":
                updates.append(f"{key} = '{json.dumps(val)}'::vector")
            elif isinstance(val, (int, float)):
                updates.append(f"{key} = {val}")
            else:
                v = str(val).replace("'", "''")
                updates.append(f"{key} = '{v}'")
        if not updates:
            return False
        self.query(f"UPDATE public.memories SET {', '.join(updates)} WHERE id = '{memory_id}'")
        return True

    def delete_memory(self, memory_id: str, hard: bool = False) -> bool:
        if hard:
            self.query(f"DELETE FROM public.memories WHERE id = '{memory_id}'")
        else:
            self.query(f"UPDATE public.memories SET status = 'deleted' WHERE id = '{memory_id}'")
        return True

    def list_memories(
        self,
        *,
        memory_type: str | None = None,
        status: str = "active",
        category_slug: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[dict]:
        where = [f"m.status = '{status}'"]
        if memory_type:
            where.append(f"m.type = '{memory_type}'")
        if category_slug:
            where.append(f"c.slug = '{category_slug}'")
        where_clause = " AND ".join(where)
        return self.query(
            f"SELECT m.id, m.title, m.summary, m.type, m.status, m.importance, "
            f"m.access_count, m.created_at, m.updated_at, "
            f"c.name AS category_name, c.slug AS category_slug "
            f"FROM public.memories m "
            f"LEFT JOIN public.categories c ON c.id = m.category_id "
            f"WHERE {where_clause} "
            f"ORDER BY m.importance DESC, m.updated_at DESC "
            f"LIMIT {limit} OFFSET {offset}"
        )

    def search(self, query: str, limit: int = 10) -> list[dict]:
        q = query.replace("'", "''")
        return self.query(f"SELECT * FROM public.search_memories_fulltext('{q}', {limit})")

    def search_by_vector(
        self, embedding: list[float], limit: int = 10, min_similarity: float = 0.5,
    ) -> list[dict]:
        emb_str = json.dumps(embedding)
        return self.query(
            f"SELECT * FROM public.search_memories_by_vector('{emb_str}'::vector, {limit}, {min_similarity})"
        )

    def ensure_tag(self, name: str, slug: str | None = None, color: str = "#94a3b8") -> str:
        slug = slug or name.lower().replace(" ", "-")
        slug_s = slug.replace("'", "''")
        name_s = name.replace("'", "''")
        rows = self.query(f"SELECT id FROM public.tags WHERE slug = '{slug_s}' LIMIT 1")
        if rows:
            return rows[0]["id"]
        rows = self.query(
            f"INSERT INTO public.tags (name, slug, color) VALUES ('{name_s}', '{slug_s}', '{color}') RETURNING id"
        )
        return rows[0]["id"]

    def tag_memory(self, memory_id: str, tag_name: str) -> None:
        tag_id = self.ensure_tag(tag_name)
        self.query(
            f"INSERT INTO public.memory_tags (memory_id, tag_id) VALUES ('{memory_id}', '{tag_id}') ON CONFLICT DO NOTHING"
        )
        self.query(f"UPDATE public.tags SET count = count + 1 WHERE id = '{tag_id}'")

    def get_tags(self, memory_id: str) -> list[dict]:
        return self.query(f"SELECT * FROM public.get_memory_tags('{memory_id}')")

    def link_memories(
        self, source_id: str, target_id: str, relationship: str = "related", weight: float = 1.0,
    ) -> None:
        self.query(
            f"INSERT INTO public.memory_links (source_memory_id, target_memory_id, relationship_type, weight) "
            f"VALUES ('{source_id}', '{target_id}', '{relationship}', {weight}) "
            f"ON CONFLICT (source_memory_id, target_memory_id) DO UPDATE SET weight = EXCLUDED.weight"
        )

    def get_links(self, memory_id: str) -> list[dict]:
        return self.query(f"SELECT * FROM public.get_linked_memories('{memory_id}')")

    def start_conversation(self, title: str = "") -> str:
        title_s = title.replace("'", "''")
        rows = self.query(f"INSERT INTO public.conversations (title) VALUES ('{title_s}') RETURNING id")
        return rows[0]["id"]

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        embedding: list[float] | None = None,
        memory_refs: list[str] | None = None,
    ) -> str:
        content_s = content.replace("'", "''")
        emb_clause = f"'{json.dumps(embedding)}'::vector" if embedding else "NULL"
        refs_clause = f"ARRAY[{','.join(repr(r) for r in memory_refs)}]::uuid[]" if memory_refs else "NULL"
        rows = self.query(
            f"INSERT INTO public.conversation_messages (conversation_id, role, content, embedding, memory_refs) "
            f"VALUES ('{conversation_id}', '{role}', '{content_s}', {emb_clause}, {refs_clause}) RETURNING id"
        )
        return rows[0]["id"]

    def set_preference(self, key: str, value: Any, description: str = "") -> None:
        key_s = key.replace("'", "''")
        val_j = json.dumps(value).replace("'", "''")
        desc_s = description.replace("'", "''")
        self.query(
            f"INSERT INTO public.user_preferences (key, value, description) "
            f"VALUES ('{key_s}', '{val_j}'::jsonb, '{desc_s}') "
            f"ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW()"
        )

    def get_preference(self, key: str, default: Any = None) -> Any:
        rows = self.query(f"SELECT value FROM public.user_preferences WHERE key = '{key}' LIMIT 1")
        return rows[0]["value"] if rows else default

    def create_collection(self, name: str, description: str = "") -> str:
        name_s = name.replace("'", "''")
        desc_s = description.replace("'", "''")
        rows = self.query(
            f"INSERT INTO public.collections (name, description) VALUES ('{name_s}', '{desc_s}') RETURNING id"
        )
        return rows[0]["id"]

    def add_to_collection(self, collection_id: str, memory_id: str) -> None:
        self.query(
            f"INSERT INTO public.collection_memories (collection_id, memory_id) "
            f"VALUES ('{collection_id}', '{memory_id}') ON CONFLICT DO NOTHING"
        )

    def stats(self) -> dict:
        tables = ["memories", "tags", "categories", "conversations",
                  "conversation_messages", "collections"]
        counts = {}
        for t in tables:
            rows = self.query(f"SELECT COUNT(*) AS n FROM public.{t}")
            counts[t] = rows[0]["n"]
        return counts
