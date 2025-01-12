##NDMC
# Disease Dashboard

This project is an interactive disease visualization dashboard built with **Streamlit**. The dashboard is designed to analyze and visualize disease-related data across Indian states using CSV and GeoJSON files.

---

## Features

- **Interactive Map Visualization**: View disease data on a map for selected years and diseases.
- **Year Comparison**: Compare disease statistics over a range of years with side-by-side maps.
- **Customizable Color Scales**: Choose from preset or custom color scales for map visualization.
- **Percentage Maps**: Display disease data as percentages for easier interpretation.
- **File Upload Support**: Upload custom CSV and GeoJSON files for personalized analyses.
- **Responsive Design**: Optimized for various screen sizes.

---

Element   | Description
:--------:|:-----------
/.streamlit  | 
/.streamlit/├──config.toml | This contains some styling used as global style of the project
/dashboard | This folder contains the files for the project
/dashboard/__init__.pt | The file imports various modules from the same package (modules within the same directory) and exposes them\
/dashboard/card.py |  Can use to provide description and photos of the disease in question 
/dashboard/datagrid.py | Will use to display the data in a tabular form 
/dashboard/india_state_geo.json | used to generate the map
/dashboard/map.py | map component
/dashboard/pie.py | pie chart component
/dashboard/player.py | Maybe will be used to have a video of instructions on how to run the file 
/dashboard/radar.py | Radar chart component
/streamlit_app.py | Main page file
## Installation

### Prerequisites

1. Python (>= 3.8)
2. Git
3. Virtual Environment (optional but recommended)

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Cameronmeow/NDMC.git
   cd NDMC
   ```

2. **Set Up a Virtual Environment (Optional)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Required Packages**
   ```bash
   pip install streamlit 
   pip install pandas
   pip install pathlib
   pip install streamlit_elements
   pip install types 
   pip install geopandas
   pip install plotly.express
   pip install abc
   pip install uuid
   pip install contextlib
   pip install -U kaleido
   ```

4. **Add the `DiseaseData.csv` and `india_telengana.geojson` Files**
   - Place the dataset (`DiseaseData.csv`) and GeoJSON file (`india_telengana.geojson`) in the root directory or provide their paths in the app.

5. **Run the Application**
   ```bash
   python -m streamlit run streamlit_app.py
   ```

---

## Usage

### Running the Dashboard

1. Open your browser and go to the URL displayed in your terminal (default is `http://localhost:8501`).
2. Use the sidebar to upload your files and adjust settings.

### Sidebar Features

- **File Upload**: Upload your disease data CSV and GeoJSON files.
- **Year Selection**: Choose a specific year or a range of years to visualize.
- **Disease Selection**: Pick a disease to analyze.
- **Color Scale Picker**: Select a color scale for better visualization.

### Main Pages

1. **Main Page**:
   - Displays a single map for the selected year and disease.
2. **Compare Years**:
   - Compare disease data across a range of years.
3. **Percentage Page**:
   - Visualize disease data as percentages for better comparisons.

---

## File Format Guidelines

### CSV File (`DiseaseData.csv`)

- **Columns**:
  - `States/UTs`: Name of the states/UTs.
  - `Short Form`: Abbreviations of states/UTs.
  - `Year-Disease`: Columns in the format `Year-Disease` (e.g., `2008-Lymphoedema`).
  - `Cases`: Number of cases for each disease and year.

**Example:**
```csv
States/UTs,Short Form,2008-Lymphoedema,2009-Lymphoedema
Andhra Pradesh,AP,100,120
Telangana,TS,80,90
```

### GeoJSON File (`india_telengana.geojson`)

- Should contain boundary information for Indian states/UTs.
- Must have a `feature` property with state names matching the `States/UTs` column in the CSV file.

**Example:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Andhra Pradesh"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [ ... ]
      }
    }
  ]
}
```

---

## Code Structure
- **dashboard**: Contains map files 
- **`streamlit_app.py`**: Contains the `DiseaseMap`, `DiseasePercentMap`, and `GridMap` classes for rendering maps.

---

## Development

### Adding Features

1. Clone the repository and set up your environment.
2. Modify or add components in `map.py` or `streamlit_app.py` or `map_percent.py ` or `gridmap.py`.
3. Test changes locally before committing.

### Contributing

- Fork the repository.
- Create a feature branch.
- Submit a pull request.

---

## Troubleshooting

1. **Slow Map Rendering**:
   - Ensure you have a high-performance machine.
   - Reduce the number of data points in your dataset.
   - Use Streamlit's caching (`@st.cache_data`).

2. **File Upload Issues**:
   - Ensure the CSV and GeoJSON files are in the correct format.

---

## Acknowledgments

- **Streamlit**: For making data apps easy to build.
- **Seaborn** and **Matplotlib**: For beautiful visualizations.
- **Open Source Libraries**: GeoJSON parsing and data processing.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact

For queries or contributions, contact:
- **Email**: [22b2463@iitb.ac.in]
- **GitHub**: [https://github.com/Cameronmeow/NDMC]
