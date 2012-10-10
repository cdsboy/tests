begin;
  create table shows (
    show_id serial primary key,
    show_name text unique not null
  );

  create table genres (
    genre_id serial primary key,
    genre_name text unique not null
  );

  create table demographics (
    demo_id serial primary key,
    demo_name text unique not null
  );

  create table entries (
    entry_id serial primary key,
    sex text not null,
    age text not null,
    show_id int references shows(show_id) not null,
    demo_id int references demographics(demo_id) not null,
    fav_genre int references genres(genre_id) not null,
    least_genre int references genres(genre_id) not null
  );

  create view show_count as
    select show.show_name, count(entry.entry_id)
    from entries entry, shows show where entry.show_id = show.show_id
    group by show.show_name;
commit;
