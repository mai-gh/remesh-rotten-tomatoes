# Mai Atwell  ::  rt.py 

## CLI tool get the "best movie match" from rottentomatoes.com

### Usage:

`./rt.py search query`

the search query can be formatted probably any way you like, the only
requirement is that it must contain a letter or a number. keep in mind rotten tomatoes names are pretty specific so if you search for:

`./rt.py godfather 2` 

it probably will not work, so try instead:

`./rt.py godfather ii`

### Data Retrieval:

The rottentomatoes.com data api was revealed by watching the network tab in developer tools in my web browser after clicking on the next button after making a search

[https://www.rottentomatoes.com/napi/search/all?after=MQ%3D%3D&searchQuery=star+wars&type=movie&f=null](https://www.rottentomatoes.com/napi/search/all?after=MQ%3D%3D&searchQuery=star+wars&type=movie&f=null)

#### API Paramenters:
`after=MQ%3D%3D`

`searchQuery=star+wars`

`type=movie`

`f=null`

the only ones we care about are `after` and `searchQuery`

`after` can simply be empty e.g. ` 'after=' `

if you look at ` json_data -> movies -> pageInfo -> endCursor ` you can get what you need to put in for ` after ` to get the next page

additionally there is ` json_data -> movies -> pageInfo -> hasNextPage ` which I used to check when to break out of retrieving pages (if downloading all pages in a query)

`searchQuery` should be self explanitory

**All values given to parameters must be url encoded**

### Extra Features:

`./rt.py --help`


```
usage: rt.py [-h] [--load-json-file JSON_LOAD_FILE_PATH]
             [--save-json-file JSON_SAVE_FILE_PATH]
             [--max-dl-pages MAX_DL_PAGES]
             search_query_string [search_query_string ...]

positional arguments:
  search_query_string   search query

options:
  -h, --help            show this help message and exit
  --load-json-file JSON_LOAD_FILE_PATH
                        provide a json file instead of querying the api
  --save-json-file JSON_SAVE_FILE_PATH
                        save a json file after querying the api
  --max-dl-pages MAX_DL_PAGES
                        specify number of pages when querying the api. if not
                        specified, defaults to 10. provide `ALL` to download
                        all pages

```


### Functions: 

`def pretty_print(data):`

`def get_json_from_api(srch_str, max_pages = None):` 

`def filter_movies(test_string, movies_list):`

`def pick_best_movie(movies_list):`

`def format_result(srch_str, movie):`

`def main_app():`

### Testing:

Test with `pytest -v`

Tests defined in `test_rt.py`

##### Helpers:

`def movie_builder(name, critval, usrval, year):` build mock data to test with

##### Test Coverage:

`def test_api_results_length():`

`def test_filter_movies_names():`

`def test_filter_movies_critic_score():`

`def test_filter_movies_audience_score():`

`def test_filter_movies_release_year():`

`def test_pick_best_movie_critic():`

`def test_pick_best_movie_audience():`

`def test_pick_best_movie_year():`

`def test_pick_best_movie_year():`


