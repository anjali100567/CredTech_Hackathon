create table if not exists events (
    id bigserial primary key,
    issuer_id int reference issuers(id),
    ts timestamptz not null,
    sourece text,
    headline text,
    sentiment_tb double precision,
    sentiment_hf double precision,
    event_type text,
    impact double precision
)