# Open Brain — Persistent Memory for YAPPYVERSE-FACTORY

**Status:** ✅ Live | **Database:** `second_brain` on VPS `31.220.58.212`
**Verified:** March 2026

---

## What It Is

The Open Brain is a self-hosted Supabase database (`second_brain`) running on the
VPS alongside the rest of the YAPPYVERSE stack. It provides persistent, searchable
memory for AI agents — eliminating context re-feeding and enabling long-term
knowledge accumulation.

---

## Access Pattern

All access goes through the Supabase pg meta query API:

```
POST http://31.220.58.212:8001/pg/query
Headers: apikey: <SUPABASE_SERVICE_ROLE_KEY>
         Authorization: Bearer <SUPABASE_SERVICE_ROLE_KEY>
Body:    {"query": "<SQL>", "connection_string": "postgresql://...@localhost:5432/second_brain"}
```

> Note: The `localhost:5432` in the connection string resolves inside the Docker
> network to the Supabase postgres container — **do not change this**.

---

## Python Utility

```python
from tools.open_brain import OpenBrain

brain = OpenBrain()  # reads env vars automatically

# Save a memory
mem_id = brain.save_memory(
    "YAPPYVERSE render pipeline insight",
    "Using Blender headless + queue achieves 3× throughput vs. sequential",
    memory_type="insight",
    importance=4,
    category_slug="code",
)

# Full-text search
results = brain.search("render pipeline performance", limit=5)

# Tag it
brain.tag_memory(mem_id, "blender")
brain.tag_memory(mem_id, "performance")

# Vector search (384-dim embeddings)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
embedding = model.encode("text to search").tolist()
results = brain.search_by_vector(embedding, limit=10, min_similarity=0.6)

# Check stats
print(brain.stats())
```

---

## Schema Summary

| Table | Purpose |
|-------|---------|
| `memories` | Core knowledge with 384-dim vector + fulltext |
| `categories` | 10 default categories (general, work, code, …) |
| `tags` | Flat tag vocabulary |
| `memory_tags` | Many-to-many: memories ↔ tags |
| `memory_links` | Directed relationships between memories |
| `conversations` | Conversation sessions |
| `conversation_messages` | Messages per conversation |
| `user_preferences` | Key-value settings store |
| `collections` | Named memory groupings |
| `collection_memories` | Many-to-many: collections ↔ memories |

**Indexes:** HNSW cosine on `memories.embedding` + `conversation_messages.embedding`,
GIN fulltext, GIN metadata, trigram title, B-tree on type/status/importance/dates.

**Functions:**
- `search_memories_by_vector(embedding, count, min_similarity)` — semantic search
- `search_memories_fulltext(query, count)` — ranked fulltext (title=A, summary=B, content=C)
- `record_memory_access(memory_id)` — track access patterns
- `get_memory_tags(memory_id)` — all tags for a memory
- `get_linked_memories(memory_id)` — related memories (bidirectional)

---

## Re-Deploying the Schema

If the database is wiped, run the idempotent migration:

```bash
# From any machine with access to the VPS:
python tools/apply_schema.py --host 31.220.58.212 --db second_brain
# OR manually via Supabase Studio (port 3001):
#   New query → paste db/second_brain_schema.sql → Run
```

The migration SQL is in `db/second_brain_schema.sql`.

---

## Embedding Dimensions

The schema uses **384-dimensional** embeddings (matching `all-MiniLM-L6-v2`).
If you switch to OpenAI `text-embedding-ada-002` (1536-dim), you must:
1. Drop and recreate the `embedding` column with `vector(1536)`
2. Rebuild the HNSW index

---

## Connection Details

See `Supabase + Open Brain — Connection Details.md` in Downloads for full
credentials. Store secrets in `.env` (see `.env.template`); never hardcode.

---

*OPEN_BRAIN.md | YAPPYVERSE-FACTORY | Agent Zero authority | March 2026*
