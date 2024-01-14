# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 00:21:38 2021

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

col1, col2 = st.columns([2, 1])

st.sidebar.title("Parameters")
comp_val = st.sidebar.multiselect(label = "Tournament", options = comps_list, default = comps_list)
odds_val = st.sidebar.slider(label = "Price", min_value = min_price, max_value = max_price, value = [min_price, max_price])

from_date = st.date_input("From date", datetime.date(2021, 3, 15))
to_date = st.date_input("To date", datetime.datetime.today())

days_elapsed = (to_date - from_date).days
days_to_end_of_year = (datetime.date(2022, 1, 1) - to_date).days



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

pre_change = source[source['Date'] < datetime.datetime(2021,4,5).date()]
post_change = source[(source['Date'] > datetime.datetime(2021,4,5).date()) & (source['Date'] < datetime.datetime(2021,6,21).date()) ]
post_2nd_change = source[source['Date'] > datetime.datetime(2021,6,21).date()]

try:
    pre_profit = round(pre_change['Total_Profit'].iloc[-1], 2)
except: 
    pre_profit = 0

try: 
    post_profit = round(post_change['Total_Profit'].iloc[-1], 2) - pre_profit
except:
    post_profit = 0
    
try: 
    post_20_profit = round(post_2nd_change['Total_Profit'].iloc[-1], 2) - (pre_profit + post_profit)
except:
    post_20_profit = 0
    
pre_profit_amt = pre_profit * 10
post_profit_amt = post_profit * 15
post_20_profit_amt = post_20_profit *15



profit_tf =  int(pre_profit_amt + post_profit_amt + post_20_profit_amt)
#selection = alt.selection_multi(fields=['Total_Profit'])
#cond_color = alt.condition(tt_file.Total_Profit < 0, 'red', 'green')

eoy_proj = int(((profit_tf/days_elapsed)*days_to_end_of_year) + profit_tf)


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
#col2.metric("Total Profit: ", total_profit_loss)
#st.text(total_profit_loss)
col2.subheader("Total bets: " + str(number_of_bets))
col2.subheader("P/L: " + str(p_l_perc) + "%")
#col2.subheader("Profit (To Date): " + "£" + str(profit_tf))
#col2.subheader("Profit (End of year projection): " + "£" + str(eoy_proj))


if st.button("Show all bets in range:"):
    source


#st.image(image)
