# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 18:58:02 2021

@author: fothe
"""

import streamlit as st

import numpy as np 
import pandas as pd
import altair as alt
from PIL import Image
import datetime

tt_file = pd.read_csv(r"https://raw.githubusercontent.com/tomfothergill/tabletennis/main/Model_Assessment.csv")
tt_file = tt_file[~tt_file['Scoreline'].isnull()]
tt_file['Date'] = pd.to_datetime(tt_file['Time']).dt.date
#st.line_chart(tt_file)


#################################################################
comps_list = list(tt_file.League.unique())
min_price = float(tt_file.Price.min())
max_price = float(tt_file.Price.max())

col1, col2 = st.beta_columns([2, 1])

st.sidebar.title("Parameters")
comp_val = st.sidebar.multiselect(label = "Tournament", options = comps_list, default = comps_list)
odds_val = st.sidebar.slider(label = "Price", min_value = min_price, max_value = max_price, value = [min_price, max_price])

from_date = st.date_input("From date", datetime.date(2021, 3, 15))
to_date = st.date_input("To date", datetime.datetime.today())


col1.title("Model Performance")
#source = data.stocks()

tt_file = tt_file[tt_file['Date'].between(from_date, to_date)]
source = tt_file[(tt_file['League'].isin(comp_val)) & (tt_file['Price'].between(odds_val[0], odds_val[1]))]
source = source.sort_values(by = ['Time'])


source = source.reset_index(drop = True)

source['Total_Return'] =  source.Returns.cumsum()
source['Total_Spend'] = source.Unit_Stake.cumsum()

source['Total_Profit'] = source['Total_Return'] - source['Total_Spend'] 
source['Bet_No'] = source.index
source['Bet_Profit'] = source.Returns - source.Unit_Stake
source['y'] = 0

total_profit_loss = round(source['Total_Profit'].iloc[-1], 2)
number_of_bets = source.Time.count()
p_l_perc = round((total_profit_loss/number_of_bets) * 100, 2)
#selection = alt.selection_multi(fields=['Total_Profit'])
#cond_color = alt.condition(tt_file.Total_Profit < 0, 'red', 'green')

#test = alt.Predicate(1<2)

base = alt.Chart(source)

area = alt.Chart(source).mark_line( 
    line = {'color':'darkgrey'},
    color = 'lightblue'
).encode(
    x='Bet_No',
    y='Total_Profit',
    #color=alt.condition(alt.datum.Total_Profit < 0, alt.value('red'), alt.value('green'))
)
    
c1 = base.mark_rule(strokeDash = [10, 10], color = 'darkgrey').encode(y = 'y')    
    
col1.altair_chart(area + c1, use_container_width = True)
col2.subheader("Total Profit: " + str(total_profit_loss) + " units")
#st.text(total_profit_loss)
col2.subheader("Total bets: " + str(number_of_bets))
col2.subheader("P/L: " + str(p_l_perc) + "%")




#st.image(image)
