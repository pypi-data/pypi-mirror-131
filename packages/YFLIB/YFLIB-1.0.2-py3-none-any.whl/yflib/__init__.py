import os
if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),"cache")):
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)),"cache"))

__version__ = "1.0.0"