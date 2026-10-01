import streamlit as st
import pandas as pd
import joblib

# Load the trained XGBoost model
model = joblib.load("xgb_model.pkl")

# Load the scaler used during model training
scaler = joblib.load("scaler.pkl")

# App title and description
st.title("MTA Elevator & Escalator Outage Predictor")

st.write(
    "Enter current equipment information to predict whether an "
    "unscheduled outage may occur in the following month."
)

# User input fields
st.subheader("Equipment Information")

equipment_type = st.selectbox(
    "Equipment Type",
    ["Elevator", "Escalator"]
)

borough = st.selectbox(
    "Borough",
    ["Bronx", "Brooklyn", "Manhattan", "Queens"]
)

scheduled_outages = st.number_input(
    "Current Month Scheduled Outages",
    min_value=0,
    value=0
)

unscheduled_outages = st.number_input(
    "Current Month Unscheduled Outages",
    min_value=0,
    value=0
)

entrapments = st.number_input(
    "Entrapments",
    min_value=0,
    value=0
)

time_since_improvement = st.number_input(
    "Time Since Last Major Improvement in Months",
    min_value=0,
    value=0,
    step=1
)

availability = st.number_input(
    "24-Hour Availability (%)",
    min_value=0.0,
    max_value=100.0,
    value=95.0
)

previous_outages = st.number_input(
    "Previous Month Unscheduled Outages",
         min_value=0,
        value=0,
        step=1
)

# Make prediction when the user clicks the button
if st.button("Predict Next Month Unscheduled Outage"):

    # Create one row using the same columns the model was trained on
    input_data = pd.DataFrame({
        "Scheduled Outages": [scheduled_outages],
        "Unscheduled Outages": [unscheduled_outages],
        "Entrapments": [entrapments],
        "Time Since Major Improvement": [time_since_improvement],
        "24-Hour Availability": [availability],
        "Previous Month Outages": [previous_outages],

        # Convert Equipment Type into the dummy variable used during training
        "Equipment Type_Escalator": [
            1 if equipment_type == "Escalator" else 0
        ],

        # Convert Borough into the dummy variables used during training
        "Borough_Brooklyn": [
            1 if borough == "Brooklyn" else 0
        ],
        "Borough_Manhattan": [
            1 if borough == "Manhattan" else 0
        ],
        "Borough_Queens": [
            1 if borough == "Queens" else 0
        ]
    })

    # Apply the same scaling used during model training
    input_scaled = scaler.transform(input_data)

    # Make the prediction
    prediction = model.predict(input_scaled)[0]

    # Get the probability of a future outage
    outage_probability = model.predict_proba(input_scaled)[0][1]

    # Display the result
    st.subheader("Prediction")

    if prediction == 1:
        st.warning("Future next month unscheduled outage predicted.")
    else:
        st.success("No next month unscheduled outage predicted.")

    st.write(
        f"Estimated probability of an outage next month: "
        f"{outage_probability:.1%}"
    )