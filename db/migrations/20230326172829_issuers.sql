-- migrate:up
CREATE TABLE issuers
(
  id           integer generated always as identity PRIMARY KEY,
  issuer_name  text,
  total_shares integer,
  share_price  float,
  account_id   integer,
  created_at   timestamp not null DEFAULT CURRENT_TIMESTAMP,
  updated_at   timestamp
);

-- migrate:down
DROP TABLE issuers;
