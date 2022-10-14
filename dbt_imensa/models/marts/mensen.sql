{{ config(materialized='table') }}

WITH source AS (
  SELECT *
  FROM {{ref('create_foreign_keys')}}
)

SELECT
  {{ dbt_utils.surrogate_key(
      ['mensa_name',
      'city',
      'streetname']
  )
  }} AS id,
  mensa_name,
  city,
  streetname,
  MAX(state) As state,
  MAX(house_number) AS house_number,
  MAX(plz) AS plz,
  MAX(operator) AS operator,
  MAX(timestamp_created) AS max_timestamp_created
FROM
  source
GROUP BY
  mensa_name, city, streetname
