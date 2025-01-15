import pandas as pd
import geopandas as gpd
import plotly.express as px
import streamlit as st
from io import BytesIO
import zipfile


class MapMatrix:
    def __init__(self):
        pass

    def create_map(self, csv_path, shapefile_path, year, disease, state_name, color_scale):
        # Load data
        data = pd.read_csv(csv_path)
        data["States/UTs"] = data["States/UTs"].str.strip()
        data["Short Form"] = data["Short Form"].str.strip()

        # Load shapefile
        gdf = gpd.read_file(shapefile_path)
        gdf["ST_NM"] = gdf["ST_NM"].str.strip()  # Ensure state names match

        # Melt and preprocess data
        data_melted = data.melt(
            id_vars=["States/UTs", "Short Form"], var_name="Year-Disease", value_name="Cases"
        )
        data_melted[["Year", "Disease"]] = data_melted["Year-Disease"].str.split("-", expand=True)
        data_melted.drop(columns=["Year-Disease"], inplace=True)

        # Merge and filter data
        merged = gdf.merge(
            data_melted, left_on="ST_NM", right_on="States/UTs", how="left"
        )
        filtered_data = merged[(merged["Year"] == str(year)) & (merged["Disease"] == disease)]

        # Add text for hover information
        filtered_data["text"] = (
            filtered_data[state_name] + "<br>" + filtered_data["Cases"].astype(str)
        )

        # Calculate total cases
        total_cases = filtered_data["Cases"].sum()
        state_count = filtered_data["Cases"].notna().sum()
        national_average = total_cases / state_count if state_count > 0 else 0

        # Plot the choropleth map
        fig = px.choropleth(
            filtered_data,
            geojson=filtered_data.geometry,
            locations=filtered_data.index,
            color="Cases",
            color_continuous_scale=color_scale,
            hover_name="ST_NM",
            labels={"Cases": "Number of Cases"},
            title=f"{disease} Cases in {year} - Total Cases: {total_cases:,}"
        )

        # Add text labels to each state
        for _, row in filtered_data.iterrows():
            if pd.notna(row["Cases"]):
                fig.add_scattergeo(
                    lon=[row.geometry.centroid.x],
                    lat=[row.geometry.centroid.y],
                    text=row["text"],
                    mode="text",
                    showlegend=False,
                    textfont=dict(family="Arial, sans-serif", size=12, color="black"),
                )

        # Update map properties
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(
            title={
                "text": f"{disease} Cases in {year} - Total Cases: {total_cases:,}",
                "y": 0.93,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            annotations=[
                dict(
                    text=f"National Average<br> <b>{national_average:.2f} cases</b>",
                    x=0.8,
                    y=0.2,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=16, color="black", family="Arial, sans-serif"),
                ),
            ],
            title_font=dict(size=20, family="Arial, sans-serif", color="black"),
            margin=dict(l=0, r=0, t=0, b=0),
            width=600,
            height=400,
        )

        return fig

    def render_maps_grid(self, csv_path, shapefile_path, start_year, end_year, disease, state_name, color_scale):
        years = list(range(start_year, end_year + 1))
        fig_list = []
        col1, col2 = st.columns(2)

        for idx, year in enumerate(years):
            fig = self.create_map(csv_path, shapefile_path, year, disease, state_name, color_scale)
            fig_list.append(fig)

            # Display in a 2x2 grid
            if idx % 2 == 0:
                with col1:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                with col2:
                    st.plotly_chart(fig, use_container_width=True)

        return fig_list

    
