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

The documentation for the project on the dbt side can be generated using:

` dbt docs generate `

and served on a local website using:

` dbt docs serve `

There is a docker-compose.yml for the scrapy and postgres part of the project. It works with the right settings in pipelines.py, profiles.yml and docker-compose.yml, but the implementation of dbt as a container in this setup is a work in progress.

There is also the file imensa_dump, which can be used to recreate the final database.

Here is an interesting overview of where the different columns are scraped from the imensa.de pages:

![imensa_scraper_items](https://user-images.githubusercontent.com/69685614/195756234-666ca9bf-4693-4256-afa8-56b8048152aa.png)

Here ist the lineage graph for the dbt model transformation as documented in the dbt docs:

![image](https://user-images.githubusercontent.com/69685614/195765511-da410b69-0c56-40c6-80cd-f5733da1e1b1.png)

Here is some more documentation on a final table by dbt - what a great tool:

![image](https://user-images.githubusercontent.com/69685614/195765775-e49f6036-7dec-4fc1-81a9-06a08817611f.png)

