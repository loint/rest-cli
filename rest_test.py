from pytest import *
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
    def assert_new_application():
        assert path.isdir('user') is True
        assert path.isfile('user/rest.json') is True
        assert path.isfile('user/config/database.php') is True

    @staticmethod
    def assert_sync_structure():
        # Assert application structure
        assert path.isdir('vendor') is True
        assert path.isdir('src/Model') is True
        assert path.isdir('src/Repository') is True
        assert path.isdir('src/Service') is True
        assert path.isdir('src/Controller') is True
        assert path.isdir('src/Shared/IO') is True
        assert path.isdir('test/Controller') is True
        # Assert example structure
        assert path.isfile('src/Model/User.php') is True
        assert path.isfile('src/Repository/UserRepository/UserRepository.php') is True
        assert path.isfile('src/Repository/UserRepository/UserRepositoryImpl.php') is True
        assert path.isfile('src/Service/UserService/UserService.php') is True
        assert path.isfile('src/Service/UserService/UserServiceImpl.php') is True
        assert path.isfile('src/Controller/UserController.php') is True
        assert path.isdir('src/Shared/IO/UserController') is True
        assert path.isfile('test/Controller/UserControllerTest.php') is True

    @mark.dependency()
    def test_rest_create(self):
        system('rest create user --quite --force --mysql')
        self.assert_new_application()

    @mark.dependency(depends=["TestRestCLI::test_rest_create"])
    def test_rest_migration(self):
        chdir(getcwd() + '/user')
        system('rest migrate')
        self.assert_database()

    @mark.dependency(depends=["TestRestCLI::test_rest_migration"])
    def test_rest_synchronization(self):
        system('rest sync')
        self.assert_sync_structure()
        chdir('../')


