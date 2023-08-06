import transistordatabase as tdb
import numpy as np
import datetime
import pytest
from pytest import approx
import os





if __name__ == '__main__':
    t = tdb.import_json('GS66506T.json')
    t.export_datasheet()
