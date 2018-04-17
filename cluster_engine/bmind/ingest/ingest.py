import glob

import pandas as pd


def read_multi_csv(directory, filepattern):
    files = glob.glob(directory + filepattern)

    df = pd.concat([pd.read_csv(f) for f in files])
    return df
