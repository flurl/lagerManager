#V1199
#V0000

alter table dir_typen add column dit_beginn_ditid int unsigned;
alter table dir_typen add foreign key dir_typen_beginn_typ_fk (dit_beginn_ditid) references dir_typen(dit_id);
alter table dir_typen add column dit_ende_ditid int unsigned;
alter table dir_typen add foreign key dir_typen_beginn_typ_fk (dit_ende_ditid) references dir_typen(dit_id);



