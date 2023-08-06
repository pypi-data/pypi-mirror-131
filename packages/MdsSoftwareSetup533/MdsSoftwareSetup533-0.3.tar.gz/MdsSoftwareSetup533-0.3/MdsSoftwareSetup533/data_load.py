# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---


import pandas as pd
import os
import sys

def read_data():
    try:
        data= pd.read_csv('MdsSoftwareSetup533/base_data.csv',index_col=False)
    except FileNotFoundError:
        print("Invalid file address")
        sys.exit(0)
    else: 
        try:
            return data
        except NameError:
            print("data not found")
            sys.exit()

    
