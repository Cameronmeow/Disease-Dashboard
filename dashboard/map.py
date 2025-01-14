import pandas as pd
import geopandas as gpd
import plotly.express as px
import streamlit as st


class DiseaseMap:
    def __init__(self):
        pass

    def __call__(self, csv_path, shapefile_path, year, disease,state_name,color_scale):
        # Load CSV data
        data = pd.read_csv(csv_path)
        data["States/UTs"] = data["States/UTs"].str.strip()
        data["Short Form"] = data["Short Form"].str.strip()

        # Load Shapefile data
        gdf = gpd.read_file(shapefile_path)
        gdf["ST_NM"] = gdf["ST_NM"].str.strip()
        print(gdf['ST_NM'])
        # Melt and preprocess CSV data
        data_melted = data.melt(
            id_vars=["States/UTs", "Short Form"], var_name="Year-Disease", value_name="Cases"
        )
        data_melted[["Year", "Disease"]] = data_melted["Year-Disease"].str.split("-", expand=True)
        data_melted.drop(columns=["Year-Disease"], inplace=True)

        # Merge and filter data
        merged = gdf.merge(
            data_melted, left_on="ST_NM", right_on="States/UTs", how="left"
        )
        filtered_data = merged[(merged["Year"] == year) & (merged["Disease"] == disease)]

        # Add hover text
        filtered_data["text"] = (
            filtered_data[state_name] + "<br>" + filtered_data["Cases"].astype(str)
        )

        # Calculate total cases and national average
        total_cases = filtered_data["Cases"].sum()
        state_count = filtered_data["Cases"].notna().sum()
        national_average = total_cases / state_count if state_count > 0 else 0

        # Create choropleth map
        fig = px.choropleth(
            filtered_data,
            geojson=filtered_data.geometry,
            locations=filtered_data.index,
            color="Cases",
            color_continuous_scale=color_scale,
            hover_name="ST_NM",
            labels={"Cases": "Number of Cases"},
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
                    textfont=dict(family="Droid Sans, sans-serif", size=12, color="black"),
                )

        # Update map properties
        fig.update_geos(
            fitbounds="locations",
            visible=False,
        )

        # Update layout with title and annotations
        fig.update_layout(
            title={
                "text": f"{disease} Cases in {year} - Total Cases: {total_cases:,}",
                "y": 0.95,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            title_font=dict(
                size=30,
                family="Arial, sans-serif",
                color="black"
            ),
            annotations=[
                dict(
                    text=f"National Average<br><b>{national_average:.2f}</b> cases",
                    x=0.8,
                    y=0.2,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=20, color="black", family="Arial, sans-serif")
                ),
            ],
            geo=dict(
                fitbounds="locations",
                visible=False
            ),
            margin=dict(
                l=0, r=0, t=50, b=0
            ),
            width=1200,
            height=800,
        )

        # Render the map in Streamlit
        st.plotly_chart(fig, use_container_width=True)
