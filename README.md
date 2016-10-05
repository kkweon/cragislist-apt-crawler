# Craigslist Apartment Crawler
crawl apartment and update the database.
It also finds the closest Caltrain station and returns its distance.

targetsite: https://sfbay.craigslist.org/search/apa

# Requirements
1. scrapy
2. python3

# File Description
- README.md (current file)
- result.csv
    - result file
- craigslit_apt/
    - scrapy project

# How to use

```bash
scrapy crawl cl # run crawler
(source) mongo2csv # from mongo to result.csv
```

