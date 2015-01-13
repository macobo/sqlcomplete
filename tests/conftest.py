import sys
import logging

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s::%(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
