import time
import pandas as pd
import streamlit as st
import plotly

df = pd.read_csv(r'datasets/alcool-expect_vida-religiao.csv')

############
## Inicio ##
############

# st.markdown(
#         f"""
# <style>
#     .reportview-container .main .block-container{{
#         max-width: {max_width}px;
#         padding-top: {padding_top}rem;
#         padding-right: {padding_right}rem;
#         padding-left: {padding_left}rem;
#         padding-bottom: {padding_bottom}rem;
#     }}
#     .reportview-container .main {{
#         color: {COLOR};
#         background-color: {BACKGROUND_COLOR};
#     }}
# </style>
# """,
#    unsafe_allow_html=True,
# )

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

st.subheader('DataFrame a ser utilizado para o projeto')

st.dataframe(df)