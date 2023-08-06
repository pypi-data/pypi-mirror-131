import code
import os

def pry():
    """Opens interactive python console when this line is called, 
    with then-loaded variables, functions, modules, etc. available."""
    code.interact(local=dict(globals(), **locals()))

def cd(path):
    '''
    Moves from current directory to path passed as argument,
    printing current & posterior path locations.

    :param str path: destination to move to
    '''
    print("\nCurrently in ", os.getcwd())
    os.chdir(path)
    print("\nMoved to ", os.getcwd())

def pwd():
    '''
    Prints current directory.
    '''
    print(os.getcwd())