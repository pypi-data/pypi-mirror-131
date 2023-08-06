# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.12.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
  
import pandas as pd
import MdsSoftwareSetup.data_load as dl

from MdsSoftwareSetup import base_class
class conda_class(base_class.base):
       
    data=dl.read_data()
    def __init__(self,software_name,os):
        self.software_name=software_name
        self.os=os
    def Installation_Guide(self):
        print('\033[1m'+base_class.base.message(self))
        data1=conda_class.data[conda_class.data["OS"]=="Mac"]
        data1=data1[data1["Software"]=="Anaconda"]
        print('\033[1m'+"Below is the link containing step-by-step installation instructions:\n")
        ig=data1.to_string(columns=['Installation_Guide'], index=False,header=False)
        return ig
    
    def Description(self):
        data1=conda_class.data[conda_class.data["OS"]=="Mac"]
        data1=data1[data1["Software"]=="Anaconda"]
        print('\033[1m'+"Below is a brief description of Anaconda: \n")
        desc=data1.to_string(columns=['Description'], index=False,header=False)
        return desc
    
    def Tutorial(self):
        data1=conda_class.data[conda_class.data["OS"]=="Mac"]
        data1=data1[data1["Software"]=="Anaconda"]
        print('\033[1m'+"Below is the link for a video tutorial of Anaconda: \n ")
        Tutorial=data1.to_string(columns=['Tutorial'], index=False,header=False)
        return Tutorial

    

