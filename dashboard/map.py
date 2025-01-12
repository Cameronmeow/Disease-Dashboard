import pandas as pd
import geopandas as gpd
import plotly.express as px
import streamlit as st


class DiseaseMap:
    def __init__(self):
        pass

    def __call__(self, csv_path, geojson_path, year, disease,state_name, color_scale):
        # Load data
        data = pd.read_csv(csv_path)
        data["States/UTs"] = data["States/UTs"].str.strip()
        data["Short Form"] = data["Short Form"].str.strip()
        gdf = gpd.read_file(geojson_path)
        gdf["NAME_1"] = gdf["NAME_1"].str.strip()

        # Melt and preprocess data
        data_melted = data.melt(
            id_vars=["States/UTs", "Short Form"], var_name="Year-Disease", value_name="Cases"
        )
        data_melted[["Year", "Disease"]] = data_melted["Year-Disease"].str.split("-", expand=True)
        data_melted.drop(columns=["Year-Disease"], inplace=True)

        # Merge and filter data
        merged = gdf.merge(
            data_melted, left_on="NAME_1", right_on="States/UTs", how="left"
        )
        filtered_data = merged[(merged["Year"] == year) & (merged["Disease"] == disease)]

        # Add text for hover information
        filtered_data["text"] = (
            filtered_data[state_name] + "<br>" + filtered_data["Cases"].astype(str)
        )

        
        # Calculate total cases
        total_cases = filtered_data["Cases"].sum()
        state_count = filtered_data["Cases"].notna().sum()
        national_average = total_cases / state_count if state_count > 0 else 0

        # Plot the choropleth map with labels, featureidkey, and projection
        fig = px.choropleth(
            filtered_data,
                geojson=filtered_data.geometry,
                locations=filtered_data.index,
                color="Cases",
                # title=f"{disease} Cases in {year}",
                color_continuous_scale=color_scale,
                hover_name="NAME_1",
                labels={"Cases": "Number of Cases"},
                title=f"{disease} Cases in {year} - Total Cases: {total_cases:,}"
        )
        total_cases = 0
            # Add text labels to each state
        for i, row in filtered_data.iterrows():
                total_cases += row["Cases"]
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
        # total_cases = sum()
        fig.update_layout(
            title={
                "text": f"{disease} Cases in {year} - Total Cases: {total_cases:,}",
                "y": 0.95,  # Position closer to the top
                "x": 0.5,   # Centered horizontally
                "xanchor": "center",
                "yanchor": "top",
            },
            title_font=dict(
                size=30,       # Larger font size for better visibility
                family="Arial, sans-serif",
                color="black"
            ),
            annotations=[
                dict(
                    text=f"National Average<br> <b>{national_average:.2f} cases",
                    x=0.8,  # Centered horizontally
                    y=0.2,  # Position just below the title
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=25, color="black", family="Arial, sans-serif")
                ),
                
            ],
            geo=dict(
                fitbounds="locations",
                visible=False
            ),
            margin=dict(
                l=0, r=0, t=0, b=0  # Increase top margin for the title
            ),
            width=1200,   # Adjust the width as needed
            height=1200   # Adjust the height as needed
        )
        # Render the map in Streamlit
        st.plotly_chart(fig,use_container_width=True)
