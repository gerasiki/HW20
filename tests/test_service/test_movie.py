from unittest.mock import MagicMock

import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService
from setup_db import db


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    avatar = Movie(id=1, title='avatar', description="any desc 1", trailer='any trailer 1', year=2009, rating=8)
    avengers = Movie(id=2, title='avengers', description="any desc 2", trailer='any trailer 2', year=2012, rating=7.9)
    thor = Movie(id=3, title='thor', description="any desc 3", trailer='any trailer 3', year=2011, rating=6.7)

    movie_dao.get_one = MagicMock(return_value=avatar)
    movie_dao.get_all = MagicMock(return_value=[avatar, avengers, thor])
    movie_dao.create = MagicMock(return_value=Movie(id=3))
    movie_dao.update = MagicMock()
    movie_dao.delete = MagicMock()
    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie != None
        assert movie.id != None

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0

    def test_create(self):
        movie_d = {
            "title": "thor 2",
            "description": "any desc 4",
            "trailer": "any trailer 4",
            "year": 2012,
            "rating": 7.3
        }
        movie = self.movie_service.create(movie_d)
        assert movie.id != None

    def test_update(self):
        movie_d = {
            "id": 3,
            "title": "thor: ragnarok",
            "description": "any desc new",
            "trailer": "any trailer new",
            "year": 2017,
            "rating": 7.7
        }
        self.movie_service.update(movie_d)

    def test_delete(self):
        self.movie_service.delete(1)
