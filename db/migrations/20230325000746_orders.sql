-- migrate:up
CREATE TABLE orders
(
  id           integer generated always as identity PRIMARY KEY,
  timestamp    integer,
  operation    text,
  issuer_name  text,
  total_shares integer,
  share_price  float,
  account_id   integer,
  created_at   timestamp not null DEFAULT CURRENT_TIMESTAMP,
  updated_at   timestamp
);

-- migrate:down
DROP TABLE orders;
