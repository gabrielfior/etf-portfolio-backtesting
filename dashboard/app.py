#from calculations.db.DatabaseHandler import DatabaseHandler
from  .. import calculations as c2
import streamlit as st
import numpy as np
import pandas as pd

'''
st.title('Portfolio visualization')

# get data from sqlite, plot it
d = DatabaseHandler()
df = pd.read_sql_table(d.tablename, d.engine, parse_dates=['Date'])

st.line_chart(df)
'''

#ToDo - Check how to do proper import -> https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
d = DatabaseHandler()
print ('test')