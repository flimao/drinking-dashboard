import time
import streamlit as st
import plotly 


st.title('Hello, *World!* :sunglasses:')

st.header('How are you today?')
st.caption('Fine, I guess?..')
st.write('<br><br>', unsafe_allow_html = True)

st.text('Some code:')
st.code('''
st.title('Hello, *World!* :sunglasses:')

st.header('How are you today?')
st.caption('Fine, I guess?..')
''')

st.write('<br><br>', unsafe_allow_html = True)

st.write('Legen...')
with st.spinner('...wait for it...'):
    time.sleep(5)
st.success('...dary!')

# cards
avg_mm = 0.7

cols = st.columns(3)
cols[1].metric('Variação MoM', f'{avg_mm:.0%}', f'{avg_mm - 1:.0%}')
