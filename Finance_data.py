import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go 
import plotly.express as px 

import openpyxl
import xlrd
import itertools


st.set_page_config(layout = 'wide',
                   page_title = 'Sales Dashboard' ,page_icon=":bar_chart:"
                   )

st.title(' 🔍 Financial Data Dashboard')
st.markdown("_Prototype v0.4.1_")

@st.cache_data
def load_data(file):
    try:
        data = pd.read_excel(file,engine = 'openpyxl')
    except:
        data =pd.read_excel(file,engine = 'xlrd')   
    return data     
    
    
with st.sidebar:
    uploaded_file = st.file_uploader("Choose a file")



if uploaded_file is None:
    st.info(" Upload a file through config", icon = "ℹ️")
    st.stop()

df = load_data(uploaded_file)  

with st.expander('Data Preview ℹ️'):
    st.dataframe(df,
                 column_config={'Year':st.column_config.NumberColumn(format = "%d")})

st.divider()


# line chart 
df = pd.read_excel('./Financial Data Clean.xlsx')
print(df.head(2))

all_months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


def plot_bottom_left():
    sales_data = df.loc[(df['Year'] == 2023) &
            (df['Account'] == 'Sales') & 
            (df['business_unit'] == 'Software'),
            ['Scenario'] + all_months].melt(id_vars='Scenario',
                                            var_name = 'month',
                                            value_name = 'sales')
 

    fig = px.line(sales_data,
                  x = 'month',
                  y = 'sales',
                  color='Scenario',
                  text='sales',
                  title = ' 📊 Monthly Budget vs Forecast 2023'
                  )
    fig.update_traces(textposition = 'top right')
    st.plotly_chart(fig, use_container_width=True)

plot_bottom_left()    

st.divider()

def plot_bottom_right():
    data2 = df.loc[
        (df['Year'] == 2023) &
        (df['Account']=='Sales') ,
        ['Scenario','business_unit'] + all_months
    ]

    data2 = data2.melt(
        id_vars=['Scenario','business_unit'],
        value_vars=all_months,
        var_name = 'months',
        value_name='sales'
    )

    agg_sales = data2.groupby(['Scenario','business_unit'],as_index=False)['sales'].sum()

    fig = px.bar(agg_sales,
                 x = 'business_unit',
                 y = 'sales',
                 color='Scenario',
                 barmode='group',
                 text_auto='.2s',
                 title=' 📈 Sales for The Year 2023',
                 height=400,)
    fig.update_traces(textfont_size = 12,
                      textangle = 0,
                      textposition = 'outside',
                      cliponaxis = False)
    st.plotly_chart(fig,use_container_width=True)

plot_bottom_right()    

st.divider()



def plot_bottom_left():
    data3 = df.loc[(df['Scenario'] == 'Actuals')]
    data3[all_months] = data3[all_months].abs()

    data3 = data3.melt(id_vars=['Account','Year'],
                       value_vars=all_months,
                       var_name='month',
                       value_name='sales')

    add_sales3 = data3.groupby(['Account', 'Year'])['sales'].sum().reset_index()
    colors = itertools.cycle(['rgb(51,34,222)', 'rgb(222,51,34)', 'rgb(34,222,51)', 'rgb(255,165,0)', 'rgb(148,0,211)'])

    trace = []
    for account in add_sales3['Account'].unique():
        account_data = add_sales3[add_sales3['Account'] == account]
        trace.append(go.Bar(
            x=account_data['Year'],
            y=account_data['sales'],
            name=account,
            marker=dict(color=next(colors), line={'width': 2})
        ))

    layout = go.Layout(
        title=' 🔍 Actual Yearly Sales per Account',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Sales'),
        hovermode='closest',
        barmode='group'
    )

    fig = go.Figure(data=trace, layout=layout)

    st.plotly_chart(fig, use_container_width=True)

plot_bottom_left()    
st.divider()

print(df.head(6))







