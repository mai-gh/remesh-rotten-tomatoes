#!/usr/bin/env python3

import rt

import urllib.request
import urllib.parse
import json


def movie_builder(name, critval, usrval, year):
  if critval:
    critval = int(critval) # this matches what the api responds with
  if usrval:
    usrval = str(usrval)
  if year:
    year = str(year)

  movie = {
    "name": str(name),
    "criticsScore": {
      "value": critval
    },
    "audienceScore": {
      "score": usrval,
    },
    "releaseYear": year
  }

  return movie

def test_api_results_length():
  data = rt.get_json_from_api("lord of the rings", max_pages=1)
  assert len(data) == 7
  
def test_filter_movies_names():
  data = [ movie_builder("the lord of the rings", 95, 90, 2000),
           movie_builder("star wars", 95, 90, 2000),
           movie_builder("star trek", 95, 90, 2000),
           movie_builder("the terminator", 95, 90, 2000),
           movie_builder("the godfather", 95, 90, 2000),
           movie_builder("the matrix", 95, 90, 2000) ]

  assert len(data) == 6
  assert len(rt.filter_movies("lord rings", data)) == 1
  assert rt.filter_movies("lord rings", data)[0]['name'] == "the lord of the rings"
  assert len(rt.filter_movies("star", data)) == 2

def test_filter_movies_critic_score():
  data = [ movie_builder("the lord of the rings", None, 90, 2000),
           movie_builder("star wars", 95, 90, 2000),
           movie_builder("star trek", None, 90, 2000),
           movie_builder("the terminator", 95, 90, 2000),
           movie_builder("the godfather", 95, 90, 2000),
           movie_builder("the matrix", 95, 90, 2000) ]

  assert len(data) == 6
  assert len(rt.filter_movies("lord rings", data)) == 0
  assert len(rt.filter_movies("star", data)) == 1
  assert len(rt.filter_movies("the", data)) == 3


def test_filter_movies_audience_score():
  data = [ movie_builder("the lord of the rings", 95, None, 2000),
           movie_builder("star wars", 95, 90, 2000),
           movie_builder("star trek", 95, None, 2000),
           movie_builder("the terminator", 95, 90, 2000),
           movie_builder("the godfather", 95, 90, 2000),
           movie_builder("the matrix", 95, 90, 2000) ]

  assert len(data) == 6
  assert len(rt.filter_movies("lord rings", data)) == 0
  assert len(rt.filter_movies("star", data)) == 1
  assert len(rt.filter_movies("the", data)) == 3

def test_filter_movies_release_year():
  data = [ movie_builder("the lord of the rings", 95, 90, None),
           movie_builder("star wars", 95, 90, 2000),
           movie_builder("star trek", 95, 90, None),
           movie_builder("the terminator", 95, 90, 2000),
           movie_builder("the godfather", 95, 90, 2000),
           movie_builder("the matrix", 95, 90, 2000) ]

  assert len(data) == 6
  assert len(rt.filter_movies("lord rings", data)) == 0
  assert len(rt.filter_movies("star", data)) == 1
  assert len(rt.filter_movies("the", data)) == 3

def test_pick_best_movie_critic():
  data = [ movie_builder("the lord of the rings", 95, 90, 2000),
           movie_builder("star wars", 100, 90, 2000),
           movie_builder("star trek", 95, 90, 2000) ]
  assert len(rt.pick_best_movie(data)) == 1
  assert rt.pick_best_movie(data)[0]['name'] == "star wars"
   
def test_pick_best_movie_audience():
  data = [ movie_builder("the lord of the rings", 95, 90, 2000),
           movie_builder("star wars", 100, 90, 2000),
           movie_builder("star trek", 100, 92, 2000) ]
  assert len(rt.pick_best_movie(data)) == 1
  assert rt.pick_best_movie(data)[0]['name'] == "star trek"
   
def test_pick_best_movie_year():
  data = [ movie_builder("the lord of the rings", 95, 90, 1999),
           movie_builder("star wars", 95, 90, 2000),
           movie_builder("star trek", 95, 90, 2000) ]
  assert len(rt.pick_best_movie(data)) == 1
  assert rt.pick_best_movie(data)[0]['name'] == "the lord of the rings"
   

def test_pick_best_movie_year():
  data = [ movie_builder("the lord of the rings", 95, 90, 1999),
           movie_builder("star wars", 95, 90, 2000),
           movie_builder("star trek", 95, 90, 1999) ]
  assert len(rt.pick_best_movie(data)) == 2
  assert rt.pick_best_movie(data)[0]['name'] == "the lord of the rings"
  assert rt.pick_best_movie(data)[1]['name'] == "star trek"
   
