#V1023
alter table dienste_vorlagen add column div_dauer int unsigned not null;

update dienste_vorlagen
set div_dauer = if((div_beginn <= div_ende), unix_timestamp(date_add('1970-01-01', INTERVAL time_to_sec(div_ende) second))-unix_timestamp(date_add('1970-01-01', INTERVAL time_to_sec(div_beginn) second)), unix_timestamp(date_add('1970-01-02', INTERVAL time_to_sec(div_ende) second))-unix_timestamp(date_add('1970-01-01', INTERVAL time_to_sec(div_beginn) second)));

alter table dienste_vorlagen drop column div_ende;

