CREATE TABLE apex_live_ws (
    id bigserial primary key,
    name text not null,  -- This is the livetiming name
    ts timestamp not null default now(),
    frame text not null,
    processed timestamp
);

CREATE TABLE track (
    id bigserial primary key,
    name text not null,
    url text not null
);

CREATE TABLE session (
    id bigserial primary key,
    id_track bigint references track(id) on delete cascade,
    ts timestamp not null,
    grid text not null
);

CREATE TABLE session_pilots (
    id bigserial primary key,
    id_session bigint references session(id) on delete cascade,
    name text not null,
    "number" text
);

CREATE TABLE laps (
    id bigserial primary key,
    id_session bigint references session(id) on delete cascade,
    name text,
    "number" text,
    laptime interval not null
);


create index on session_pilots(id_session);
create index on session(id_track);
create index on laps(id_session, name);