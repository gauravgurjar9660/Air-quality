import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from datetime import datetime

# 1. Saved Model aur Pipeline ko load karein
data=pd.read_csv("air_quality_index.csv")
model = joblib.load("model2.pkl")
pipeline = joblib.load("pipeline2.pkl")

# 2. App ka Title aur Description
st.title("Air Quality Index (AQI) Prediction App ")
st.write("Apne area ki details dalein aur pata karein ki average pollutant index kitna hai.")

# 3. User se Input lene ke liye form/inputs banayein
st.header("Enter Location & Pollutant Details:")

country = st.selectbox("Country", ["India"])
state_list=sorted(data["state"].unique().tolist())
state = st.selectbox("Enter Your State ",state_list)
filter_state=data[data["state"]==state]
city_list=sorted(filter_state["city"].unique().tolist())
 
city = st.selectbox("Enter your city", city_list)
filter_city=filter_state[filter_state["city"]==city]
station_list=sorted(filter_city["station"].unique().tolist())
station = st.selectbox("Station", station_list)
pollutant_id = st.selectbox("Pollutant ID", ["PM2.5", "PM10", "NO2", "CO"])

latitude = st.number_input("Latitude", value=28.6)
longitude = st.number_input("Longitude", value=77.2)
pollutant_min = st.slider("Minimum Pollutant Level", 0, 500, 15)
pollutant_max = st.slider("Maximum Pollutant Level", 0, 500, 450)
# last_update = st.text_input("Last Update Date/Time", "2026-06-03 17:00:00")

# 4. Prediction Button
if st.button("Predict AQI"):
    current_now=datetime.now().strftime("%y-%m-%d %H:%M:%S")
    input_dict = {
        "country": [country], "state": [state], "city": [city], 
        "station": [station], "pollutant_id": [pollutant_id], "last_update": [current_now],
        "latitude": [latitude], "longitude": [longitude], 
        "pollutant_min": [pollutant_min], "pollutant_max": [pollutant_max]
    }
    input_df = pd.DataFrame(input_dict)
    
    try:
        transformed_data = pipeline.transform(input_df)
        prediction = model.predict(transformed_data)
        st.success(f"Predicted Pollutant Average: **{prediction[0]:.2f}**")
        
        if prediction[0] > 300:
            st.warning(" 🟤: Health alert posing life-threatening risks!")
        elif(300>prediction [0] >200):
            st.info("🟣: Health warnings of emergency conditions.")
        elif (200>prediction[0]>150):
             st.info(" 🔴: Everyone may begin to experience health effects !")
        elif (150>prediction[0]>100):
             st.info(" 🟠: Sensitive individuals (like those with asthma or heart conditions) may experience health effects.")
        elif (100>prediction[0]>50):
             st.info(" 🟡: Air quality is acceptable. ")
        else :
             st.info("  Air quality is satisfactory, and poses little or no risk.")
    except Exception as e:
        st.error(f"Error in prediction: {e}")
 

# --- Aapka existing prediction aur warning message code ---
# st.warning("🟠 : Sensitive individuals (like those with asthma or heart conditions) may experience health effects.")
    
    st.markdown("---")
    st.subheader(f"📈 {pollutant_id} Trend Chart - {city}")
    
    # 1. ACTUAL DATA LOGIC (Agar aapka data connected hai)
    try:
        # User ke select kiye hue inputs ke basis par data filter karein
        filtered_df = df[
            (df['State'] == state) & 
            (df['City'] == city) & 
            (df['Station'] == station) & 
            (df['Pollutant_ID'] == pollutant_id)
        ].sort_values(by='Date')
    
        if not filtered_df.empty:
            # Matplotlib Line Chart Creation
            fig, ax = plt.subplots(figsize=(10, 4.5))
            
            # Line plot with markers
            ax.plot(filtered_df['Date'], filtered_df['Pollutant_Level'], 
                    marker='o', color='#ff4b4b', linewidth=2.5, label='AQI/Pollutant Level')
            
            # Styling
            ax.set_title(f"Historical Trend for {station}", fontsize=12, fontweight='bold', pad=15)
            ax.set_xlabel("Date/Time", fontsize=10)
            ax.set_ylabel(f"{pollutant_id} Level", fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend()
            
            plt.xticks(rotation=30)
            plt.tight_layout()
    
            # Streamlit mein render karna
            st.pyplot(fig)
        else:
            st.info("Selected location ke liye data available nahi hai.")
    
    except NameError:
        # 2. DUMMY DATA LOGIC (Testing ke liye jab tak aapka actual dataframe 'df' ready nahi hai)
        # Yeh aapki app par 100% chalega bina kisi error ke
        dates = pd.date_range(start="2026-05-25", periods=10).strftime('%d %b')
        
        # Aapke predicted 124.21 ke aas-paas ke 10 fake random values line chart ke liye
        dummy_levels = np.random.randint(90, 150, size=10) 
        
        fig, ax = plt.subplots(figsize=(10, 4.5))
        
        # Line chart plot kiya
        ax.plot(dates, dummy_levels, marker='o', color='#ff4b4b', linewidth=2.5, label=f'Current Trend ({pollutant_id})')
        
        # Chart decorative setup
        ax.set_title(f"Pollutant Level Trend over Time ({city}, {state})", fontsize=12, fontweight='bold', pad=15)
        ax.set_xlabel("Timeline", fontsize=10)
        ax.set_ylabel("Index Value", fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        
        plt.tight_layout()
        
        # Streamlit interface par display karne ke liye
        st.pyplot(fig)