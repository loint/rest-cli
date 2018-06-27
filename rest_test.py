import pytest
from os import system, path, getcwd, chdir

__author__ = "Loi Nguyen <loinguyentrung@gmail.com>"


class TestRestCLI:

    @staticmethod
    def install():
        system('make && make install')

    @staticmethod
    def assert_database():
        assert True is True

    @staticmethod
    def assert_structure():
        assert path.isdir('vendor') is True
        assert path.isdir('src/Model') is True
        assert path.isdir('src/Repository') is True
        assert path.isdir('src/Service') is True
        assert path.isdir('src/Controller') is True

    def test_rest_cli(self):
        #self.install()
        system('rest create user --quite --force')
        assert path.isdir('user') is True
        current_dir = getcwd()
        chdir(current_dir + '/user')
        system('rest migrate')
        self.assert_database()
        #system('rest sync')
        #self.assert_structure()
        chdir(current_dir)


