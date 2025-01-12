import streamlit as st

def home_page():
    # Title and Welcome Section with Centered Alignment
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            color: #4CAF50;
            margin-bottom: 1rem;
        }
        .sub-title {
            font-size: 1.5rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        </style>
        <div class="main-title">🌟 Disease Dashboard Home</div>
        <div class="sub-title">Explore trends, analyze patterns, and gain insights with our interactive geospatial app.</div>
        """,
        unsafe_allow_html=True,
    )

    # Visual Separator
    st.markdown("---")

    # Features Overview Section
    st.header("📖 Features Overview")
    st.markdown(
        """
        Discover what each page in the dashboard offers:
        """
    )

    # Display features in a 3-column layout
    features = [
        {
            "title": "📊 Main Page",
            "description": (
                "Visualize disease trends for a specific year and disease. "
                "Upload your CSV and GeoJSON files, choose the year and disease, "
                "and view a choropleth map with detailed statistics."
            ),
        },
        {
            "title": "🔍 Compare Years",
            "description": (
                "Compare disease trends across a range of years. "
                "See multiple maps in a grid view, analyze differences, and export all visualizations together."
            ),
        },
        {
            "title": "📈 Percentage Analysis",
            "description": (
                "View the percentage contribution of cases from each region relative to the national total. "
                "This feature provides insights into the proportional distribution of cases."
            ),
        },
    ]

    cols = st.columns(3)
    for i, feature in enumerate(features):
        with cols[i]:
            st.markdown(f"### {feature['title']}")
            st.write(feature["description"])

    # Another Separator
    st.markdown("---")

    # Instructions Section
    st.header("📋 How to Use the Dashboard")
    st.markdown(
        """
        Follow these steps to explore the data:
        
        1. **Upload Data**: Use the sidebar to upload the required data files:
           - A CSV file containing disease data.
           - A GeoJSON file for the geographical boundaries.
        2. **Select Options**: Choose the year, disease, and other settings from the sidebar controls.
        3. **Explore Maps**: Navigate to different pages to explore various analyses:
           - **Main Page**: Focus on a single year and disease.
           - **Compare Years**: Compare data across multiple years in a grid format.
           - **Percentage Analysis**: Analyze percentage contributions for each region.
        4. **Export Results**: Download maps for further use or reporting purposes.
        """
    )

    # Include an expandable section for tips
    with st.expander("💡 Tips for Using the Dashboard"):
        st.markdown(
            """
            - Ensure the CSV and GeoJSON files have matching region names for accurate mapping.
            - Use the color scale picker on the sidebar to customize the map visuals.
            - Hover over regions on the map for detailed case information.
            """
        )

    

    # Footer with Buttons and Contact Information
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    st.markdown(
        """
        <div style="text-align: center; background-color: #86A788; padding: 20px; border-radius: 10px;" >
            Need Help? Reach out to our support team at
            <a href="mailto:support@example.com">support@example.com</a>.
        </div>
        """,
        unsafe_allow_html=True,
    )
