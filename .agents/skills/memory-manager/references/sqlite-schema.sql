-- Core memory index table
CREATE TABLE IF NOT EXISTS memories (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL CHECK (type IN ('episode', 'procedure', 'insight')),
  status TEXT NOT NULL,
  title TEXT NOT NULL,
  path TEXT NOT NULL,
  summary TEXT,
  project TEXT,
  task_type TEXT,
  tags TEXT, -- JSON array string
  error_signature TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  last_used_at TEXT,
  use_count INTEGER NOT NULL DEFAULT 0,
  success_count INTEGER NOT NULL DEFAULT 0,
  confidence REAL,
  human_verified INTEGER NOT NULL DEFAULT 0,
  shared INTEGER NOT NULL DEFAULT 0,
  source_run_id TEXT
);

CREATE INDEX IF NOT EXISTS idx_memories_type_status ON memories(type, status);
CREATE INDEX IF NOT EXISTS idx_memories_project_task ON memories(project, task_type);
CREATE INDEX IF NOT EXISTS idx_memories_error_signature ON memories(error_signature);
CREATE INDEX IF NOT EXISTS idx_memories_last_used ON memories(last_used_at);

-- Relation table for evidence and derivation links
CREATE TABLE IF NOT EXISTS memory_links (
  from_id TEXT NOT NULL,
  to_id TEXT NOT NULL,
  relation_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  PRIMARY KEY (from_id, to_id, relation_type),
  FOREIGN KEY (from_id) REFERENCES memories(id),
  FOREIGN KEY (to_id) REFERENCES memories(id)
);

CREATE INDEX IF NOT EXISTS idx_memory_links_to_id ON memory_links(to_id);

-- Full-text search index (v0)
CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
  id UNINDEXED,
  title,
  summary,
  tags,
  error_signature,
  content='',
  tokenize='unicode61'
);
