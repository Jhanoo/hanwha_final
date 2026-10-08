-- DeskMate demo schema draft: PostgreSQL 17 + pgvector.
-- Apply only to a new/local demo database after reviewing docs/database.md.
-- Embedding dimensions must match the configured embedding model.

BEGIN;

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS conversations (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    closed_at timestamptz,
    status text NOT NULL DEFAULT 'open'
        CHECK (status IN ('open', 'resolved', 'escalated'))
);

CREATE TABLE IF NOT EXISTS messages (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    conversation_id uuid NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role text NOT NULL CHECK (role IN ('employee', 'assistant', 'system')),
    body text NOT NULL,
    category text,
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS messages_conversation_created_idx
    ON messages (conversation_id, created_at);

CREATE TABLE IF NOT EXISTS approvals (
    id uuid PRIMARY KEY,
    conversation_id uuid NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    draft_sha256 text NOT NULL CHECK (length(draft_sha256) = 64),
    status text NOT NULL CHECK (status IN ('pending', 'approved', 'rejected', 'consumed')),
    created_at timestamptz NOT NULL DEFAULT now(),
    approved_at timestamptz,
    UNIQUE (id, conversation_id)
);

CREATE TABLE IF NOT EXISTS tickets (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    conversation_id uuid NOT NULL REFERENCES conversations(id),
    approval_id uuid NOT NULL,
    title text NOT NULL CHECK (length(trim(title)) > 0),
    category text NOT NULL,
    priority text NOT NULL DEFAULT 'normal'
        CHECK (priority IN ('low', 'normal', 'high', 'critical')),
    status text NOT NULL DEFAULT 'open'
        CHECK (status IN ('open', 'in_progress', 'resolved')),
    summary jsonb NOT NULL DEFAULT '{}'::jsonb,
    idempotency_key text NOT NULL UNIQUE,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT tickets_approval_conversation_fk
        FOREIGN KEY (approval_id, conversation_id)
        REFERENCES approvals(id, conversation_id)
);
CREATE INDEX IF NOT EXISTS tickets_status_updated_idx ON tickets (status, updated_at DESC);
CREATE INDEX IF NOT EXISTS tickets_conversation_idx ON tickets (conversation_id);

CREATE TABLE IF NOT EXISTS ticket_events (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ticket_id bigint NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    previous_status text,
    new_status text NOT NULL CHECK (new_status IN ('open', 'in_progress', 'resolved')),
    actor text NOT NULL CHECK (actor IN ('employee', 'agent', 'it_operator', 'system')),
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ticket_events_ticket_created_idx
    ON ticket_events (ticket_id, created_at);

CREATE TABLE IF NOT EXISTS knowledge_documents (
    id text PRIMARY KEY,
    title text NOT NULL,
    source_uri text NOT NULL,
    version text NOT NULL,
    category text NOT NULL,
    active boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_uri, version)
);

CREATE TABLE IF NOT EXISTS knowledge_chunks (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    document_id text NOT NULL REFERENCES knowledge_documents(id) ON DELETE CASCADE,
    chunk_index integer NOT NULL CHECK (chunk_index >= 0),
    chunk_text text NOT NULL CHECK (length(trim(chunk_text)) > 0),
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    embedding vector(1536) NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (document_id, chunk_index)
);
CREATE INDEX IF NOT EXISTS knowledge_chunks_document_idx ON knowledge_chunks (document_id);
CREATE INDEX IF NOT EXISTS knowledge_chunks_metadata_idx ON knowledge_chunks USING gin (metadata);
CREATE INDEX IF NOT EXISTS knowledge_chunks_embedding_hnsw_idx
    ON knowledge_chunks USING hnsw (embedding vector_cosine_ops);

COMMIT;
