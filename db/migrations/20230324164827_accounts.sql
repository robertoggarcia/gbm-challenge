-- migrate:up
CREATE TABLE accounts
(
  id           integer generated always as identity PRIMARY KEY,
  cash         float,
  created_at   timestamp not null DEFAULT CURRENT_TIMESTAMP,
  updated_at   timestamp
);

-- migrate:down
DROP TABLE accounts;
