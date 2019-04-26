

create or replace view dienstnehmer_view as select *, concat(din_nachname, ' ', din_vorname) name from dienstnehmer;
