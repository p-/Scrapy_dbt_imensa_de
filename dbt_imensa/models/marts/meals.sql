{{ config(materialized='table') }}

WITH source AS (
  SELECT *
  FROM {{ref('create_foreign_keys')}}
)

SELECT
    id,
    meal_category,
    meal_description,
    price_in_euro,
    price_per,
    last_time_meal,
    meal_attribute_general,
    meal_attribute_additives,
    meal_attributes_allergens,
    meal_attributes_calories_macros,
    date_meal,
    timestamp_created,
    mensa_id,
    rating_mensa_id

FROM source
WHERE source.is_meal = TRUE


