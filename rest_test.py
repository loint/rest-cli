import pytest
from os import system, path

__author__ = "Loi Nguyen <loinguyentrung@gmail.com>"


class TestRest:

    @staticmethod
    def install():
        system('make && make install')

    def test_rest_create(self):
        self.install()
        system('rest create user --quite --force')
        assert path.isdir('user') is True

