"""
Credit Scorecard Model
Author: Ashwin Naidu
"""
import os
import sys
import zipfile
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
sns.set(style='whitegrid', palette="deep", font_scale=1.1, rc={"figure.figsize": [8, 5]})

# To decide display window width on console
DESIRED_WIDTH = 320
pd.set_option('display.width', DESIRED_WIDTH)
np.set_printoptions(linewidth=DESIRED_WIDTH)
pd.set_option('display.max_columns', 30)

PATH_TO_ZIP_FILE = 'german_credit.zip'
PATH_TO_CSV_FILE = 'german_credit/'
IMAGE_DIR = 'images/'

def csvtodataframe():
    """
    Extract csv file from zip folder and covert into dataframe.
    Also make images directory if not exist.
    :return: <pd.Dataframe> Dataframe realted with german-credit score
    """
    # Create the Image directory to save any plots
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    # Extract the zipfile
    if os.path.exists(PATH_TO_ZIP_FILE):
        with zipfile.ZipFile(PATH_TO_ZIP_FILE, 'r') as zip_ref:
            zip_ref.extractall(PATH_TO_CSV_FILE)

        dataframe = pd.read_csv(os.path.join(PATH_TO_CSV_FILE, os.listdir(PATH_TO_CSV_FILE)[0]))
        dataframe = dataframe.drop(dataframe.columns[0], axis=1)
        return dataframe

    return None

creditdata = csvtodataframe()
if creditdata is None:
    sys.exit("Zip file Not Found!!!")

def displaydatasetproperties(dataframe):
    """
    Check below 4 properties of dataframe
        1. Looking the Type of Data
        2. Null Numbers
        3. Unique values
        4. The first rows of our dataset

    :param dataframe: <pd.Dataframe> Dataframe realted with german-credit score
    """
    # Check for Null Values
    print(dataframe.info())
    # Check Unique Values
    print(dataframe.nunique())
    # Check for distribution of data
    print(dataframe.describe())

# Display dataset properties
print(creditdata.head(n=10))
displaydatasetproperties(creditdata)

def datasetexplorations(dataframe):
    """
    We will Exploratory Data Analysis by plotting
        1. Plot Target Variable 'Risk' Distribution
        2. Plot Age vs Risk
        3. Plot Age vs Credit Amount against 'Risk' column
        4. Plot Sex vs Credit Amount against 'Risk' column
        5. Plot Housing vs Risk

    :param dataframe: <pd.Dataframe> Dataframe containing german-credit dataset
    :return:
    """
    # 1. Plot Target Variable Distribution
    dataframe['Risk'].value_counts().plot(kind='bar')
    plt.savefig(IMAGE_DIR + 'target_distribution_plot.jpeg')
    plt.close()

    # 2. Age vs Risk Plot
    gplot = sns.FacetGrid(dataframe, col="Risk", hue_kws={'color': ['r', 'b']}, hue="Risk")
    gplot.map(plt.hist, "Age")
    plt.savefig(IMAGE_DIR + 'AgevsRisk.jpeg')
    plt.close()

    # 3. Age vs Credit Amount
    # Let's look the Credit Amount column
    interval = (18, 25, 35, 60, 120)
    # Creating an categorical variable to handle with the Age variable
    dataframe["Age_Categorical"] = pd.cut(dataframe.Age, interval,
                                          labels=['Student', 'Young', 'Adult', 'Senior'])

    # Used boxplot from seaborn
    sns.catplot(x="Age_Categorical", y="Credit amount", hue="Risk", kind='box', data=dataframe,
                aspect=3, height=10)
    plt.savefig(IMAGE_DIR + 'AgevsCreditAmt.jpeg')
    plt.close()

    # 4. Sex vs Credit amount
    sns.catplot(x="Sex", y="Credit amount", hue="Risk", kind='box', data=dataframe,
                aspect=2, height=6)
    plt.savefig(IMAGE_DIR + 'SexvsCreditAmt.jpeg')
    plt.close()

    # 5. Housing vs Risk Plot
    housexrisk = dataframe[['Housing', 'Risk']].groupby(['Housing',
                                                         'Risk']).size().to_frame('Count').reset_index()
    housexrisk = housexrisk.sort_values(by='Count', ascending=False)
    sns.catplot(x="Housing", y="Count", hue="Risk", kind='bar', data=housexrisk,
                aspect=2, height=6)
    plt.savefig(IMAGE_DIR + 'HousingvsRisk.jpeg')
    plt.close()

    # 6. Housing vs credit amount
    sns.violinplot(x="Housing", y="Credit amount", hue="Risk", data=dataframe,
                   aspect=2, height=6)
    plt.savefig(IMAGE_DIR + 'HousingvsCreditAmt.jpeg')
    plt.close()

    # 5. Job vs Risk Plot
    jobxrisk = dataframe[['Job', 'Risk']].groupby(['Job',
                                                   'Risk']).size().to_frame('Count').reset_index()
    jobxrisk = jobxrisk.sort_values(by='Count', ascending=False)
    sns.catplot(x="Job", y="Count", hue="Risk", kind='bar', data=jobxrisk,
                aspect=2, height=6)
    plt.savefig(IMAGE_DIR + 'JobvsRisk.jpeg')
    plt.close()

    # 7. Job vs credit amount
    sns.catplot(x="Job", y="Credit amount", hue="Risk", kind='box', data=dataframe,
                aspect=2, height=6)
    plt.savefig(IMAGE_DIR + 'JobvsCreditAmt.jpeg')
    plt.close()

datasetexplorations(creditdata)