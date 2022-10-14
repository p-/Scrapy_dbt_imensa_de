WITH source AS (
  SELECT *
  FROM {{ref('data_cleaning')}}
)

, mensa_id AS (
    SELECT
        {{ dbt_utils.surrogate_key(
        ['mensa_name',
        'city',
        'streetname']
        )
        }} AS id,
        mensa_name,
        city,
        streetname
    FROM
        source
    GROUP BY
        mensa_name, city, streetname
)

, rating_mensa_id AS (
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
        streetname,
        daily_date_created
    FROM
        source
    GROUP BY
        mensa_name, daily_date_created, city, streetname
)

SELECT
    source.*,
    mensa_id.id AS mensa_id,
    rating_mensa_id.id AS rating_mensa_id

FROM
    source
        LEFT JOIN mensa_id
            ON (mensa_id.mensa_name = source.mensa_name OR (mensa_id.mensa_name IS NULL AND source.mensa_name IS NULL))
            AND (mensa_id.city = source.city OR (mensa_id.city IS NULL AND source.city IS NULL))
            AND (mensa_id.streetname = source.streetname OR (mensa_id.streetname IS NULL AND source.streetname IS NULL))
        LEFT JOIN rating_mensa_id
            ON (source.mensa_name = rating_mensa_id.mensa_name OR (rating_mensa_id.mensa_name IS NULL AND source.mensa_name IS NULL))
            AND (source.daily_date_created = rating_mensa_id.daily_date_created OR (rating_mensa_id.daily_date_created IS NULL AND source.daily_date_created IS NULL))
            AND (source.city = rating_mensa_id.city OR (rating_mensa_id.city IS NULL AND source.city IS NULL))
            AND (source.streetname = rating_mensa_id.streetname OR (rating_mensa_id.streetname IS NULL AND source.streetname IS NULL))


-- mensa_id and rating_mensa_id should both be NOT NULL