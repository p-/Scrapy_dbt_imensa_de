WITH source AS (
  SELECT *
  FROM {{source('imensa_scraper', 'items_raw')}}
)

SELECT
    id AS id,
    TRIM(mensa_name) AS mensa_name,
    TRIM(state) AS state,
    TRIM(meal_category) AS meal_category,
    TRIM(meal_name) AS meal_description,
    CASE
      WHEN price = 'Ausverkauft' THEN NULL
      ELSE to_number(REPLACE(REPLACE(TRIM(price),'€',''),',','.'), '99999.99')
    END AS price_in_euro,
    TRIM(price) as price,
   	CASE
		  WHEN price_per IS NULL THEN 'pro Portion'
		  ELSE TRIM(price_per)
	  END AS price_per,
    to_date(TRIM(last_time), 'DD.MM.YYYY') AS last_time_meal,
    substring (TRIM(meal_attributes) FROM '(?<=^)(.*?)(?=ZUSATZ|ALLERGEN|NÄHRWERT|$|ZULETZT)') AS meal_attribute_general,
    substring (TRIM(meal_attributes) FROM '(?<=ZUSATZ)(.*?)(?=ZUSATZ|ALLERGEN|NÄHRWERT|ZULETZT|$)') AS meal_attribute_additives,
    substring (TRIM(meal_attributes) FROM '(?<=ALLERGEN)(.*?)(?=ZUSATZ|NÄHRWERT|ZULETZT|$)') AS meal_attributes_allergens,
    substring (TRIM(meal_attributes) FROM '(?<=NÄHRWERT)(.*?)(?=ZUSATZ|NÄHRWERT|ALLERGEN|$)') AS meal_attributes_calories_macros,
    to_date(date_meal, 'DD.MM.YYYY') as date_meal,
    to_number(REPLACE(TRIM(stars_average),',','.'), '9.9') AS stars_average,
    to_number(REPLACE(TRIM(ratings_count),'.',''),'9999999999') AS ratings_count,
    to_number(REPLACE(TRIM(number_5_star_ratings),'%',''),'99') AS number_5_star_ratings_percent,
    to_number(REPLACE(TRIM(number_4_star_ratings),'%',''),'99') AS number_4_star_ratings_percent,
    to_number(REPLACE(TRIM(number_3_star_ratings),'%',''),'99') AS number_3_star_ratings_percent,
    to_number(REPLACE(TRIM(number_2_star_ratings),'%',''),'99') AS number_2_star_ratings_percent,
    to_number(REPLACE(TRIM(number_1_star_ratings),'%',''),'99') AS number_1_star_ratings_percent,
    CASE
      WHEN (street_and_nr ~ '\d') THEN substring (TRIM(street_and_nr) from '(.*) ')
      ELSE street_and_nr
    END AS streetname,
    CASE
      WHEN (street_and_nr ~ '\d') THEN reverse(split_part(reverse(TRIM(street_and_nr)), ' ', 1))
      ELSE NULL
    END AS house_number,
    split_part(TRIM(plz_and_city), ' ', 1) AS plz,
    split_part(TRIM(plz_and_city), ' ', 2) AS city,
    TRIM(unique_key) as unique_key,
    TRIM(operator) AS operator,
    day_minute_scraped AS timestamp_created,
    to_date(split_part(day_minute_scraped, ' ', 1), 'YYYY-MM-DD') as daily_date_created,
    CASE
      WHEN
        (TRIM(meal_category) ~ 'Info|Achtung|Information|Aktuelles|Kennzeichnungen|Kennzeichungen|Hinweis' AND price is NULL)
        OR meal_name ~ 'keine Ausgabe|Heute geschlossen|heute geschlossen|aktuell geschlossen|Aktuell geschlossen'
        THEN FALSE::BOOLEAN
      ELSE TRUE::BOOLEAN
    END AS is_meal,
    CASE
      WHEN meal_name ~ 'keine Ausgabe|Heute geschlossen|heute geschlossen|aktuell geschlossen|Aktuell geschlossen'
        THEN TRUE::BOOLEAN
      ELSE FALSE::BOOLEAN
    END AS is_closed






FROM
    source

