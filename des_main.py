import sys
sys.dont_write_bytecode = True
from layout.login_layout import login_layout

if __name__ == "__main__" :
    """
    Code that runs when this is the main module.
    """
    login_layout_view = login_layout()
    login_layout_view.self_layout()
    login_layout_view.render()
    login_layout_view.listen()

    pass