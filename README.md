# Scrapy_dbt_imensa.de

This project scrapes imensa.de using scrapy, loads the scraped data into a Postgresql database and transforms the raw data in postgres using dbt.

It needs a PostgreSQL database setup and running on the local system with a database setup as defined in ./scrapy_imensa/scraper_imensa/pipelines.py and in the profiles.yml file of dbt.

After installing dbt, profiles.yml can be found using

` dbt debug --config-dir `

The scraper can be started as follows (executed in the scrapy project folder ./scrapy_imensa): 

` scrapy crawl imensa `

The dbt models can be started as follows (executed in the dbt project folder ./dbt_imensa):

` dbt run ` 

The dbt test suite can be started as follow (executed in the dbt project folder ./dbt_imensa):

` dbt test `

There is a docker-compose.yml for the scrapy and postgres part of the project. It works with the right settings in pipelines.py, profiles.yml and docker-compose.yml, but it is a work in progress.



Here is an interesting overview of where the different columns are scraped from the imensa.de pages:

![imensa_scraper_items](https://user-images.githubusercontent.com/69685614/195756234-666ca9bf-4693-4256-afa8-56b8048152aa.png)

The 
