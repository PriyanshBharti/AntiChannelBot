create table if not exists CHANNEL_LINKED_GROUP
(
    group_id    integer not null
        constraint CHANNEL_LINKED_GROUP_pk
            primary key,
    channel_id  int,
    create_time timestamp default current_timestamp,
    update_time integer   default (strftime('%s', 'now'))
);

create unique index if not exists CHANNEL_LINKED_GROUP_channel_id_uindex on CHANNEL_LINKED_GROUP (channel_id);
