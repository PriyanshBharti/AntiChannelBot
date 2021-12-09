create table if not exists BANNED_CHANNELS
(
    id          integer
        constraint BANNED_CHANNELS_pk
            primary key autoincrement,
    group_id    integer not null,
    channel_id  integer not null,
    create_time timestamp default current_timestamp,
    whitelisted boolean   default false
);
