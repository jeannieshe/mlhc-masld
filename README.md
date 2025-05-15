# MLHC 2025 Project: Early Prognosis of Metabolic Dysfunction Associated Fatty Liver Disease using Deep Learning and Clinical Data Analysis

## Overview
This project aims to evaluate deep learning models in prediction of progression of metabolic dysfunction associated fatty liver disease (MASLD). It includes three types of predictions: binary classification, time-to-event prediction, and survival analysis.

This project contains various Jupyter Notebooks for cleaning the data, training machine learning and deep learning models, and interpreting these models. The contents are broken down below:

### Directory: clean (code for data cleaning)


### Directory: models (code for training and evaluating models)


### Directory: interpret (code for interpreting the models and identifying most influential features)


## Running the Code

To clean the data, run all the Jupyter notebooks and scripts in the "clean" directory except for "combine.sh." There are 5 datasets used in the final analysis, and they are cleaned separately.This combine script should be run at the end of data cleaning and is responsible for combining all of the separate datasets from data cleaning.

To train the models, run the Jupyter notebook with the name of that model. Each of these Jupyter notebooks includes code for evaluating the model output as well.

Finally, for interpretations, run the notebooks in the interpret folder.
