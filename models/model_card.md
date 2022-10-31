# Pest Classification Model Card: MIT 808 Capstone Project 2022
Last updated:**June 2020**

## Model Details
For this research task we develop four machine learning models to classify the presence of two types of invasive pests in South Africa based on historical weather patterns. We make use of the Support Vector Machine algorithm and the XGBoost algorithm to make our classifications. The models are referred to as follows:

- Lepto_SVM: Support Vector Classifier for classifying the presence of the Leptocybe invasa pest.
- Lepto_XGB: XGBoost classifier for classifying the presence of the Leptocybe invasa pest.
- Sirex_SVM: Support Vector Classifier for classifying the presence of the Sirex noctilio pest.
- Sirex_XGB: XGBoost classifier for classifying the presence of the Sirex noctilio pest.


### Model dates

- Lepto_SVM: 7 May 2022
- Lepto_XGB: 29 April 2022
- Sirex_SVM: 8 May 2022
- Sirex_XGB: 29 April 2022

### Model types

All models are binary classification models.

### Model version

The models published in this repository are the first versions made available to anyone other than the contributors.

### Paper or other resource for more information
- [Project Scoping Document](https://github.com/up-mitc-ds/mit808-2022-project-significant-outliers-1/blob/master/reports/MIT808%20Scoping.pdf) 
- [Exploratory Data Analysis](https://github.com/up-mitc-ds/mit808-2022-project-significant-outliers-1/blob/master/reports/MIT808%20EDA.pdf)
- [Modelling Report](https://github.com/up-mitc-ds/mit808-2022-project-significant-outliers-1/blob/master/reports/MIT808%20Modelling.pdf)
- [Visualisation Report](https://github.com/up-mitc-ds/mit808-2022-project-significant-outliers-1/blob/master/reports/MIT808%20Visualisation.pdf)
- [Final Submission Report](https://github.com/up-mitc-ds/mit808-2022-project-significant-outliers-1/blob/master/reports/MIT808%20Final%20Report.pdf)


### Where to send questions or comments about the model
Please email the authors below:

- Gené Fourie: u20797274@tuks.co.za
- Connor McDonald: u16040725@tuks.co.za

## Intended Uses:

### Primary intended uses

The primary intended users of these models are *researchers and members of the Forestry Agriculture and Biodiversity Institute of South Africa (FABI)*.

These models were designed to predict the presence of specific pests in South African forests, to help combat them and preserve these forests.

### Secondary uses

Here are some secondary use cases we believe are likely:

- **Data Validation**: The Application allows the user to identify faulty stations or stations that do not provide any data at all.

- **Station Mapping**: The application aggregates data from various active stations over time, which allows researchers and users of the app to construct an uninterrupted timeline of weather records.

- **Resource Allocation**: Allows researchers to identify high risk areas and allocate/recommend more pesticide usage in these regions.

- **Provides Predictions for inaccessible locations**: Many of these forests are vast and inaccessible by vehicle, this allows researchers to gain some insight into these regions by using an extrapolation from the machine learning models.

- **Weather-based decision-making**: Identify monthly total rainfall and average maximum and minimum trends at any location in South Africa from 1950 to 2019. This can assist in planning for rainwater harvesting, crop farming, localised stormwater management or wildfire control.


### Out-of-scope use cases

- **Location sensitive**: Since the models use the nearest weather station to extrapolate weather conditions for pest classification, the model can theoretically make predictions for any location on earth. However, this is discouraged as the models were only trained on weather stations within South Africa, therefore, there is a strong chance of low quality predictions as the location of prediction moves further away from South Africa.

- **Pest specific**: The models were only trained to predict the presence of two pests, Leptocybe invasa and Sirex noctilio. Therefore, the models should not be used to predict the presence of any other pests found in South Africa without being retrained first.

- **Presence not severity**: The models predict pest presence, but not severity. As a result, a positive prediction means that one tree or 200 trees in the selected region may be infected.

## Evaluation Data

### Datasets

We were provided with three primary datasets, namely:

- Daily Weather records for various stations across South Africa from over 6000 weather stations from 1950-2019
- Annual inspection records for Leptocybe invasa from 2012-2020
- Annual inspection records for Sirex noctilio from 2012-2020

We constructed a complex feature engineering script located in `notebooks/03-gf-feature-engineering-input.ipynb`. This script generated 8 more features such as "temperature difference from average" and "rainfall difference from average" which were then used by both algorithms to create the four models.


### Motivation

The project behind the development of these models had three main goals shown below:

1. Integration and standardisation of weather and pest datasets.
2. Analysis of weather and pest trends over time. These analyses will aim to detect any correlations between pest prevalence and climatic patterns.
3. Web-based user interface development for analysis, visualisation and scenario modelling.

Goal 2 formed the primary motivation for the development of these models, as these models were able to analyse large amounts of data and uncover patterns and correlations not seen by the naked eye. This allowed us to predict pest prevalence with up to 81% accuracy (for Leptocybe).


### Caveats and Recommendations


Due to the nature of the problem investigated in this research, our dataset was largely imbalanced. This led us to use penalisation factors in our models to ensure that the model was more conservative when predicting the minority class (positive inspection). As a result, this reduced the performance of the majority class classification and led to a number of false positives. This may lead to one believing that the model is not performing well as the model may frequently predict a positive inspection when it is in fact negative.

Furthermore, the models are not capable of determining the severity of infestation as they only output a binary result. It may be a reasonable area for future research should the need arise. We recommend researchers investigate these aspects of the model and share their results.

