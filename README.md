# MTA Elevator & Escalator Predictive Maintenance

## Project Overview

Elevators and escalators are important parts of New York City's subway system, particularly for riders who depend on accessible station infrastructure. Unscheduled outages can disrupt service and reduce accessibility.

This project explores **predictive maintenance** by using historical MTA elevator and escalator performance data to predict whether a piece of equipment will experience an **unscheduled outage in the following month**.

Rather than only analyzing outages after they occur, the goal is to identify equipment that may be at risk ahead of time so maintenance and inspection efforts could be prioritized.

## Research Question

**Using information available for an elevator or escalator during the current month, can we predict whether it will experience an unscheduled outage in the following month?**

## Dataset

The project uses historical monthly elevator and escalator performance data from the Metropolitan Transportation Authority (MTA).

SOURCE: https://data.ny.gov/Transportation/MTA-NYCT-Subway-Elevator-and-Escalator-Availabilit/rc78-7x78/about_data

- **82,000+ monthly equipment records**
- **695 unique elevators and escalators**
- Data spans **2015–2026**
- One observation represents **one piece of equipment during one month**

Because each piece of equipment appears repeatedly over time, the dataset provides historical operating patterns that can be used to predict future equipment behavior.

## Target Variable

The target variable is:

**`Future 1-Month Outage`**

It indicates whether the same piece of equipment experiences at least one unscheduled outage during the following month:

- `0` = No unscheduled outage next month
- `1` = At least one unscheduled outage next month

The target was engineered by assigning each equipment unit's next month unscheduled outage outcome to its current- month record. The target equals 1 if the equipment experiences at least one unscheduled outage in the following month and 0 otherwise.

## Features

The final model uses current and historical equipment information available at prediction time:

- Equipment Type
- Borough
- Current Month Scheduled Outages
- Current Month Unscheduled Outages
- Entrapments
- Time Since Major Improvement
- 24-Hour Availability
- Previous Month Unscheduled Outages

Using only information available at or before the prediction month helps prevent **data leakage**.

## Modeling Approach

The data was split chronologically so that earlier observations were used for training and more recent observations were reserved for testing. This better represents a real forecasting scenario than randomly mixing historical and future observations.

Three classification algorithms were evaluated:

1. **Logistic Regression**
2. **Random Forest**
3. **XGBoost**

XGBoost was also evaluated using **time based cross validation** to preserve the chronological nature of the data during model tuning.

Because failing to identify an actual future outage could be costly in a predictive maintenance setting, **recall for the outage class** was treated as an important evaluation metric.

## Model Results
## Model Results

| Model | Accuracy | Outage Precision | Outage Recall | Outage F1 |
|---|---:|---:|---:|---:|
| Logistic Regression | 79.5% | 84% | 83% | 83% |
| Random Forest | 79.6% | 80% | 89% | 84% |
| XGBoost | 81.5% | 80% | **93%** | **86%** |
| Tuned XGBoost | 81.5% | 81% | 92% | **86%** |

The baseline XGBoost model achieved the highest outage recall, identifying approximately **93% of the actual outages in the held out test data**.

## Streamlit Application

An interactive Streamlit application was developed to demonstrate how the trained model could be used for prediction.

Users enter current equipment information such as outage history, availability, equipment type, and time since major improvement. The application processes those inputs using the same preprocessing used during model training and returns a prediction for whether an unscheduled outage is expected in the following month.

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Streamlit
- Jupyter Notebook
