import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.append('src')
from config import *
from utils import calculate_health_indicators

st.set_page_config(page_title="WORLDPOP Dashboard", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_data():
    if not os.path.exists(PROCESSED_DATA_FILE):
        st.error("Processed data file not found. Please run the data pipeline first.")
        st.stop()
    df = pd.read_parquet(PROCESSED_DATA_FILE)
    return df

def filter_data(df, countries, age_groups, sexes):
    filtered = df[
        (df['country_code'].isin(countries)) &
        (df['age_group'].isin(age_groups)) &
        (df['sex'].isin(sexes))
    ].copy()
    return filtered

def create_population_pyramid(df, country_code):
    country_data = df[df['country_code'] == country_code].copy()
    male_data = country_data[country_data['sex'] == 'M'].sort_values('age_order')
    female_data = country_data[country_data['sex'] == 'F'].sort_values('age_order')

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=male_data['age_group_label'],
        x=male_data['population'],
        name='Male',
        orientation='h',
        marker_color='blue',
        hovertemplate='<b>Male</b><br>Age: %{y}<br>Population: %{text}<extra></extra>',
        text=[f"{abs(x):,.0f}" for x in male_data['population']]
    ))

    fig.add_trace(go.Bar(
        y=female_data['age_group_label'],
        x=female_data['population'],
        name='Female',
        orientation='h',
        marker_color='pink',
        hovertemplate='<b>Female</b><br>Age: %{y}<br>Population: %{text}<extra></extra>',
        text=[f"{abs(x):,.0f}" for x in female_data['population']]
    ))

    max_pop = max(male_data['population'].max(), female_data['population'].max())
    fig.update_layout(
        title=f'Population Pyramid for {COUNTRIES[country_code]} (2025)',
        barmode='overlay',
        bargap=0.1,
        height=600,
        xaxis=dict(
            title='Population',
            tickformat=',',
            tickvals=[-max_pop, -max_pop/2, 0, max_pop/2, max_pop],
            ticktext=[f"{abs(x/1e6):.1f}M" for x in [-max_pop, -max_pop/2, 0, max_pop/2, max_pop]]
        ),
        yaxis_title='Age Group',
        hovermode='y unified',
    )
    return fig

def create_age_distribution_chart(df):
    age_totals = df.groupby(['age_group_label', 'age_order'])['population'].sum().reset_index()
    age_totals = age_totals.sort_values('age_order')
    
    fig = px.bar(
        age_totals,
        x='age_group_label',
        y='population',
        title='Population Distribution by Age Group',
        labels={'age_group_label': 'Age Group', 'population': 'Population'},
        color='population',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=400,
        showlegend=False
    )
    
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Population: %{y:,.0f}<extra></extra>'
    )
    
    return fig


def create_sex_comparison_chart(df):
    sex_totals = df.groupby(['country_name', 'sex_label'])['population'].sum().reset_index()
    
    fig = px.bar(
        sex_totals,
        x='country_name',
        y='population',
        color='sex_label',
        barmode='group',
        title='Population by Sex and Country',
        labels={'country_name': 'Country', 'population': 'Population', 'sex_label': 'Sex'},
        color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'}
    )
    
    fig.update_layout(height=400)
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y:,.0f}<extra></extra>'
    )
    
    return fig


def main():
    st.title("WORLDPOP Dashboard")
    st.markdown("""
    Interactive visualization of age and sex structured population data for Kenya and Uganda.
    """)
    with st.spinner("Loading data..."):
        df = load_data()
    st.sidebar.header("Filters")
    selected_countries = st.sidebar.multiselect("Select Countries", options=list(COUNTRIES.keys()), default=list(COUNTRIES.keys()), format_func=lambda x: COUNTRIES[x])
    selected_age_groups = st.sidebar.multiselect("Select Age Groups", options=AGE_GROUPS, default=AGE_GROUPS, format_func=lambda x: AGE_GROUP_LABELS[x])
    selected_sexes = st.sidebar.multiselect("Select Sex", options=SEX_CATEGORIES, default=SEX_CATEGORIES, format_func=lambda x: "Male" if x == 'M' else "Female")
    filtered_df = filter_data(df, selected_countries, selected_age_groups, selected_sexes)
    
    st.header("Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_population = filtered_df['population'].sum()
    male_population = filtered_df[filtered_df['sex'] == 'M']['population'].sum()
    female_population = filtered_df[filtered_df['sex'] == 'F']['population'].sum()
    
    col1.metric("Total Population", f"{total_population:,.0f}")
    col2.metric("Male Population", f"{male_population:,.0f}", f"{male_population/total_population*100:.1f}%")
    col3.metric("Female Population", f"{female_population:,.0f}", f"{female_population/total_population*100:.1f}%")
    col4.metric("Sex Ratio (M/100F)", f"{(male_population/female_population*100):.1f}" if female_population > 0 else "N/A")
    
    st.header("Public Health Indicators")
    
    indicators = calculate_health_indicators(filtered_df)
    
    if indicators:
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Children (0-14)", f"{indicators['children_pct']:.1f}%", help="Proportion of population aged 0-14 years")
        col2.metric("Youth (15-24)", f"{indicators['youth_pct']:.1f}%", help="Proportion of population aged 15-24 years")
        col3.metric("Working Age (25-59)", f"{indicators['working_age_pct']:.1f}%", help="Proportion of population aged 25-59 years")
        col4.metric("Elderly (60+)", f"{indicators['elderly_pct']:.1f}%", help="Proportion of population aged 60+ years")
        
        if 'dependency_ratio' in indicators:
            st.info(f"""Dependency Ratio: {indicators['dependency_ratio']:.1f} This indicates that for every 100 people 
            of working age (25-59), there are {indicators['dependency_ratio']:.0f} dependents (children and elderly).
            A lower ratio suggests a larger working-age population relative to dependents.
            """)
    st.header("Visualizations")
    if len(selected_countries) > 0:
        st.subheader("Population Pyramids")
        
        pyramid_cols = st.columns(len(selected_countries))
        
        for idx, country_code in enumerate(selected_countries):
            with pyramid_cols[idx]:
                fig = create_population_pyramid(df, country_code)
                st.plotly_chart(fig, use_container_width=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_age_distribution_chart(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_sex_comparison_chart(filtered_df), use_container_width=True)
    
    with st.expander("View Raw Data"):
        display_df = filtered_df[['country_name', 'sex_label', 'age_group_label', 'population']].copy()
        if 'age_order' in filtered_df.columns:
            display_df = display_df.assign(age_order=filtered_df['age_order']).sort_values(['country_name', 'age_order', 'sex_label'])
        else:
            display_df = display_df.sort_values(['country_name', 'sex_label'])
        st.dataframe(
            display_df[['country_name', 'sex_label', 'age_group_label', 'population']].reset_index(drop=True),
            use_container_width=True
        )

if __name__ == "__main__":
    main()
