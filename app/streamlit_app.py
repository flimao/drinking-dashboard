import time
import pandas as pd
import streamlit as st
import plotly.express as px

dfrel = pd.read_csv(r'datasets/religiao-tratado.csv')

def topnrels(n, df = dfrel):
    toprels = df.MajorReligion.value_counts().head(n)
    s = df.MajorReligion.where(df.MajorReligion.isin(toprels.index), 'Outros')
    s.name = 'MajorReligion_top'
    s.astype('category')
    return s

df_raw = pd.read_csv(r'datasets/alcool-expect_vida-religiao.csv')
df_full = (df_raw
    .astype({
        'Region': 'category',
        'IncomeGroup': 'category',
        'MajorReligion': 'category'
    })
)
df = df_full[(df_full.Year > 1960) & (df_full.Year <= 2011)]
df['MajorReligion_top'] = topnrels(5)
df['Total_BottlesWinePerMonth'] = df['Total_LitersAlcPerYear'] * (1 / (0.12 * 0.75 * 12))


top5rel = dfrel.MajorReligion.value_counts()

labels = {
    'LifeExp': 'Expectativa de vida',
    'Total_LitersAlcPerYear': 'Litros de álcool puro consumidos por ano por pessoa',
    'Region': 'Região',
    'Year': 'Ano',
    'Spirits_LitersPerYear': 'Destilados (L/ano)',
    'Total_BottlesWinePerMonth': 'Garrafas de vinho por mês por pessoa',
    'MajorReligion': 'Religião',
    'MajorReligion_top': 'Religião'
}



############
## Inicio ##
############

# css para tornar um pouco mais largo

st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 1000px;
    }}
</style>
""",
        unsafe_allow_html=True,
    )

st.title('Análise de consumo de álcool :beer:, expectativa de vida :older_woman: e religião :pray: em cada país')

st.header('Premissa')
# st.caption('Fine, I guess?..')

st.write('Vamos analisar a relação entre o consumo de álcool (cerveja, vinho e bebidas destiladas), a expectativa de vida e a religião de cada país')

st.subheader('Conjunto de dados a ser utilizado para o projeto (amostra)')

st.dataframe(df.sample(5))

st.header('Investigação inicial')

baralc = px.bar(df.groupby(['Year', 'Region']).mean().reset_index(), 
    x = 'Year', y = 'Total_BottlesWinePerMonth', 
    color = 'Region',
    title = 'Consumo de álcool ao longo do tempo', labels = labels
)
baralc.update_layout(
    autosize=False,
    width=1100,
    height=600
)

st.plotly_chart(baralc)

barrel = px.bar(df, 
    x = 'MajorReligion_top', y = 'Total_BottlesWinePerMonth', 
    title = 'Consumo de álcool por religião', labels = labels
)
barrel.update_layout(
    autosize=False,
    width=1100,
    height=600
)

st.plotly_chart(barrel)

sct = px.scatter(df, y = 'LifeExp', x = 'Total_BottlesWinePerMonth', 
    range_x = [df.Total_LitersAlcPerYear.min(), 20], 
    range_y = [df.LifeExp.min(), df.LifeExp.max()], 
    color = 'Region',
    animation_frame = 'Year',
    hover_data = ['Country'],
    title = 'Relação entre total de álcool consumido (garrafas de vinho equivalente por mês por pessoa) e Expectativa de vida',
    labels = labels
)

sct.update_layout(
    autosize=False,
    width=1100,
    height=600,
)

st.plotly_chart(sct)


st.write('Parece que não há uma relação muito clara entre os dois...')

st.header('Mapas')

mapa = px.choropleth(df, locations = 'CountryCode', color="Total_BottlesWinePerMonth", 
    range_color = [0, df['Total_BottlesWinePerMonth'].quantile(q = 0.975)],
    hover_name = 'Country', hover_data = ['MajorReligion'],
    animation_frame = 'Year', labels = labels
)

mapa.update_layout(
    autosize=False,
    width=1100,
    height=600,
    title = 'Consumo de bebidas alcoolicas (em garrafas de vinho equivalentes por mês por pessoa, entre 1960 e 2011)' 
)

st.plotly_chart(mapa)