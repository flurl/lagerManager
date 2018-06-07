#V1195
#V0000

alter table config add column cfg_validTill datetime not null default '2099-12-31 23:59:59';

alter table config drop index cfg_key;

alter table config add unique key config_key_validTill_uq (cfg_key, cfg_validTill);
