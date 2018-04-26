import sys, os
sys.path.append(os.path.relpath(".."))

import template.template as template
from Misc import button

class Menu(template.State):
    
    def __init__(self):
        super().__init__("menu")
