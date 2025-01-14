import json
import streamlit as st
import pandas as pd
from io import BytesIO
from matplotlib.colors import to_rgb
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from dashboard import DiseaseMap, DiseasePercentMap, GridMap, MapMatrix, home_page

# Cache loading data
@st.cache_data
def load_disease_data(csv_file):
    diseasedata = pd.read_csv(csv_file)
    df_melted = diseasedata.melt(
        id_vars=["States/UTs", "Short Form"],
        var_name="Year-Disease",
        value_name="Cases"
    )
    df_melted[["Year", "Disease"]] = df_melted["Year-Disease"].str.split("-", expand=True)
    df_melted.drop(columns=["Year-Disease"], inplace=True)
    df_melted["States/UTs"] = df_melted["States/UTs"].str.strip()
    df_melted["Short Form"] = df_melted["Short Form"].str.strip()
    return df_melted

@st.cache_data
def load_geojson_data(geojson_file):
    return json.load(geojson_file)

def show_color_scale(colors):
    rgb_colors = [to_rgb(color) for color in colors]
    rgb_array = [rgb_colors]
    fig, ax = plt.subplots(figsize=(6, 0.5))
    ax.imshow(rgb_array, extent=[0, len(colors), 0, 1], aspect="auto")
    ax.axis("off")
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
    buf.seek(0)
    plt.close(fig)
    return buf

def preset_color_picker():
    preset_scales = {
        "Pink-White": ["#EEEEEE", "#E73879"],
        "Green-Yellow": ["#00ff00", "#ffff00"],
        "Purple-Orange": ["#800080", "#ffa500"],
        "Blues": sns.color_palette("Blues", 10).as_hex(),
        "Coolwarm": sns.color_palette("coolwarm", 10).as_hex(),
        "Viridis": sns.color_palette("viridis", 10).as_hex(),
        "hls": sns.color_palette("hls", 8).as_hex()
    }

    selected_scale = st.sidebar.selectbox(
        "Select a Preset Color Scale",
        options=list(preset_scales.keys()),
    )
    st.sidebar.image(show_color_scale(preset_scales[selected_scale]), use_container_width=True)
    return preset_scales[selected_scale]

def main_page(color_scale, year, disease, state_name, csv_file):
    with st.spinner(f"Rendering map for {year}, {disease}..."):
        map_component = DiseaseMap()
        map_component(
            csv_path=csv_file,
            shapefile_path='./Admin2.shp',
            year=year,
            disease=disease,
            state_name=state_name,
            color_scale=color_scale
        )

def compare_years_page(start_year, end_year, disease, state_name, color_scale):
    # with st.spinner(f"Rendering map for {year}, {disease}..."):
        st.markdown("### Compare Disease Data Across Selected Years")
        disease_map = GridMap()
        disease_map.render_maps(
            csv_path="DiseaseData.csv",
            shapefile_path='./Admin2.shp',
            start_year=start_year,
            end_year=end_year,
            disease=disease,
            state_name=state_name,
            color_scale=color_scale,
        )

def map_matrix_page(start_year, end_year, disease, state_name, color_scale):
    # with st.spinner(f"Rendering map for {year}, {disease}..."):
        st.markdown("### Compare Disease Data Across Selected Years (Grid View)")
        disease_map = MapMatrix()
        disease_map.render_maps_grid(
            csv_path="DiseaseData.csv",
            shapefile_path='./Admin2.shp',
            start_year=start_year,
            end_year=end_year,
            disease=disease,
            state_name=state_name,
            color_scale=color_scale,
        )

def percent_page(csv_path, color_scale, year, disease, state_name):
    with st.spinner(f"Rendering map for {year}, {disease}..."):
        map_component = DiseasePercentMap()
        map_component(
            csv_path=csv_path,
            shapefile_path='./Admin2.shp',
            year=year,
            disease=disease,
            state_name=state_name,
            color_scale=color_scale
        )

def main():
    st.sidebar.title("Disease Map Settings")
    csv_file = st.sidebar.file_uploader("Upload Disease Data CSV", type="csv")

    # Create the navbar
    
    selected_page = option_menu(
        menu_title="Main Menu",
        options=[
            "Home Page",
            "Single Graph with Numbers",
            "Single Graph with Percentage",
            "Compare Years one by one",
            "Compare Years in a grid"
        ],
        # icons=["house", "bar-chart", "percent", "calendar3", "grid"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if selected_page == "Home Page":
        home_page()

    elif csv_file:
        try:
            diseasedata = load_disease_data(csv_file)

            year = st.sidebar.slider(
                "Select a year:",
                min_value=int(diseasedata["Year"].min()),
                max_value=int(diseasedata["Year"].max()),
                value=int(diseasedata["Year"].min())
            )

            state_name = st.sidebar.selectbox(
                "Select State Name Type", ['States/UTs', 'Short Form']
            )

            start_year = st.sidebar.number_input(
                "Start Year",
                min_value=int(diseasedata["Year"].min()),
                value=int(diseasedata["Year"].min())
            )
            end_year = st.sidebar.number_input(
                "End Year",
                min_value=start_year,
                value=start_year + 3
            )

            if start_year > end_year:
                st.sidebar.error("Start Year cannot be greater than End Year.")

            disease = st.sidebar.selectbox(
                "Select Disease", diseasedata["Disease"].unique()
            )

            color_scale = preset_color_picker()

            if selected_page == "Single Graph with Numbers":
                main_page(color_scale, str(year), disease, state_name, csv_file)
            elif selected_page == "Single Graph with Percentage":
                percent_page(csv_file, color_scale, str(year), disease, state_name)
            elif selected_page == "Compare Years one by one":
                compare_years_page(start_year, end_year, disease, state_name, color_scale)
            elif selected_page == "Compare Years in a grid":
                map_matrix_page(start_year, end_year, disease, state_name, color_scale)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.info("Please upload the CSV file to proceed.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Disease Dashboard",
        page_icon="./ndmc_logo.png",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    main()
