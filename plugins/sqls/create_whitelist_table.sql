create table if not exists WHITELISTED_CHANNELS
(
    id          integer
        constraint WHITELISTED_CHANNELS_pk
            primary key autoincrement,
    group_id    integer not null,
    channel_id  integer not null,
    create_time timestamp default current_timestamp
);
