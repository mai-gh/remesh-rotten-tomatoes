#!/usr/bin/env python3


import urllib.request
import urllib.parse
import json
import math


def pretty_print(data):
    print(json.dumps(data, indent=4, sort_keys=True))


def get_json_from_api(srch_str, max_pages=None):
    m_list = []
    parsed_search_str = urllib.parse.quote_plus(srch_str)
    after = ""
    has_next_page = True
    current_page = 0
    total_pages = "???"

    while has_next_page:
        if not max_pages or current_page < max_pages:
            current_page += 1
        else:
            break
        page_info_str = (
            "(Current Page: " + str(current_page) + " / " + str(total_pages) + ")"
        )
        print(
            "    Searching for movie with string filter",
            "'" + srch_str + "'",
            page_info_str,
            "    ",
            end="\r",
        )
        url_str = "https://www.rottentomatoes.com/napi/search/all?after={}&searchQuery={}&type=movie&f=null".format(
            after, parsed_search_str
        )
        with urllib.request.urlopen(url_str) as url:
            data = json.loads(url.read().decode())
            m_list += data["movie"]["items"]
            total_pages = math.ceil(int(data["movie"]["count"]) / 10)
            if data["movie"]["pageInfo"]["hasNextPage"] == "true":
                after = urllib.parse.quote_plus(data["movie"]["pageInfo"]["endCursor"])
            else:
                has_next_page = False

    print()
    return m_list


def filter_movies(test_string, movies_list):

    new_movies_list = []

    for movie in movies_list:

        # filter out instances where name does not contain ALL of query words
        if all(
            s in movie["name"].lower().replace(" ", "")
            for s in test_string.lower().split()
        ):

            # filter out instances with no critic score
            if ("value" in movie["criticsScore"]) and (movie["criticsScore"]["value"]):

                # filter out instances with no audience score
                if ("score" in movie["audienceScore"]) and (
                    movie["audienceScore"]["score"]
                ):

                    # filter out instances with no release year
                    if movie["releaseYear"]:
                        new_movies_list.append(movie)

    return new_movies_list


def pick_best_movie(movies_list):

    # sort by highest critic score, then filter out instances less than the highest critic scores
    movies_list.sort(key=lambda m: m["criticsScore"]["value"], reverse=True)

    # filter out everything except highest critic scores
    _hcs = int(movies_list[0]["criticsScore"]["value"])
    _hcs_list = list(
        filter(lambda m: (int(m["criticsScore"]["value"]) >= _hcs), movies_list)
    )

    # sort by highest audience score, then filter out instances less than the highest audience scores
    _hcs_list.sort(key=lambda m: int(m["audienceScore"]["score"]), reverse=True)
    _has = int(_hcs_list[0]["audienceScore"]["score"])
    _has_list = list(
        filter(lambda m: (int(m["audienceScore"]["score"]) >= _has), _hcs_list)
    )

    # sort by earliest release year, then filter out instances later than the earliest release year
    _has_list.sort(key=lambda m: int(m["releaseYear"]))
    _erl = int(_has_list[0]["releaseYear"])
    _erl_list = list(filter(lambda m: (int(m["releaseYear"]) <= _erl), _has_list))

    return _erl_list


def format_result(srch_str, movie):
    movie_info_str = ""
    movie_info_str += "The best match for movie search string '" + srch_str + "'" + "\n"
    movie_info_str += "Title: " + movie["name"].upper() + "\n"
    movie_info_str += "Release Year: " + movie["releaseYear"] + "\n"
    movie_info_str += (
        "Critic Score: " + str(movie["criticsScore"]["value"]) + "%" + "\n"
    )
    movie_info_str += "User Score: " + str(movie["audienceScore"]["score"]) + "%" + "\n"
    movie_info_str += "URL: " + movie["url"]
    return movie_info_str


def main_app():

    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "strings",
        metavar="search_query_string",
        type=str,
        #nargs="+",
        nargs=argparse.REMAINDER,
        help="search query",
    )
    parser.add_argument(
        "--load-json-file",
        dest="json_load_file_path",
        type=str,
        help="provide a json file instead of querying the api",
    )
    parser.add_argument(
        "--save-json-file",
        dest="json_save_file_path",
        type=str,
        help="save a json file after querying the api",
    )
    parser.add_argument(
        "--max-dl-pages",
        dest="max_dl_pages",
        help="specify number of pages when querying the api. if not specified, defaults to 10. provide `ALL` to download all pages",
    )

    args = parser.parse_args()

    if not args.max_dl_pages:
        max_dl_pages = 10
    elif args.max_dl_pages == "ALL":
        max_dl_pages = None
    else:
        max_dl_pages = int(args.max_dl_pages)

    search_string = " ".join(args.strings)

    if not any(c.isalpha() for c in search_string) and not any(
        c.isnumeric() for c in search_string
    ):
        print(
            "ERROR: search_string: -->{}<-- does not contain any letters or numbers".format(
                search_string
            )
        )
        sys.exit()

    if args.json_load_file_path and args.json_save_file_path:
        print(
            "ERROR: Please only use `--load-json-file` OR `--save-json-file` NOT BOTH"
        )
        sys.exit()
    elif args.json_load_file_path:
        with open(args.json_load_file_path) as json_file:
            movies = json.load(json_file)
    else:
        movies = get_json_from_api(search_string, max_dl_pages)
        if args.json_save_file_path:
            with open(args.json_save_file_path, "w", encoding="utf-8") as f:
                json.dump(movies, f, ensure_ascii=False, indent=4)

    filtered_movie_list = filter_movies(search_string, movies)
    if len(filtered_movie_list) == 0:
        print("ERROR: No matches found")
        print(
            'HINT: try rephrasing the query. E.g. "god father ii" instead of "god father 2"'
        )
        sys.exit()

    result = pick_best_movie(filtered_movie_list)

    if len(result) == 1:
        print(format_result(search_string, result[0]))
    elif len(result) >= 2:
        print("ERROR: More than one match found")
        pretty_print(result)


if __name__ == "__main__":
    main_app()
