-- second_brain_schema.sql
-- Idempotent migration — run in the second_brain database
-- Extensions must already be installed (vector, pg_trgm)
-- Last updated: March 2026

-- ── Extensions ────────────────────────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ── categories ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.categories (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    slug        TEXT NOT NULL UNIQUE,
    description TEXT,
    color       TEXT DEFAULT '#6366f1',
    icon        TEXT DEFAULT '📁',
    parent_id   UUID REFERENCES public.categories(id) ON DELETE SET NULL,
    sort_order  INTEGER DEFAULT 0,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ── tags ──────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.tags (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name       TEXT NOT NULL,
    slug       TEXT NOT NULL UNIQUE,
    color      TEXT DEFAULT '#94a3b8',
    count      INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ── memories ──────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.memories (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title            TEXT NOT NULL,
    content          TEXT NOT NULL,
    summary          TEXT,
    type             TEXT DEFAULT 'note'
                       CHECK (type IN ('note','insight','conversation','document',
                                       'code','reference','task','idea')),
    status           TEXT DEFAULT 'active'
                       CHECK (status IN ('active','archived','draft','deleted')),
    importance       INTEGER DEFAULT 3
                       CHECK (importance BETWEEN 1 AND 5),
    category_id      UUID REFERENCES public.categories(id) ON DELETE SET NULL,
    embedding        vector(384),
    metadata         JSONB DEFAULT '{}',
    source           TEXT,
    access_count     INTEGER DEFAULT 0,
    last_accessed_at TIMESTAMPTZ,
    search_vector    tsvector,
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    updated_at       TIMESTAMPTZ DEFAULT NOW()
);

-- ── memory_tags ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.memory_tags (
    memory_id UUID NOT NULL REFERENCES public.memories(id) ON DELETE CASCADE,
    tag_id    UUID NOT NULL REFERENCES public.tags(id) ON DELETE CASCADE,
    PRIMARY KEY (memory_id, tag_id)
);

-- ── memory_links ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.memory_links (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_memory_id  UUID NOT NULL REFERENCES public.memories(id) ON DELETE CASCADE,
    target_memory_id  UUID NOT NULL REFERENCES public.memories(id) ON DELETE CASCADE,
    relationship_type TEXT DEFAULT 'related'
                        CHECK (relationship_type IN ('related','contradicts',
                               'supports','follows_from','part_of','example_of')),
    weight            FLOAT DEFAULT 1.0 CHECK (weight BETWEEN 0 AND 1),
    notes             TEXT,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (source_memory_id, target_memory_id)
);

-- ── conversations ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.conversations (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title      TEXT,
    summary    TEXT,
    metadata   JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ── conversation_messages ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.conversation_messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES public.conversations(id) ON DELETE CASCADE,
    role            TEXT NOT NULL CHECK (role IN ('user','assistant','system','tool')),
    content         TEXT NOT NULL,
    embedding       vector(384),
    memory_refs     UUID[],
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ── user_preferences ──────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.user_preferences (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key         TEXT NOT NULL UNIQUE,
    value       JSONB NOT NULL,
    description TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ── collections ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.collections (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    description TEXT,
    color       TEXT DEFAULT '#6366f1',
    icon        TEXT DEFAULT '📚',
    metadata    JSONB DEFAULT '{}',
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ── collection_memories ───────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.collection_memories (
    collection_id UUID NOT NULL REFERENCES public.collections(id) ON DELETE CASCADE,
    memory_id     UUID NOT NULL REFERENCES public.memories(id) ON DELETE CASCADE,
    sort_order    INTEGER DEFAULT 0,
    added_at      TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (collection_id, memory_id)
);

-- ── Indexes ───────────────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS memories_embedding_hnsw
    ON public.memories USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 128);

CREATE INDEX IF NOT EXISTS messages_embedding_hnsw
    ON public.conversation_messages USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 128);

CREATE INDEX IF NOT EXISTS memories_search_vector_gin
    ON public.memories USING gin(search_vector);

CREATE INDEX IF NOT EXISTS memories_metadata_gin
    ON public.memories USING gin(metadata);

CREATE INDEX IF NOT EXISTS memories_title_trgm
    ON public.memories USING gin(title gin_trgm_ops);

CREATE INDEX IF NOT EXISTS memories_type_idx       ON public.memories(type);
CREATE INDEX IF NOT EXISTS memories_status_idx     ON public.memories(status);
CREATE INDEX IF NOT EXISTS memories_category_idx   ON public.memories(category_id);
CREATE INDEX IF NOT EXISTS memories_importance_idx ON public.memories(importance DESC);
CREATE INDEX IF NOT EXISTS memories_created_at_idx ON public.memories(created_at DESC);
CREATE INDEX IF NOT EXISTS memories_updated_at_idx ON public.memories(updated_at DESC);

-- ── Trigger: tsvector update ─────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION public.update_memory_search_vector()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.search_vector :=
    setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(NEW.summary, '')), 'B') ||
    setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'C');
  RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER memories_tsvector_trigger
BEFORE INSERT OR UPDATE OF title, summary, content
ON public.memories
FOR EACH ROW EXECUTE FUNCTION public.update_memory_search_vector();

-- ── Trigger: updated_at ───────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER memories_updated_at_trigger
BEFORE UPDATE ON public.memories
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE OR REPLACE TRIGGER user_preferences_updated_at_trigger
BEFORE UPDATE ON public.user_preferences
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE OR REPLACE TRIGGER collections_updated_at_trigger
BEFORE UPDATE ON public.collections
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE OR REPLACE TRIGGER conversations_updated_at_trigger
BEFORE UPDATE ON public.conversations
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- ── Search functions ──────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION public.search_memories_by_vector(
    query_embedding vector(384),
    match_count     INT     DEFAULT 10,
    min_similarity  FLOAT   DEFAULT 0.5
)
RETURNS TABLE (
    id          UUID,
    title       TEXT,
    summary     TEXT,
    type        TEXT,
    status      TEXT,
    importance  INTEGER,
    category_id UUID,
    metadata    JSONB,
    created_at  TIMESTAMPTZ,
    similarity  FLOAT
)
LANGUAGE sql STABLE AS $$
  SELECT
    m.id, m.title, m.summary, m.type, m.status,
    m.importance, m.category_id, m.metadata, m.created_at,
    1 - (m.embedding <=> query_embedding) AS similarity
  FROM public.memories m
  WHERE m.status = 'active'
    AND m.embedding IS NOT NULL
    AND 1 - (m.embedding <=> query_embedding) >= min_similarity
  ORDER BY m.embedding <=> query_embedding
  LIMIT match_count;
$$;

CREATE OR REPLACE FUNCTION public.search_memories_fulltext(
    search_query TEXT,
    match_count  INT DEFAULT 10
)
RETURNS TABLE (
    id          UUID,
    title       TEXT,
    summary     TEXT,
    type        TEXT,
    status      TEXT,
    importance  INTEGER,
    category_id UUID,
    metadata    JSONB,
    created_at  TIMESTAMPTZ,
    rank        FLOAT
)
LANGUAGE sql STABLE AS $$
  SELECT
    m.id, m.title, m.summary, m.type, m.status,
    m.importance, m.category_id, m.metadata, m.created_at,
    ts_rank(m.search_vector, plainto_tsquery('english', search_query)) AS rank
  FROM public.memories m
  WHERE m.status = 'active'
    AND m.search_vector @@ plainto_tsquery('english', search_query)
  ORDER BY rank DESC
  LIMIT match_count;
$$;

CREATE OR REPLACE FUNCTION public.record_memory_access(p_memory_id UUID)
RETURNS VOID LANGUAGE plpgsql AS $$
BEGIN
  UPDATE public.memories
  SET access_count     = access_count + 1,
      last_accessed_at = NOW()
  WHERE id = p_memory_id;
END;
$$;

CREATE OR REPLACE FUNCTION public.get_memory_tags(p_memory_id UUID)
RETURNS TABLE (id UUID, name TEXT, slug TEXT, color TEXT)
LANGUAGE sql STABLE AS $$
  SELECT t.id, t.name, t.slug, t.color
  FROM public.tags t
  JOIN public.memory_tags mt ON mt.tag_id = t.id
  WHERE mt.memory_id = p_memory_id
  ORDER BY t.name;
$$;

CREATE OR REPLACE FUNCTION public.get_linked_memories(p_memory_id UUID)
RETURNS TABLE (
    id                UUID,
    title             TEXT,
    type              TEXT,
    relationship_type TEXT,
    weight            FLOAT,
    direction         TEXT
)
LANGUAGE sql STABLE AS $$
  SELECT m.id, m.title, m.type, ml.relationship_type, ml.weight, 'outgoing'
  FROM public.memory_links ml
  JOIN public.memories m ON m.id = ml.target_memory_id
  WHERE ml.source_memory_id = p_memory_id AND m.status = 'active'
  UNION
  SELECT m.id, m.title, m.type, ml.relationship_type, ml.weight, 'incoming'
  FROM public.memory_links ml
  JOIN public.memories m ON m.id = ml.source_memory_id
  WHERE ml.target_memory_id = p_memory_id AND m.status = 'active'
  ORDER BY weight DESC;
$$;

-- ── Seed default categories ───────────────────────────────────────────────────
INSERT INTO public.categories (name, slug, description, color, icon, sort_order)
VALUES
  ('General',       'general',       'General knowledge and notes',       '#6366f1', '📝', 0),
  ('Personal',      'personal',      'Personal reflections and goals',     '#ec4899', '🙋', 1),
  ('Work',          'work',          'Professional tasks and projects',    '#f59e0b', '💼', 2),
  ('Learning',      'learning',      'Things to learn or study',           '#10b981', '📚', 3),
  ('Ideas',         'ideas',         'Creative ideas and brainstorming',   '#8b5cf6', '💡', 4),
  ('Projects',      'projects',      'Active projects and their context',  '#3b82f6', '🚀', 5),
  ('References',    'references',    'External references and bookmarks',  '#64748b', '🔗', 6),
  ('Code',          'code',          'Code snippets and technical notes',  '#06b6d4', '💻', 7),
  ('Conversations', 'conversations', 'Important conversation summaries',   '#84cc16', '💬', 8),
  ('Research',      'research',      'Research notes and findings',        '#f97316', '🔬', 9)
ON CONFLICT (slug) DO NOTHING;
