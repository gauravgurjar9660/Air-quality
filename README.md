# Air-quality
This project about air quality data from different places with excellent efficiency and in app user customize the details according there details.
# Air Quality Analysis & Prediction 

An end-to-end Machine Learning project to analyze and predict air pollutant levels across different stations and cities. This project includes a complete data preprocessing pipeline, statistical testing, and an interactive web application built with Streamlit.

## Project Overview & Approach
For this project, my main focus was on creating a statistically sound model and strictly avoiding data leakage, rather than just chasing a high R2 score. 

**Key Data Science Steps Taken:**
* **Preventing Data Leakage:** Handled missing values by imputing the median of the *Train* data into the *Test* data. Handled outliers strictly on the training set.
* **Smart Encoding:** Instead of using standard One-Hot Encoding for high-cardinality columns (like City and Station) which creates too many dimensions, I used `TargetEncoder`. 
* **Scaling:** Used `RobustScaler` to make the model stable against outliers.
* **Statistical Rigor:** Checked for multicollinearity using VIF (Variance Inflation Factor) and verified OLS Regression assumptions (like Autocorrelation and Heteroscedasticity).

## 🛠️ Tech Stack
- **Language:** Python
- **Libraries:** Pandas, NumPy, Scikit-Learn, Matplotlib
- **Web Framework:** Streamlit
- **Other Tools:** Joblib (for saving pipelines/models), category_encoders

##  App Features
- **Custom Predictions:** Users can select specific States, Cities, and Stations to predict pollutant levels.
- **Health Alerts:** Dynamic UI warnings based on AQI values (e.g., "Health warnings of emergency conditions" if levels cross 200).
- **Trend Analysis:** Generates historical line charts for selected pollutants using Matplotlib.

## Project Structure
```text
 Air-quality
   air.py                       # Main Streamlit web application
   Rework_air_quality.ipynb     # Final notebook with EDA, stats, and model training
   pipeline.pkl                 # Saved data preprocessing pipeline
   model_file.pkl               # Saved trained Machine Learning model
   air_quality_index.csv        # Dataset
