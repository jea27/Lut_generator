PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS oauth_states (
  state_hash TEXT PRIMARY KEY,
  verifier_ciphertext TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  expires_at INTEGER NOT NULL,
  consumed_at INTEGER
);
CREATE INDEX IF NOT EXISTS oauth_states_expiry ON oauth_states(expires_at);

CREATE TABLE IF NOT EXISTS review_sessions (
  id_hash TEXT PRIMARY KEY,
  github_user_id INTEGER NOT NULL CHECK (github_user_id = 45896918),
  github_login TEXT NOT NULL CHECK (github_login = 'jea27'),
  access_token_ciphertext TEXT,
  refresh_token_ciphertext TEXT,
  access_expires_at INTEGER NOT NULL,
  refresh_expires_at INTEGER NOT NULL,
  created_at INTEGER NOT NULL,
  last_seen_at INTEGER NOT NULL,
  expires_at INTEGER NOT NULL,
  refresh_lease_id TEXT,
  refresh_lease_until INTEGER,
  revoked_at INTEGER
);
CREATE INDEX IF NOT EXISTS review_sessions_expiry ON review_sessions(expires_at);

CREATE TABLE IF NOT EXISTS review_submissions (
  payload_hash TEXT PRIMARY KEY,
  idempotency_hash TEXT NOT NULL UNIQUE,
  feature_id TEXT NOT NULL,
  issue_number INTEGER NOT NULL CHECK (issue_number > 0),
  revision TEXT NOT NULL,
  decision TEXT NOT NULL CHECK (decision IN ('approve', 'changes')),
  status TEXT NOT NULL CHECK (status IN ('reserved', 'sending', 'retryable', 'sent')),
  lease_id TEXT,
  lease_until INTEGER,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  comment_id INTEGER,
  comment_url TEXT
);
CREATE INDEX IF NOT EXISTS review_submissions_issue ON review_submissions(issue_number, created_at);

CREATE TABLE IF NOT EXISTS rate_limits (
  key_hash TEXT NOT NULL,
  bucket INTEGER NOT NULL,
  hit_count INTEGER NOT NULL CHECK (hit_count > 0),
  expires_at INTEGER NOT NULL,
  PRIMARY KEY (key_hash, bucket)
);
CREATE INDEX IF NOT EXISTS rate_limits_expiry ON rate_limits(expires_at);
