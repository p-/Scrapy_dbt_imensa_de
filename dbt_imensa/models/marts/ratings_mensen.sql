{{ config(materialized='table') }}


WITH source AS (
  SELECT *
  FROM {{ref('create_foreign_keys')}}
)

SELECT
   {{ dbt_utils.surrogate_key(
      ['mensa_name',
      'city',
      'streetname',
      'daily_date_created']
        )
        }} AS id,
  mensa_name,
  city,
  mensa_id,
  streetname,
  MAX(stars_average) AS stars_average,
  MAX(ratings_count) AS ratings_count,
  MAX(number_5_star_ratings_percent) AS number_5_star_ratings_percent,
  MAX(number_4_star_ratings_percent) AS number_4_star_ratings_percent,
  MAX(number_3_star_ratings_percent) AS number_3_star_ratings_percent,
  MAX(number_2_star_ratings_percent) AS number_2_star_ratings_percent,
  MAX(number_1_star_ratings_percent) AS number_1_star_ratings_percent,
  daily_date_created

FROM
  source
GROUP BY
  mensa_id, daily_date_created,city, streetname, mensa_name
