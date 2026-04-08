import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Crime Analytics Dashboard",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.25rem solid #1f77b4;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 📂 Load Data (safe)
@st.cache_data
def load_data():
    return pd.read_csv("clustered_crime_data.csv", nrows=50000)

df = load_data()

# 🎯 Sidebar Navigation with improved styling
st.sidebar.markdown('<div class="sidebar-header">🚔 Crime Analytics Dashboard</div>', unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "Select Analysis",
    ["📊 Overview", "📈 Crime Statistics", "🌍 Geographic Analysis", "⏱️ Temporal Patterns", "🧠 Dimensionality Reduction", "🤖 ML Model Tracking"],
    help="Choose the type of analysis you want to explore"
)

# Add data info in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Dataset Info")
st.sidebar.write(f"**Total Records:** {len(df):,}")
st.sidebar.write(f"**Date Range:** {df['Year'].min()} - {df['Year'].max()}")
st.sidebar.write(f"**Crime Types:** {df['Primary Type'].nunique()}")

# ================================
# 📊 OVERVIEW PAGE
# ================================
if page == "📊 Overview":
    st.markdown('<div class="main-header">📊 Crime Analytics Overview</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Crimes", f"{len(df):,}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Crime Types", df['Primary Type'].nunique())
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        arrest_rate = (df['Arrest'].sum() / len(df) * 100).round(1)
        st.metric("Arrest Rate", f"{arrest_rate}%")
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Years Covered", f"{df['Year'].max() - df['Year'].min() + 1}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Top crime types
    st.subheader("🔥 Top 10 Crime Types")
    crime_counts = df['Primary Type'].value_counts().head(10)

    fig = px.bar(
        x=crime_counts.values,
        y=crime_counts.index,
        orientation='h',
        labels={'x': 'Number of Crimes', 'y': 'Crime Type'},
        color=crime_counts.values,
        color_continuous_scale='Reds'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Crime distribution by year
    st.subheader("📈 Crime Trends Over Time")
    yearly_crimes = df['Year'].value_counts().sort_index()

    fig = px.line(
        x=yearly_crimes.index,
        y=yearly_crimes.values,
        markers=True,
        labels={'x': 'Year', 'y': 'Number of Crimes'}
    )
    fig.update_traces(line_color='#1f77b4', marker_color='#ff7f0e')
    st.plotly_chart(fig, use_container_width=True)


# ================================
# 📈 CRIME STATISTICS PAGE
# ================================
elif page == "📈 Crime Statistics":
    st.markdown('<div class="main-header">📈 Crime Statistics</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Crime Distribution", "Arrest Analysis", "Location Analysis"])

    with tab1:
        st.subheader("Crime Type Distribution")

        col1, col2 = st.columns(2)

        with col1:
            # Bar chart
            crime_counts = df['Primary Type'].value_counts().head(15)
            fig = px.bar(
                x=crime_counts.index,
                y=crime_counts.values,
                labels={'x': 'Crime Type', 'y': 'Count'},
                color=crime_counts.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Pie chart
            fig = px.pie(
                values=crime_counts.values,
                names=crime_counts.index,
                title="Crime Type Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Arrest Rate Analysis")

        # Arrest rate by crime type
        arrest_by_type = df.groupby('Primary Type')['Arrest'].mean().sort_values(ascending=False).head(15)

        fig = px.bar(
            x=arrest_by_type.index,
            y=arrest_by_type.values * 100,
            labels={'x': 'Crime Type', 'y': 'Arrest Rate (%)'},
            color=arrest_by_type.values,
            color_continuous_scale='Greens'
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Location-Based Analysis")

        # Top locations
        location_counts = df['Location Description'].value_counts().head(15)

        fig = px.bar(
            x=location_counts.values,
            y=location_counts.index,
            orientation='h',
            labels={'x': 'Number of Crimes', 'y': 'Location'},
            color=location_counts.values,
            color_continuous_scale='Purples'
        )
        st.plotly_chart(fig, use_container_width=True)


# ================================
# 🌍 GEOGRAPHIC ANALYSIS PAGE
# ================================
elif page == "🌍 Geographic Analysis":
    st.markdown('<div class="main-header">🌍 Geographic Crime Analysis</div>', unsafe_allow_html=True)

    # Filters
    col1, col2 = st.columns(2)

    with col1:
        selected_crime = st.selectbox(
            "Filter by Crime Type",
            ["All"] + list(df['Primary Type'].unique())
        )

    with col2:
        sample_size = st.slider("Sample Size", 500, 5000, 2000)

    # Filter data
    if selected_crime != "All":
        filtered_df = df[df['Primary Type'] == selected_crime].dropna(subset=['Latitude', 'Longitude'])
    else:
        filtered_df = df.dropna(subset=['Latitude', 'Longitude'])

    sample_df = filtered_df.sample(min(sample_size, len(filtered_df)))

    # Create map
    m = folium.Map(location=[41.87, -87.62], zoom_start=10)

    # Add markers
    for _, row in sample_df.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=3,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.6,
            popup=f"Crime: {row['Primary Type']}<br>Location: {row['Location Description']}"
        ).add_to(m)

    st_folium(m, width=800, height=600)


# ================================
# ⏱️ TEMPORAL PATTERNS PAGE
# ================================
elif page == "⏱️ Temporal Patterns":
    st.markdown('<div class="main-header">⏱️ Temporal Crime Patterns</div>', unsafe_allow_html=True)

    # Ensure Date column is datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Hour'] = df['Date'].dt.hour
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['Month'] = df['Date'].dt.month_name()

    tab1, tab2, tab3, tab4 = st.tabs(["Hourly Patterns", "Daily Patterns", "Monthly Patterns", "Seasonal Analysis"])

    with tab1:
        st.subheader("Crime Patterns by Hour")

        hourly = df['Hour'].value_counts().sort_index()

        fig = px.line(
            x=hourly.index,
            y=hourly.values,
            markers=True,
            labels={'x': 'Hour of Day', 'y': 'Number of Crimes'},
            title="Crimes by Hour"
        )
        fig.update_traces(line_color='#1f77b4', marker_color='#ff7f0e')
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Crime Patterns by Day of Week")

        daily = df['DayOfWeek'].value_counts()

        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily = daily.reindex(day_order)

        fig = px.bar(
            x=daily.index,
            y=daily.values,
            labels={'x': 'Day of Week', 'y': 'Number of Crimes'},
            color=daily.values,
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Crime Patterns by Month")

        monthly = df['Month'].value_counts()

        # Reorder months
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        monthly = monthly.reindex(month_order)

        fig = px.bar(
            x=monthly.index,
            y=monthly.values,
            labels={'x': 'Month', 'y': 'Number of Crimes'},
            color=monthly.values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("Seasonal Analysis")

        # Create seasons
        def get_season(month):
            if month in [12, 1, 2]:
                return 'Winter'
            elif month in [3, 4, 5]:
                return 'Spring'
            elif month in [6, 7, 8]:
                return 'Summer'
            else:
                return 'Fall'

        df['Season'] = df['Date'].dt.month.map(get_season)
        seasonal = df['Season'].value_counts()

        fig = px.pie(
            values=seasonal.values,
            names=seasonal.index,
            title="Crimes by Season",
            color_discrete_sequence=px.colors.seasonal
        )
        st.plotly_chart(fig, use_container_width=True)


# ================================
# 🧠 DIMENSIONALITY REDUCTION PAGE
# ================================
elif page == "🧠 Dimensionality Reduction":
    st.markdown('<div class="main-header">🧠 Dimensionality Reduction Analysis</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["PCA Visualization", "Clustering Analysis"])

    with tab1:
        st.subheader("Principal Component Analysis (PCA)")

        try:
            pca_df = pd.read_csv("pca_crime_data.csv")
            if 'PC1' in pca_df.columns and 'PC2' in pca_df.columns:
                col1, col2 = st.columns(2)

                with col1:
                    sample_size = st.slider("Sample Size for PCA", 1000, 10000, 5000, key="pca_sample")

                with col2:
                    color_by = st.selectbox("Color by", ["None", "Cluster"], key="pca_color")

                sample_pca = pca_df.sample(min(sample_size, len(pca_df)))

                if color_by == "Cluster" and 'KMeans_Cluster' in df.columns:
                    # Merge with cluster info
                    cluster_info = df[['KMeans_Cluster']].sample(min(sample_size, len(pca_df)))
                    sample_pca = sample_pca.join(cluster_info.reset_index(drop=True))

                    fig = px.scatter(
                        sample_pca,
                        x='PC1',
                        y='PC2',
                        color='KMeans_Cluster',
                        title="PCA with Clustering",
                        color_continuous_scale='Viridis'
                    )
                else:
                    fig = px.scatter(
                        sample_pca,
                        x='PC1',
                        y='PC2',
                        title="PCA Components Scatter Plot"
                    )

                st.plotly_chart(fig, use_container_width=True)

                # PCA explained variance info
                st.info("💡 **PCA Insight**: The first two principal components capture the most variance in your crime data, helping identify patterns and reduce dimensionality.")

            else:
                st.warning("⚠️ PCA columns not found in the data file")
        except FileNotFoundError:
            st.warning("⚠️ PCA data file not found. Please ensure 'pca_crime_data.csv' exists.")
        except Exception as e:
            st.warning(f"⚠️ Error loading PCA data: {str(e)}")

    with tab2:
        st.subheader("Crime Clustering Analysis")

        if 'KMeans_Cluster' in df.columns:
            col1, col2 = st.columns(2)

            with col1:
                cluster_counts = df['KMeans_Cluster'].value_counts().sort_index()

                fig = px.bar(
                    x=cluster_counts.index.astype(str),
                    y=cluster_counts.values,
                    labels={'x': 'Cluster', 'y': 'Number of Crimes'},
                    title="Crimes per Cluster",
                    color=cluster_counts.values,
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Crime types by cluster
                cluster_crime_types = df.groupby(['KMeans_Cluster', 'Primary Type']).size().reset_index(name='count')
                top_crimes_per_cluster = cluster_crime_types.groupby('KMeans_Cluster').apply(lambda x: x.nlargest(3, 'count')).reset_index(drop=True)

                fig = px.bar(
                    top_crimes_per_cluster,
                    x='KMeans_Cluster',
                    y='count',
                    color='Primary Type',
                    title="Top Crime Types by Cluster",
                    barmode='stack'
                )
                st.plotly_chart(fig, use_container_width=True)

            st.info("💡 **Clustering Insight**: K-means clustering groups similar crimes based on location, time, and other features, helping identify crime hotspots and patterns.")
        else:
            st.warning("⚠️ Clustering data not found. Please ensure your data includes cluster labels.")


# ================================
# 🤖 ML MODEL TRACKING PAGE
# ================================
elif page == "🤖 ML Model Tracking":
    st.markdown('<div class="main-header">🤖 Machine Learning Model Tracking</div>', unsafe_allow_html=True)

    st.markdown("""
    ### MLflow Integration

    Track your machine learning experiments, models, and results with MLflow.

    **Features:**
    - ✅ Experiment tracking
    - ✅ Model versioning
    - ✅ Performance metrics
    - ✅ Parameter logging
    """)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Open MLflow UI", type="primary", use_container_width=True):
            st.markdown("""
            <script>
                window.open('http://127.0.0.1:5000', '_blank');
            </script>
            """, unsafe_allow_html=True)

        st.success("Click above to open MLflow UI in a new tab")

    with col2:
        st.markdown("### 📊 Model Performance")

        # Check if model files exist
        import os
        model_files = os.listdir('.')
        if 'model.pkl' in model_files:
            st.success("✅ Model file found")
        else:
            st.warning("⚠️ Model file not found")

        if 'features.pkl' in model_files:
            st.success("✅ Feature preprocessor found")
        else:
            st.warning("⚠️ Feature preprocessor not found")

    # Show recent experiments if available
    st.markdown("---")
    st.subheader("📈 Recent Experiments")

    try:
        import mlflow
        import mlflow.sklearn

        # Get experiment data
        client = mlflow.tracking.MlflowClient()
        experiments = client.list_experiments()

        if experiments:
            exp_data = []
            for exp in experiments:
                runs = client.search_runs(exp.experiment_id, max_results=1)
                if runs:
                    latest_run = runs[0]
                    exp_data.append({
                        'Experiment': exp.name,
                        'Latest Run': latest_run.info.run_id[:8],
                        'Status': 'Completed' if latest_run.info.status == 'FINISHED' else 'Running'
                    })

            if exp_data:
                st.dataframe(pd.DataFrame(exp_data))
            else:
                st.info("No experiment runs found yet.")
        else:
            st.info("No experiments found. Start training models to see results here!")

    except ImportError:
        st.warning("MLflow not installed. Install with: `pip install mlflow`")
    except Exception as e:
        st.warning(f"Error connecting to MLflow: {str(e)}")

# Footer
st.markdown("---")
st.markdown("### 📞 Support & Documentation")
st.markdown("Built with ❤️ using Streamlit | Data: Chicago Crime Dataset")

# Add some spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)

# ================================
# 📊 EDA PAGE
# ================================
if page == "📊 EDA":
    st.title("📊 Crime Distribution")

    crime_counts = df['Primary Type'].value_counts().head(10)

    fig = px.bar(
        x=crime_counts.index,
        y=crime_counts.values,
        labels={'x': 'Crime Type', 'y': 'Count'}
    )

    st.plotly_chart(fig)


# ================================
# 🌍 GEO MAP PAGE
# ================================
elif page == "🌍 Geo Map":
    st.title("🌍 Crime Heatmap")

    m = folium.Map(location=[41.87, -87.62], zoom_start=10)

    sample_df = df.dropna(subset=['Latitude', 'Longitude']).sample(2000)

    for _, row in sample_df.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=2,
            color="red"
        ).add_to(m)

    st_folium(m)


# ================================
# ⏱️ TEMPORAL PAGE
# ================================
elif page == "⏱️ Temporal":
    st.title("⏱️ Crime by Hour")

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Hour'] = df['Date'].dt.hour

    hourly = df['Hour'].value_counts().sort_index()

    fig = px.line(x=hourly.index, y=hourly.values)

    st.plotly_chart(fig)


# ================================
# 🧠 PCA PAGE
# ================================
elif page == "🧠 PCA":
    st.title("🧠 PCA Visualization")

    try:
        pca_df = pd.read_csv("pca_crime_data.csv")
        if 'PC1' in pca_df.columns and 'PC2' in pca_df.columns:
            fig = px.scatter(
                pca_df.sample(min(5000, len(pca_df))),
                x='PC1',
                y='PC2'
            )
            st.plotly_chart(fig)
        else:
            st.warning("⚠️ PCA columns not found")
    except FileNotFoundError:
        st.warning("⚠️ PCA data file not found")
    except Exception as e:
        st.warning(f"⚠️ Error loading PCA data: {str(e)}")


# ================================
# 🤖 MLFLOW PAGE
# ================================
elif page == "🤖 MLflow":
    st.title("🤖 MLflow Tracking")

    st.markdown("👉 Open MLflow UI:")
    st.code("http://127.0.0.1:5000")
    import streamlit as st
    st.title("Hello, Streamlit from sonalhub!")

