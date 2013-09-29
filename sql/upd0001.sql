
create table dir_typen (
	dit_id int unsigned auto_increment primary key not null,
	dit_bez varchar(255) not null,
	dit_kbez varchar(5) not null,
	unique key (dit_kbez)
)ENGINE=INNODB;

create table dienstnehmer_ereignisse (
	dir_id int unsigned auto_increment primary key not null,
	dir_dinid int unsigned not null,
	dir_datum datetime not null,
	dir_ditid int unsigned not null,
	foreign key dienstnehmer_ereignisse_typen_fk (dir_ditid) references dir_typen(dit_id),
	foreign key dienstnehmer_ereignisse_dienstnehmer_fk (dir_dinid) references dienstnehmer (din_id)
) ENGINE=INNODB;


insert into dir_typen (dit_bez, dit_kbez) values 
('Eintritt', 'EIN'), 
('Austritt', 'AUS'), 
('Urlaubsbeginn', 'URBEG'), 
('Urlaubsende', 'UREND'), 
('Krankenstandsbeginn', 'KSBEG'), 
('Krankenstandsende', 'KSEND');

-- appending this comment for testing the pre-commit hook
