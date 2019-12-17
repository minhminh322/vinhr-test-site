from pathlib import Path
import pandas as pd
import logging

Path.ls = lambda x : [o.name for o in x.iterdir()]
Path.ls_p = lambda x : [str(o) for o in x.iterdir()]
Path.str = lambda x : str(x)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='app.log',
                    filemode='w')
