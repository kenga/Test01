create table clickstream
(
    userId   varchar(25) charset utf8               not null,
    time     datetime                               not null,
    action   enum ('FIRST_INSTALL', 'LIKE_ARTICLE') not null,
    objectId varchar(25) charset utf8               null
);

create table articles
(
    id varchar(25) not null,
    title nvarchar(200) not null,
    created_by datetime not null,
    updated_by datetime not null,
    constraint articles_pk
        primary key (id)
);