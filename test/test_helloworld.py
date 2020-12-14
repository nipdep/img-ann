
from helloworld import sayHello

def test_sayHello_with_no_params():
    assert sayHello() == "Hello, World!"

def test_sayHello_with_params():
    assert sayHello("Everyone") == "Hello, Everyone!"
