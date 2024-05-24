create schema if not exists dbo;

create table if not exists dbo.users_template (
    hp int4 not null,
    mana int4 not null,
    balance int4 not null,
    experiance int4 not null,
    l_atck int4 not null,
    u_atck int4 not null,
    default_location text not null,
    start_dttm timestamp not null,
    end_dttm timestamp not null
);

insert into dbo.users_template (hp, mana, balance, experiance, l_atck, u_atck, default_location, start_dttm, end_dttm)
values
    (200, 100, 0, 100, 25, 50, '4c901bcce6dc22e1a97cde2e91c756c9', '2000-01-01'::timestamp, '2050-01-01'::timestamp);


create table if not exists dbo.states (
    id int2 not null,
    descr text not null,
    start_dttm timestamp not null,
    end_dttm timestamp not null
);

insert into dbo.states (id, descr, start_dttm, end_dttm)
values
    (0::int2, 'Нужно авторизоваться', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    (1::int2, 'Свободная минутка, можно переместиться на другую локацию или улучшить статы', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    (2::int2, 'Нужно принять или отклонить сражение', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    (3::int2, 'Нужно сражаться или сбегать', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    (4::int2, 'Нужно забрать или отказаться от награды', '2000-01-01'::timestamp, '2050-01-01'::timestamp);

create table if not exists dbo.commands (
    id text not null,
    descr text not null,
    start_dttm timestamp not null,
    end_dttm timestamp not null
);
    
insert into dbo.commands (id, descr, start_dttm, end_dttm)
values
    ('/new', 'Создание нового игрока', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/log', 'Авторизация в игровой аккаунт', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/logout', 'Выйти из аккаунта', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/chname', 'Поменять имя пользователя', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/chpass', 'Поменять пароль', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/move', 'Идти далее', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/moveto', 'Переместиться в другую локацию', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/abandon', 'Отклонить сражение', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/accept', 'Принять сражение', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/attack', 'Атаковать', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/take', 'Взять награду', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/skip', 'Пропустить награду', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    -- ('/cast', 'Использовать заклинание', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/up_atck', 'Увеличить атаку', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/up_hp', 'Увеличть здоровье', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/up_mana', 'Увеличить ману', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/verbose', 'Отобразить текущую информацию о игровом процессе', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/help', 'Отобразить подсказку', '2000-01-01'::timestamp, '2050-01-01'::timestamp);

create table if not exists dbo.satt_commands__attributes(
    id text not null,
    attribute text not null,
    descr text not null,
    valid_from timestamp not null,
    valid_to timestamp not null
);

insert into dbo.satt_commands__attributes (id, attribute, descr, valid_from, valid_to)
values
    ('/new', '--username', 'Имя пользователя', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/new', '--password', 'Пароль', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/log', '--username', 'Имя пользователя', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/log', '--password', 'Пароль', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/chname', '--new', 'Новое имя', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    -- ('/cast', '--spell', 'Наименование заклинания', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/chpass', '--old', 'Старый пароль', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/chpass', '--new', 'Новый пароль', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/moveto', '--location', 'Наименование локации', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/up_atck', '--which', 'Какую атаку', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/up_atck', '--value', 'Количество очков', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/up_hp', '--value', 'Количество очков', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('/up_mana', '--value', 'Количество очков', '2000-01-01'::timestamp, '2050-01-01'::timestamp);


create table if not exists dbo.users (
    id text not null,
    start_dttm timestamp not null,
    end_dttm timestamp null
);

create table if not exists dbo.satt_users__name (
    user_id text not null,
    name text not null,
    valid_from timestamp not null,
    valid_to timestamp not null
);

create table if not exists dbo.satt_users__password (
    user_id text not null,
    password text not null,
    valid_from timestamp not null,
    valid_to timestamp not null
);

create table if not exists dbo.satt_users__base_stats (
    user_id text not null,
    hp int4 not null,
    mana int4 not null,
    dttm_created timestamp not null,
    dttm_updated timestamp not null
);

create table if not exists dbo.satt_users__attck (
    user_id text not null,
    l_atck int4 not null,
    u_atck int4 not null,
    dttm_created timestamp not null,
    dttm_updated timestamp not null
);

create table if not exists dbo.satt_users__adv_stats (
    user_id text not null,
    balance int4 not null,
    experiance int4 not null,
    dttm_created timestamp not null,
    dttm_updated timestamp not null
);

create table if not exists dbo.satt_users__current_state (
    user_id text not null,
    state int2 not null,
    dttm_created timestamp not null,
    dttm_updated timestamp not null    
);

create table if not exists dbo.base_enemies (
    id text not null,
    name text not null,
    hp int4 not null,
    l_atck int4 not null,
    u_atck int4 not null,
    start_dttm timestamp not null,
    end_dttm timestamp not null
);

insert into dbo.base_enemies (id, name, hp, l_atck, u_atck, start_dttm, end_dttm)
values
    ('979d472a84804b9f647bc185a877a8b5', 'Декан', 1000, 50, 150, '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('7815a62bc723a1c2884807eefd6640c5', 'Студент ММФ', 100, 5, 35, '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('b0c7792a583d1cf39737956766ca46c2', 'Студент ФФ', 80, 25, 35, '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('3ba01956e2bde70050320757a7d1800d', 'Студент ГГФ', 55, 0, 200, '2000-01-01'::timestamp, '2050-01-01'::timestamp);

create table if not exists dbo.link_enemies__base_enemies (
    base_id text not null,
    enemy_id text not null,
    dttm timestamp not null,
    is_actual boolean not null
);

create table if not exists dbo.enemies (
    id text not null,
    dttm_created timestamp not null,
    dttm_updated timestamp not null,
    hp int4 not null,
    l_atck int4 not null,
    u_atck int4 not null,
    is_dead boolean not null
);

create table if not exists dbo.link_enemies__users (
    enemy_id text not null,
    user_id text not null,
    dttm timestamp not null,
    is_actual boolean not null
);

create table if not exists dbo.locations (
    id text not null,
    name text not null,
    start_dttm timestamp not null,
    end_dttm timestamp not null
);

create table if not exists dbo.link_users__locations (
    loc_id text not null,
    user_id text not null,
    dttm timestamp not null,
    is_actual boolean not null
);

create table if not exists dbo.link_locations__base_enemies (
    loc_id text not null,
    base_id text not null,
    dttm timestamp not null,
    chance_ratio float not null,
    is_actual boolean not null
);

insert into dbo.locations (id, name, start_dttm, end_dttm)
values
    ('4c901bcce6dc22e1a97cde2e91c756c9', 'Новый корпус', '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('07c79fbfdcd18aaddb1287aa0ee30c6d', 'Старый корпус', '2000-01-01'::timestamp, '2050-01-01'::timestamp);

insert into dbo.link_locations__base_enemies (loc_id, base_id, dttm, chance_ratio, is_actual)
values
    ('4c901bcce6dc22e1a97cde2e91c756c9','979d472a84804b9f647bc185a877a8b5','2000-01-01'::timestamp, 0.05, 1::boolean),
    ('4c901bcce6dc22e1a97cde2e91c756c9','7815a62bc723a1c2884807eefd6640c5','2000-01-01'::timestamp, 0.45, 1::boolean),
    ('4c901bcce6dc22e1a97cde2e91c756c9','b0c7792a583d1cf39737956766ca46c2','2000-01-01'::timestamp, 0.15, 1::boolean),
    ('4c901bcce6dc22e1a97cde2e91c756c9','3ba01956e2bde70050320757a7d1800d','2000-01-01'::timestamp, 0.35, 1::boolean),
    ('07c79fbfdcd18aaddb1287aa0ee30c6d','979d472a84804b9f647bc185a877a8b5','2000-01-01'::timestamp, 0.01, 1::boolean),
    ('07c79fbfdcd18aaddb1287aa0ee30c6d','7815a62bc723a1c2884807eefd6640c5','2000-01-01'::timestamp, 0.19, 1::boolean),
    ('07c79fbfdcd18aaddb1287aa0ee30c6d','b0c7792a583d1cf39737956766ca46c2','2000-01-01'::timestamp, 0.55, 1::boolean),
    ('07c79fbfdcd18aaddb1287aa0ee30c6d','3ba01956e2bde70050320757a7d1800d','2000-01-01'::timestamp, 0.25, 1::boolean);

create table if not exists dbo.base_greeds (
    id text not null,
    name text not null,
    update_identifier text not null,
    value int2 not null,
    start_dttm timestamp not null,
    end_dttm timestamp not null
);

insert into dbo.base_greeds (id, name, update_identifier, value, start_dttm, end_dttm)
values
    ('2cf9df2d1e20cde96adcc795862504d3', 'Сосиска в тесте', 'hp', 55::int2, '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('b447c27a00e3a348881b0030177000cd', 'Ашкудишка', 'mana', 20::int2, '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('52720b6799d1e573ec52482ca8c800b6', 'Синий винстон', 'l_attack', 5::int2, '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('0597f5edf0fe359c17cc94446a0da3fa', 'Одобрительный взгляд препода', 'u_attack', 15::int2, '2000-01-01'::timestamp, '2050-01-01'::timestamp),
    ('46e4a886177589186a2a0d5af290ccf2', 'Билеты к экзамену', 'experiance', 30::int2, '2000-01-01'::timestamp, '2050-01-01'::timestamp);

create table if not exists dbo.greeds (
    id text not null,
    dttm_created timestamp not null,
    dttm_updated timestamp not null,
    update_identifier text not null,
    value int2 not null
);

create table if not exists dbo.link_greeds__base_greeds (
    base_id text not null,
    greed_id text not null,
    dttm timestamp not null,
    is_actual boolean not null
);

create table if not exists dbo.link_locations__base_greeds (
    loc_id text not null,
    base_id text not null,
    dttm timestamp not null,
    chance_ratio float not null,
    is_actual boolean not null
);


insert into dbo.link_locations__base_greeds (loc_id, base_id, dttm, chance_ratio, is_actual)
values
    ('4c901bcce6dc22e1a97cde2e91c756c9','2cf9df2d1e20cde96adcc795862504d3','2000-01-01'::timestamp, 0.35, 1::boolean),
    ('4c901bcce6dc22e1a97cde2e91c756c9','b447c27a00e3a348881b0030177000cd','2000-01-01'::timestamp, 0.25, 1::boolean),
    ('4c901bcce6dc22e1a97cde2e91c756c9','52720b6799d1e573ec52482ca8c800b6','2000-01-01'::timestamp, 0.05, 1::boolean),
    ('4c901bcce6dc22e1a97cde2e91c756c9','0597f5edf0fe359c17cc94446a0da3fa','2000-01-01'::timestamp, 0.05, 1::boolean),
    ('4c901bcce6dc22e1a97cde2e91c756c9','46e4a886177589186a2a0d5af290ccf2','2000-01-01'::timestamp, 0.30, 1::boolean),
    ('07c79fbfdcd18aaddb1287aa0ee30c6d','2cf9df2d1e20cde96adcc795862504d3','2000-01-01'::timestamp, 0.45, 1::boolean),
    ('07c79fbfdcd18aaddb1287aa0ee30c6d','b447c27a00e3a348881b0030177000cd','2000-01-01'::timestamp, 0.05, 1::boolean),
    ('07c79fbfdcd18aaddb1287aa0ee30c6d','52720b6799d1e573ec52482ca8c800b6','2000-01-01'::timestamp, 0.15, 1::boolean),
    ('07c79fbfdcd18aaddb1287aa0ee30c6d','0597f5edf0fe359c17cc94446a0da3fa','2000-01-01'::timestamp, 0.1, 1::boolean),
    ('07c79fbfdcd18aaddb1287aa0ee30c6d','46e4a886177589186a2a0d5af290ccf2','2000-01-01'::timestamp, 0.25, 1::boolean);


create table if not exists dbo.link_greeds__users (
    greed_id text not null,
    user_id text not null,
    dttm timestamp not null,
    is_actual boolean not null
);

