DROP FUNCTION IF EXISTS getCocktailArticleIds;
DELIMITER //
CREATE FUNCTION getCocktailArticleIds(
					IN articleId int unsigned, 
					IN periodId int unsigned)
returns varchar(65535)
BEGIN
	declare artBez varchar(255);
	declare artIdList varchar(65535);
	
	select artikel_bezeichnung
	into artBez
	from artikel_basis
	where 1=1
	and artikel_id = articleId
	and artikel_periode = periodId;
	
	select group_concat(artikel_id)
	into artIdList
	from artikel_basis
	where 1=1
	and replace(replace(artikel_bezeichnung, 'Cocktail1-', ''), 'Cocktail2-', '') = replace(replace(artBez, 'Cocktail1-', ''), 'Cocktail2-', '')
	and artikel_periode = periodId;
	
	return(artIdList);
	
END //
DELIMITER ;