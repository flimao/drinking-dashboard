import time
from scipy.stats import sem
import pandas as pd
import streamlit as st
import plotly.express as px

dfrel = pd.read_csv(r'datasets/religiao-tratado.csv')

# função para calcular as n maiores religioes, considerando o número de países que as seguem
def topnrels(n, df = dfrel):
    toprels = df.MajorReligion.value_counts().head(n)
    s = df.MajorReligion.where(df.MajorReligion.isin(toprels.index), 'Outros')
    s.name = 'MajorReligion_top'
    s.astype('category')
    return s

# import e processamento do dataset principal
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

# labels das colunas, para rotular nos gráficos
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

# construção do mapa de cores consistente em todos os gráficos
regions = df['Region'].unique()
color_palette = px.colors.qualitative.G10

region_colors = { region: color for region, color in zip(regions, color_palette[:len(regions)]) }

# este texto estará em todas as conclusões parciais
conclusao = r'**_Pontos notáveis_**:'


############
## Inicio ##
############

# css para tornar um pouco mais largo

st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 65%;
    }}
</style>
""",
        unsafe_allow_html=True,
    )

# aqui começa o conteúdo
st.title('Análise de consumo de álcool :beer:, expectativa de vida :older_woman: e religião :pray: em cada país')

st.header('Premissa')
st.write('Vamos analisar a relação entre o consumo de álcool (cerveja, vinho e bebidas destiladas), a expectativa de vida e a religião de cada país')

st.subheader('Conjunto de dados a ser utilizado para o projeto (amostra)')
st.dataframe(df.sample(5))

# aqui começam os gráficos
st.header('Investigação')

### gráfico de linha para mostrar a evolução do consumo de bebidas alcoólicas ao longo do tempo por regiao
dfline = df.groupby(['Year', 'Region']).mean().reset_index()
alcline = px.scatter(dfline, 
    x = 'Year', y = 'Total_BottlesWinePerMonth', 
    color = 'Region', color_discrete_map = region_colors,
    title = 'Consumo de álcool ao longo do tempo', labels = labels,
)

alcline.update_traces(
    mode = 'lines',
    hovertemplate =
        '<b>%{fullData.name}</b><br>' + 
        labels['Total_BottlesWinePerMonth'] +': %{y:.1f} garrafas'+
        '<extra></extra>'
)

alcline.update_layout(
    autosize=False,
    width=1100,
    height=600,
    hovermode = 'x unified',
)

st.plotly_chart(alcline)

st.success(fr'''{conclusao}
A Europa é a maior consumidora de bebidas alcoólicas, bebendo em média 40% a mais que as Américas (2ª maior consumidora).


Há um aumento de ± 25% no consumo de álcool da Europa na década de 70. Este aumento se reverteu lentamente durante a década de 80, até se estabilizar no nível anterior.
    
Esse aumento pontual não foi observado nas outras regiões.
''')

### gráfico de barras do consumo de álcool por religião
st.markdown('---')

dfrel = df.groupby(['MajorReligion_top']).agg(
    Total_BottlesWinePerMonth = pd.NamedAgg('Total_BottlesWinePerMonth', 'mean'),
    Total_BottlesWinePerMonth_error = pd.NamedAgg('Total_BottlesWinePerMonth', sem)
).reset_index()

barrel = px.bar(dfrel, 
    x = 'MajorReligion_top', y = 'Total_BottlesWinePerMonth', 
    title = 'Consumo de álcool por religião', labels = labels,
    error_y = 'Total_BottlesWinePerMonth_error', 
    color_discrete_sequence = color_palette
)

barrel.update_traces(
    hovertemplate = 
    '<b>Religião: %{x}</b><br>' +
    labels['Total_BottlesWinePerMonth'] +': %{y:.1f} garrafas'+
    '<extra></extra>',
    error_y_color = color_palette[-3],
    error_y_thickness = 3
)
barrel.update_layout(
    autosize=False,
    width=1100,
    height=600,
    xaxis = {'categoryorder': 'total descending'}
)

st.plotly_chart(barrel)

st.success(rf'''{conclusao} 
As pessoas que se dizem **Católicos Romanos** (ou equivalente), **Budistas** ou de outras religiões são as que mais consomem bebidas alcoólicas, 
consumindo cada um o equivalente a entre 2 e 4.5 garrafas de vinho por mês.
    
**Anglicanos** bebem substancialmente menos que Católicos Romanos, consumindo por volta de 1.5 garrafa de vinho por mês por pessoa.

As pessoas que se dizem sem religião tem o consumo de bebidas bastante variável; algumas consomem bastante e outras não consomem nenhuma bebida alcoólica.
''')

### relação entre consumo de bebidas alcoólicas e expectativa de vida
sct = px.scatter(df, y = 'LifeExp', x = 'Total_BottlesWinePerMonth', 
    range_x = [df.Total_LitersAlcPerYear.min(), 20], 
    range_y = [df.LifeExp.min(), df.LifeExp.max()], 
    color = 'Region', color_discrete_map = region_colors,
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

st.info(fr'Parece que não há uma relação muito clara entre a quantidade de álcool consumida e a expectativa de vida, mesmo se separarmos por região.')

### mapa de consumo de bebidas alcoólicas ao longo do tempo

st.markdown('---')
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
    title = 'Consumo de bebidas alcoólicas (em garrafas de vinho equivalentes por mês por pessoa, entre 1960 e 2011)' 
)

st.plotly_chart(mapa)

st.success(fr'''{conclusao}
Até meados da década de 80, A Austrália, o Chile e a Europa como um todo consumiam grandes quantidades de bebidas alcoólicas. Desde então, ...

''')