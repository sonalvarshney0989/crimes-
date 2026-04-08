# 🚔 Crime Analytics Dashboard

A comprehensive Streamlit application for analyzing Chicago crime data with advanced analytics, machine learning, and interactive visualizations.

## 📊 Features

- **📈 Crime Statistics**: Detailed analysis of crime types, arrest rates, and distributions
- **🌍 Geographic Analysis**: Interactive maps showing crime hotspots
- **⏱️ Temporal Patterns**: Crime patterns by hour, day, month, and season
- **🧠 Dimensionality Reduction**: PCA visualization and clustering analysis
- **🤖 ML Model Tracking**: MLflow integration for experiment tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Navigate to the project directory**
   ```bash
   cd path/to/newGuvi
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**
   ```bash
   streamlit run app3.py
   ```

4. **(Optional) Start MLflow server**
   ```bash
   mlflow server --host 127.0.0.1 --port 5000
   ```

## 📁 Project Structure

```
├── app3.py                    # Main Streamlit application
├── pages/                     # Multi-page components
│   ├── 1_📊_EDA.py
│   ├── 2_🌍_Geo_Map.py
│   ├── 3_⏱️_Temporal.py
│   ├── 4_🧠_PCA_TSNE.py
│   └── 5_🤖_Model_MLflow.py
├── requirements.txt           # Python dependencies
├── clustered_crime_data.csv   # Main crime dataset
├── pca_crime_data.csv         # PCA transformed data
├── model.pkl                  # Trained ML model
├── features.pkl               # Feature preprocessor
├── mlruns/                    # MLflow experiment runs
└── mlflow.db                  # MLflow database
```

## 📊 Data Sources

- **Primary Dataset**: `clustered_crime_data.csv` - Chicago crime data with clustering labels
- **PCA Data**: `pca_crime_data.csv` - Dimensionality-reduced crime data
- **ML Models**: Pre-trained models for crime prediction and classification

## 🔧 Configuration

The application is configured with:
- Wide layout for better visualization
- Caching enabled for performance
- Interactive Plotly charts
- Folium maps for geographic data
- MLflow integration for model tracking

## 🎯 Usage

1. **Overview**: Get a high-level summary of crime statistics
2. **Crime Statistics**: Explore detailed crime type distributions and arrest rates
3. **Geographic Analysis**: Visualize crime patterns on interactive maps
4. **Temporal Patterns**: Analyze crime trends over time
5. **Dimensionality Reduction**: Explore PCA and clustering results
6. **ML Tracking**: Monitor machine learning experiments

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is for educational and analytical purposes.

## 🆘 Support

If you encounter any issues:
1. Check the requirements.txt for missing dependencies
2. Ensure data files are in the correct location
3. Verify MLflow server is running on port 5000 for ML tracking
4. Check the browser console for JavaScript errors

---

**Built with ❤️ using Streamlit and modern data science tools**
