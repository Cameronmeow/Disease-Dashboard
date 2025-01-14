import streamlit as st

def navbar(options):
    # Define navbar styling
    st.markdown("""
        <style>
            .navbar-container {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 10px;
                margin-bottom: 20px;
                padding: 10px;
                background-color: #F6F4F0;
                border-radius: 8px;
            }

            .navbar-button {
                background-color: #F6F4F0;
                color: #4DA1A9;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                box-shadow: 0 5px 6px #4DA1A9;
                transition: background-color 0.3s, color 0.3s, box-shadow 0.3s;
            }

            .navbar-button:hover {
                background-color: #4DA1A9;
                color: white;
            }

            .navbar-button.active {
                background-color: #2E7D32;
                color: white;
                box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
            }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state for navbar
    if "selected_nav" not in st.session_state:
        st.session_state.selected_nav = options[0]  # Default selected option

    # Create navbar
    st.markdown('<div class="navbar-container">', unsafe_allow_html=True)

    # Loop through options and display buttons
    for option in options:
        is_active = "active" if st.session_state.selected_nav == option else ""
        if st.button(option, key=f"nav_button_{option}"):
            st.session_state.selected_nav = option

        # Add button styling
        st.markdown(f"""
            <button class="navbar-button {is_active}">{option}</button>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Return selected option
    return st.session_state.selected_nav


def home_page():
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
    st.markdown("---")
    st.header("📖 Features Overview")
    st.markdown("Discover what each page in the dashboard offers:")
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
    st.markdown("---")
    st.header("📋 How to Use the Dashboard")
    st.markdown(
        """
        1. **Upload Data**: Use the sidebar to upload the required data files.
        2. **Select Options**: Choose the year, disease, and other settings.
        3. **Explore Maps**: Navigate to different pages for detailed analyses.
        """
    )
    with st.expander("💡 Tips for Using the Dashboard"):
        st.markdown(
            """
            - Ensure the CSV and GeoJSON files match for accurate mapping.
            - Use the sidebar controls to customize your view.
            - Hover over map regions for detailed case data.
            """
        )
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; background-color: #F6F4F0; padding: 20px; border-radius: 10px;">
            Need Help? Reach out to <a href="mailto:22b2463@iitb.ac.in">22b2463@iitb.ac.in</a>.
        </div>
        """,
        unsafe_allow_html=True,
    )


def main_page():
    st.title("📊 Main Page")
    st.write("Here you can visualize trends for a specific year and disease.")


def compare_years_page():
    st.title("🔍 Compare Years")
    st.write("Compare trends across a range of years in a grid view.")


def percentage_analysis_page():
    st.title("📈 Percentage Analysis")
    st.write("View the percentage contribution of cases regionally.")


def main():
    st.set_page_config(
        page_title="Disease Dashboard",
        page_icon="🌟",
        layout="wide",
    )
    pages = ["Home Page", "Main Page", "Compare Years", "Percentage Analysis"]
    selected_page = navbar(pages)

    if selected_page == "Home Page":
        home_page()
    elif selected_page == "Main Page":
        main_page()
    elif selected_page == "Compare Years":
        compare_years_page()
    elif selected_page == "Percentage Analysis":
        percentage_analysis_page()


if __name__ == "__main__":
    main()
