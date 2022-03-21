import streamlit as st
import pandas as pd
import datetime as dt
import plotly.express as px
import numpy as np
from millify import millify

st.set_page_config(
     page_title="UH 2022",
     page_icon="💣",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'About': "University Hack 2022. Created by Eva Barrero"
     }
 )


@st.cache
def load_top_items():
    items = pd.read_csv('./modified_data/items_categories.csv')
    return items

@st.cache
def load_map():
    map = pd.read_csv('./modified_data/coords.csv')
    return map

@st.cache
def load_sales_and_orders():
    items = pd.read_csv('./modified_data/sales_and_orders.csv')
    items['date'] = pd.to_datetime(items['date'])
    return items.set_index('date')

@st.cache
def load_map_table():
    map = pd.read_csv('./modified_data/map.csv')
    map = map.groupby(['city']).size().reset_index(name='counts').sort_values('counts', ascending=False).head(10)
    return map

@st.cache
def load_categories():
    products_cat = pd.read_csv('./modified_data/categories_bien.csv').fillna('')
    return products_cat


# items = load_items()
top_items = load_top_items()
items_select = load_sales_and_orders()

st.title('Sales report')


st.header("Overview")
col1, col2, col3, col4= st.columns([2,1,1,1])
select = ['Sales', 'Orders']
column = col1.selectbox("Select a variable to analyze",select)
items_grouped = items_select.groupby(items_select.index.year).sum()[column]
items_grouped_month = items_select.groupby([items_select.index.year, items_select.index.month]).sum()[column]
i = ['€' if column == 'Sales' else '']
col3.metric(f'{column} this year', f'{millify(items_grouped.iloc[1])}{i[0]}', f'{round(items_grouped.iloc[1]/items_grouped.iloc[0] * 100, 2)} %')
col4.metric(f'{column} last month', f'{millify(items_grouped_month.iloc[-1])}{i[0]}', f'{round(items_grouped_month.iloc[-1]/items_grouped_month.iloc[-2] * 100, 2)} %')


col1, col2 = st.columns([2,1])
col2.markdown('<br/><br/>', unsafe_allow_html=True)
fecha = col2.date_input('Date range', value=[items_select.index.min(), items_select.index.max()],
                    min_value=items_select.index.min(), max_value=items_select.index.max())
mode = col2.checkbox('Acummulative')
if mode:
    items_select = items_select.cumsum(axis=0)
fig = px.line(items_select, x=items_select.index, y=column, title = f"{column} from {fecha[0].strftime('%Y-%m-%d')} to {fecha[1].strftime('%Y-%m-%d')}",
            range_x=[fecha[0].strftime('%Y-%m-%d'), fecha[1].strftime('%Y-%m-%d')])

col1.plotly_chart(fig, use_container_width=True)




coords = load_map()
table = load_map_table()
st.header('Sales by location')
col1, col2, col3 = st.columns([2, 0.5, 2])
select_country = col1.selectbox('Select a place to plot', ['Europe', 'Worldwide'])
if select_country == 'Europe':
    fig = px.scatter_geo(coords, lat=coords.lat, lon=coords.lon, size='counts', scope='europe')
else: 
    fig = px.scatter_geo(coords, lat=coords.lat, lon=coords.lon, size='counts', projection='natural earth')
col1.plotly_chart(fig, use_container_width=True)
col3.dataframe(table, height = 430)



st.header('Best-selling products')
with st.container():
    col1, col12, col2, col3, col4 = st.columns([1, 1, 1, 2.5, 2])
    col1.write('')
    col12.markdown('**Sales**')
    col2.markdown('**Orders**')
    col3.markdown('**Name**')
    col4.markdown('**Category**')

    col1, col12, col2, col3, col4 = st.columns([1, 1, 1, 2.5, 2])
    item = top_items.iloc[0]
    col1.markdown('<h5 style="color:blue"> 1. </h5>', unsafe_allow_html=True)
    col12.write(str(item['Sales']))
    col2.write(str(item['Orders']))
    col3.write(item['name'])
    col4.write(item['cat1'])

    # col1, col12, col2, col3, col4 = st.columns([1, 1, 1, 2.5, 2])
    item = top_items.iloc[1]
    col1.markdown('<h5 style="color:blue"> 2. </h5>', unsafe_allow_html=True)
    col12.write(str(item['Sales']))
    col2.write(str(item['Orders']))
    col3.write(item['name'])
    col4.write(item['cat1'])

    # col1, col12, col2, col3, col4 = st.columns([1, 1, 1, 2.5, 2])
    item = top_items.iloc[2]
    col1.markdown('<h5 style="color:blue"> 3. </h5>', unsafe_allow_html=True)
    col12.write(str(item['Sales']))
    col2.write(str(item['Orders']))
    col3.write(item['name'])
    col4.write(item['cat1'])
    
    more = st.selectbox('Search a product', top_items.name, 3)
    col1, col12, col2, col3, col4 = st.columns([1, 1, 1, 2.5, 2])
    item = top_items[top_items['name'] == more]
    index = item.index.tolist()[0]
    col1.markdown(f'<h5 style="color:blue"> {index + 1}. </h5>', unsafe_allow_html=True)
    col12.write(str(item['Sales'].values[0]))
    col2.write(str(item['Orders'].values[0]))
    col3.write(item['name'].values[0])
    col4.write(item['cat1'].values[0])

st.header("Sales by categories")
fig = px.sunburst(top_items.dropna(), path=['cat1', 'cat2'])
st.plotly_chart(fig)
