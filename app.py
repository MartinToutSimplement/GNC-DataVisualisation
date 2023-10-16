import bar_chart_race as bcr
import time
import matplotlib.pyplot as plt
import geopandas as gpd
import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk


@st.cache_data
def load_data():
    df = pd.read_csv('consommation-regionale-gnc.csv', delimiter=';')

    df[['index', 'annee']] = df.iloc[:, 0].str.split(',', 1, expand=True)
    df['annee'] = df['annee'].str.replace('"', '').astype(int)

    df['latitude'], df['longitude'] = df['centroid'].str.split(',', 1).str
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].str.replace('"', '').astype(float)

    df.drop(columns=[df.columns[0], 'index', 'centroid'], inplace=True)

    return df


df = load_data()

st.title("Dashboard on CNG consumption by region in France")
st.write("""
Welcome to this dashboard displaying CNG consumption by region in France.
CNG stands for Compressed Natural Gas. It's an ecological alternative to traditional vehicle fuels.
""")

st.write("Le gaz naturel comprimé (abrégé en GNC) est du gaz naturel utilisé comme carburant pour les véhicules à moteur comme les voitures, bus ou les camions. Il est stocké sous pression dans des réservoirs spécifiques du véhicule, généralement à une pression de l'ordre de 200 bars.")

st.write("""Avantages :

Émissions réduites : Le GNC brûle plus proprement que l'essence ou le diesel, ce qui signifie moins d'émissions de gaz à effet de serre et d'autres polluants.

Coûts : Dans certaines régions, le GNC peut être moins cher que l'essence ou le diesel, ce qui peut entraîner des économies pour les utilisateurs.

Sécurité : Le GNC est moins dense que l'air, il s'évapore donc rapidement en cas de fuite, ce qui réduit les risques d'incendie.
      
Inconvénients :
    
Infrastructure limitée : Le nombre de stations-service offrant du GNC est encore limité dans de nombreux endroits, bien que cela change progressivement.

Espace de stockage : Les réservoirs de GNC dans les véhicules peuvent être plus gros et plus lourds que les réservoirs d'essence traditionnels.

Distance parcourue : Actuellement, un plein de GNC peut ne pas offrir autant de kilomètres qu'un plein d'essence, bien que cela dépende du véhicule et du réservoir.

Utilisation : Le GNC est principalement utilisé pour les flottes de véhicules, comme les bus de transport en commun, les camions poubelles, et certains taxis. Cependant, il y a aussi des voitures particulières alimentées au GNC disponibles sur le marché.

Impact sur l'environnement :
Le GNC est souvent considéré comme une option plus respectueuse de l'environnement que l'essence ou le diesel en raison de ses émissions réduites. Toutefois, il convient de noter que l'extraction, le traitement, le transport et le stockage du gaz naturel peuvent également avoir des impacts environnementaux.

Conclusion :
Bien que le GNC présente certains avantages, notamment en matière d'émissions, il ne représente qu'une des nombreuses solutions potentielles pour réduire notre dépendance aux combustibles fossiles et limiter notre impact environnemental. La combinaison de différentes sources d'énergie, technologies et pratiques est essentielle pour une transition énergétique réussie.
""")

st.write("Data overview:")
st.write(df.head())
st.sidebar.write("Martin LUCAS - DIA")
st.sidebar.write("Github: https://github.com/MartinToutSimplement")
st.sidebar.write("Linkedin: https://www.linkedin.com/in/martin-lucas02/")
st.sidebar.write("Efrei PARIS - PROMO 2025")
st.sidebar.header("Filters")
st.sidebar.write("""
Utilisez les curseurs ci-dessous pour sélectionner deux années différentes afin de comparer la consommation de GNC entre elles.
""")

year1 = st.sidebar.slider("Sélectionnez la première année", min_value=df['annee'].min(
), max_value=df['annee'].max(), value=df['annee'].min())
year2 = st.sidebar.slider("Sélectionnez la deuxième année", min_value=df['annee'].min(
), max_value=df['annee'].max(), value=df['annee'].max())

df_comparison = df[(df['annee'] == year1) | (df['annee'] == year2)]

comparison_chart = alt.Chart(df_comparison).mark_bar().encode(
    x='region:N',
    y=alt.Y('consommation_gwh_pcs:Q', stack=None,
            title='Consommation (GWh PCS)'),
    color='annee:N',
    tooltip=['region', 'consommation_gwh_pcs']
).properties(
    title=f"Comparaison de la consommation de GNC entre {year1} et {year2}",
    width=700,
    height=400
)
st.altair_chart(comparison_chart, use_container_width=True)


st.sidebar.write("""
Pour analyser la tendance de consommation d'une région spécifique au fil des ans, sélectionnez une région ci-dessous.
""")


st.write("""Nous pouvons voir que chaque région a une consommation de GNC différente. Cela peut être dû à plusieurs facteurs, notamment la population, le nombre de stations-service, la disponibilité des véhicules alimentés au GNC, etc.
La consommation est généralement croissante, mise à part quelques région qui diminue dans les années 2015-2017 puis qui remonte.""")
selected_region = st.sidebar.selectbox(
    "Sélectionnez une région pour voir la tendance de consommation", df['region'].unique())

df_region = df[df['region'] == selected_region]

trend_chart = alt.Chart(df_region).mark_line(point=True).encode(
    x='annee:O',
    y='consommation_gwh_pcs:Q',
    tooltip=['annee', 'consommation_gwh_pcs']
).properties(
    title=f"Tendance de la consommation de GNC pour {selected_region}",
    width=700,
    height=400
)
st.altair_chart(trend_chart, use_container_width=True)
st.write("""Nous pouvons voir que chaque région a une consommation de GNC différente. Cela peut être dû à plusieurs facteurs, notamment la population, le nombre de stations-service, la disponibilité des véhicules alimentés au GNC, etc.
La consommation est généralement croissante, mise à part quelques région qui diminue dans les années 2015-2017 puis qui remonte.""")

st.write("""
Le graphique circulaire représente la répartition de la consommation de GNC par région pour l'année sélectionnée.
Cela donne une idée claire de la contribution de chaque région à la consommation totale:
""")

pie_chart = alt.Chart(df[df['annee'] == year1]).mark_arc(innerRadius=50).encode(
    theta='consommation_gwh_pcs:Q',
    color='region:N',
    tooltip=['region', 'consommation_gwh_pcs']
).properties(
    title=f"Répartition de la consommation de GNC par région en {year1}",
    width=400,
    height=400
)
st.altair_chart(pie_chart, use_container_width=True)

st.write("""
Ci-dessous, vous trouverez quelques statistiques descriptives sur la consommation de GNC pour l'année sélectionnée.
Cela inclut la moyenne, la médiane, les valeurs minimales et maximales, etc.
""")

st.subheader(f"Statistiques descriptives pour {year1}")
st.write(df[df['annee'] == year1]['consommation_gwh_pcs'].describe())

hist_chart = alt.Chart(df[df['annee'] == year1]).mark_bar().encode(
    alt.X("consommation_gwh_pcs:Q", bin=alt.Bin(
        maxbins=30), title="Consommation (GWh PCS)"),
    y='count()'
).properties(
    title=f"Distribution de la consommation de GNC en {year1}",
    width=700,
    height=400
)
st.altair_chart(hist_chart, use_container_width=True)

st.write("""
Le tableau ci-dessous présente les trois régions avec la consommation la plus élevée et les trois régions avec la consommation la plus faible de GNC pour l'année sélectionnée.
""")

st.subheader(f"Top 3 des régions consommatrices en {year1}")
top_regions = df[df['annee'] == year1].nlargest(3, 'consommation_gwh_pcs')
st.write(top_regions[['region', 'consommation_gwh_pcs']])

st.subheader(f"3 régions les moins consommatrices en {year1}")
bottom_regions = df[df['annee'] == year1].nsmallest(3, 'consommation_gwh_pcs')
st.write(bottom_regions[['region', 'consommation_gwh_pcs']])

st.write("""
La variation annuelle montre comment la consommation de GNC a changé d'une année à l'autre pour chaque région. 
Une barre verte indique une augmentation de la consommation par rapport à l'année précédente, tandis qu'une barre rouge indique une diminution: comme par exemple la Bourgogne Franche Conté entre 2014 et 2017:
""")

df_sorted = df.sort_values(by=['region', 'annee'])
df_sorted['variation'] = df_sorted.groupby(
    'region')['consommation_gwh_pcs'].pct_change() * 100

# Filtrer uniquement pour les années sélectionnées
df_years = df_sorted[df_sorted['annee'].isin([year1, year2])]

# Calculer la variation pour les deux années sélectionnées
df_variation = df_years.pivot(
    index='region', columns='annee', values='consommation_gwh_pcs').reset_index()
df_variation['variation'] = (
    (df_variation[year2] - df_variation[year1]) / df_variation[year1]) * 100

variation_chart = alt.Chart(df_variation).mark_bar().encode(
    x='region:N',
    y=alt.Y('variation:Q', title="Variation annuelle (%)"),
    color=alt.condition(
        alt.datum.variation > 0,
        alt.value('green'),
        alt.value('red')
    ),
    tooltip=['region', 'variation']
).properties(
    title=f"Variation annuelle de la consommation de GNC entre {year1} et {year2}",
    width=700,
    height=400
)
st.altair_chart(variation_chart, use_container_width=True)

st.write("Nous pouvons analyser en 3D la consommation de GNC par région:")
st.write("Cartographie 3D de la consommation de GNC par région:")

df_map = df[df['annee'] == year1]

layer = pdk.Layer(
    'ColumnLayer',
    data=df_map,
    get_position=['longitude', 'latitude'],

    get_elevation='consommation_gwh_pcs*10',
    elevation_scale=100,
    radius=5000,

    get_fill_color=[255, 140, 0, 150],
    pickable=True,
    opacity=0.6
)

view_state = pdk.ViewState(
    latitude=df_map['latitude'].mean(),
    longitude=df_map['longitude'].mean(),
    zoom=5,
    min_zoom=5,
    max_zoom=15,
    pitch=40.5,
    bearing=-27.36
)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

st.write("Une facon plus complexe mais plus compréhensible est d'affiché une heatmap. On peut y voir que l'ile de France à une croissance beaucoup plus forte que les autres régions, comme la normandie qui stagne à des valeurs faibles:")
heatmap = alt.Chart(df).mark_rect().encode(
    x='region:N',
    y='annee:O',
    color=alt.Color('consommation_gwh_pcs:Q',
                    scale=alt.Scale(scheme="blueorange"),
                    title='Consommation (GWh PCS)'),
    tooltip=['region', 'annee', 'consommation_gwh_pcs']
).properties(
    title="Carte de chaleur des consommations par année et par région",
    width=700,
    height=400
)
st.altair_chart(heatmap, use_container_width=True)


data = df
regions = gpd.read_file('regions-20180101.shp')

regions['code_insee'] = regions['code_insee'].astype(str)
data['code_insee_region'] = data['code_insee_region'].astype(str)

merged_data = regions.merge(
    data, left_on='code_insee', right_on='code_insee_region')


regions_to_remove = ['Guadeloupe', 'Martinique',
                     'Guyane', 'La Réunion', 'Mayotte']
merged_data_metro = merged_data[~merged_data['nom'].isin(regions_to_remove)]

placeholder = st.empty()

years = sorted(df['annee'].unique())


def get_merged_data_for_year(year, df, regions):
    data_year = df[df['annee'] == year]
    merged_data = regions.merge(
        data_year, left_on='code_insee', right_on='code_insee_region')
    merged_data_metro = merged_data[~merged_data['nom'].isin(
        regions_to_remove)]
    return merged_data_metro


merged_data_metro = get_merged_data_for_year(year1, df, regions)

fig, ax = plt.subplots(figsize=(15, 15))
vmin = df['consommation_gwh_pcs'].min()
vmax = df['consommation_gwh_pcs'].max()
merged_data_metro.plot(column='consommation_gwh_pcs',
                       cmap='coolwarm',
                       linewidth=0.8,
                       edgecolor='black',
                       ax=ax,
                       legend=True,
                       vmin=vmin,
                       vmax=vmax)
ax.set_title(
    f'Consommation de GNC par région en France métropolitaine ({year1})', fontsize=15)

st.pyplot(fig)


df = pd.read_csv('consommation-regionale-gnc.csv', delimiter=';')

df[['index', 'annee']] = df.iloc[:, 0].str.split(',', 1, expand=True)
df['annee'] = df['annee'].str.replace('"', '').astype(int)
df.drop(columns=[df.columns[0], 'index', 'centroid'], inplace=True)

df_race = df.pivot(index='annee', columns='region',
                   values='consommation_gwh_pcs')

bcr.bar_chart_race(
    df=df_race, title='Consommation de GNC par région et par année', filename='bcr_race.gif')
st.image('bcr_race.gif', caption='Consommation de GNC par région et par année',
         use_column_width=True)


st.write(f"Cependant, la consommation de GNC par habitant est un meilleur indicateur de la consommation de GNC par région. Cela permet de comparer les régions de manière plus équitable, car les régions plus peuplées consommeront plus de GNC que les régions moins peuplées.")

population_data = pd.read_csv('donnees_regions.csv', delimiter=';')

regions['code_insee'] = regions['code_insee'].astype(int)
df['code_insee_region'] = df['code_insee_region'].astype(int)

merged_df = df.merge(
    population_data, left_on='code_insee_region', right_on='CODREG', how='left')

merged_df['consommation_per_capita'] = merged_df['consommation_gwh_pcs'] / \
    merged_df['PMUN'] * 1e6

merged_gdf = regions.merge(merged_df, left_on='code_insee', right_on='CODREG')

merged_gdf_selected_year = merged_gdf[merged_gdf['annee'] == year1]

st.write(
    f"Cartographie de la consommation de GNC par habitant par région pour l'année {year1}:")
fig, ax = plt.subplots(figsize=(15, 15))
merged_gdf_selected_year.plot(column='consommation_per_capita',
                              cmap='coolwarm',
                              linewidth=0.8,
                              edgecolor='black',
                              ax=ax,
                              legend=True,
                              legend_kwds={'label': f"Consommation de GNC (kWh par habitant) en {year1}"})
ax.set_title(
    f'Consommation de GNC par habitant par région en France ({year1})', fontsize=15)
plt.axis('off')
st.pyplot(fig)


st.write(f"En conclusion, la consommation de GNC en France affiche une évolution positive, certaines régions adoptant cette source d'énergie plus rapidement que d'autres. Comprendre les facteurs qui influencent ces tendances est essentiel pour encourager une adoption plus large du GNC à l’avenir.")

st.write("""
Merci d'avoir utilisé ce tableau de bord pour explorer la consommation de GNC par région en France.
N'hésitez pas à utiliser les filtres pour obtenir des informations plus détaillées.
""")