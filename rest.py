
from click import *


@command()
@option('--count', default=1, help='Number of greetings.')
@option('--name', prompt='Your name', help='The person to greet.')
def hello(count, name):
    for x in range(count):
        echo('Hello %s!' % name)


if __name__ == '__main__':
    hello()
