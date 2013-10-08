#V1022


create table gehaelter (
	geh_id int unsigned auto_increment primary key not null,
	geh_kbez varchar(10) not null,
	geh_bez varchar(255),
	unique key (geh_kbez)
) ENGINE=INNODB;


create table loehne (
	loh_id int unsigned not null auto_increment primary key,
	loh_summe float not null,
	loh_gehid int unsigned not null,
	loh_validTill datetime not null default '2099-12-31 23:59:59',
	foreign key loehne_gehalt_fk (loh_gehid) references gehaelter (geh_id),
	unique key (loh_gehid, loh_validTill)
) ENGINE=INNODB;

alter table dienstnehmer add column din_gehid int unsigned not null;

delimiter //

CREATE PROCEDURE UpdateGehaelter()
BEGIN

DECLARE bez varchar(10);
DECLARE lohnges float;
DECLARE stdsatz float;
DECLARE done INT default false;
DECLARE gehId INT;

declare cur1 cursor for select distinct din_stundensatz, din_stundensatz*173, concat('GEH',din_stundensatz*173) from dienstnehmer;

#declare handle 
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

#open cursor
OPEN cur1;

#starts the loop
the_loop: LOOP
  fetch cur1 into stdsatz, lohnges, bez;
  IF done THEN
    LEAVE the_loop;
  END IF;
  
  insert into gehaelter (geh_kbez) values (bez);
  
  set gehId := LAST_INSERT_ID();
  
  insert into loehne (loh_summe, loh_gehid) select lohnges, gehId;
  
  update dienstnehmer set din_gehid = gehId where din_stundensatz = stdsatz;
  
END LOOP the_loop;

CLOSE cur1;

END;
//

delimiter ;

call UpdateGehaelter;
  
alter table dienstnehmer add foreign key dienstnehmer_gehalt_fk (din_gehid) references gehaelter (geh_id);
alter table dienstnehmer drop column din_stundensatz;

drop procedure UpdateGehaelter;



