drop table if exists transactions;
create table transactions (
	id integer primary key autoincrement,
	description text not null,
	withdrawal int not null,
	deposit int not null,
	other_account_id int not null
);

drop table if exists accounts;
create table accounts (
	id integer primary key autoincrement,
	title text not null,
	account_type_id int not null
);

drop table if exists account_types;
create table account_types (
	id integer primary key autoincrement,
	title text not null
);
