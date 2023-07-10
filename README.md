# Data Analysis on US Mass Shooting
### Used Plotly interactive charts and dash to create an interactive dashboard

I am working on US Mass Shooting data that has been taken from Kaggle. The data is from 1966 to 2017 comprising up to 50 years worth of data.

The US has witnessed 398 mass shootings in last 50 years that resulted in 1,996 deaths and 2,488 injured. The latest and the worst mass shooting of October 2, 2017 killed 58 and injured 515 so far. The number of people injured in this attack is more than the number of people injured in all mass shootings of 2015 and 2016 combined.

Dataset: The dataset contains detailed information of 398 mass shootings in the United States of America that killed 1996 and injured 2488 people.

Variables: The dataset contains Serial No, Title, Location, Date, Summary, Fatalities, Injured, Total Victims, Mental Health Issue, Race, Gender, and Lat-Long information.

Goal: The purpose of the notebook is to clean the data, prepare a dash app to see the trend, and understand the geographical impact, impact in terms of lost lives, and the shooter's health condition and demographic information. Also, I am aiming to prepare different kinds of plotly charts to have a broader view of the data.

Dash app demo - 

https://github.com/kulwinderkk/data-analysis-mass-shooting-us-plotly-dash/assets/119710277/927bc0bc-b5ed-48c1-afc1-f52cfd9fb964

**Note:**
In this repository there are the following files:-
1. Mass Shootings Dataset Ver 5.csv (Raw data downloaded from Kaggle).
2. US mass shooting data analysis-fin-ver (Jupyter Notebook) *Please note that this notebook has interactive plotly charts that are not rendered on Github. So in order to see the charts this notebook can be accessed on [nbviewer](https://nbviewer.org/github/kulwinderkk/data-analysis-mass-shooting-us-plotly-dash/blob/main/US%20mass%20shooting%20data%20analysis-fin-ver.ipynb).
3. app.py is a Python script to create a Dash app. This app can be run locally through your terminal, put in the default local host ip and port (http://127.0.0.1:8050/) in any browser.
4. cleaned_out.csv is the cleaned data set after data cleaning and wrangling.

References:
Data set - [Kaggle](https://www.kaggle.com/datasets/zusmani/us-mass-shootings-last-50-years)

https://www.kaggle.com/code/antonaks/mass-shooting-in-us-using-plotly
