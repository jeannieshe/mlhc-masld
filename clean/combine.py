import pandas as pd

lab_df = pd.read_csv("/nobackup/users/ericason/mlhc-final-project/clean_data/nafl/lab.nafl.csv", delimiter=",", header=0)
lab_df.set_index("StudyID", inplace=True)

phy_df = pd.read_csv("/nobackup/users/ericason/mlhc-final-project/clean_data/nafl/phy.nafl.csv", delimiter=",", header=0)
phy_df.set_index("StudyID", inplace=True)
drop_cols = ["mean_BMI_category", "last_BMI_category"]
phy_df = phy_df.drop(drop_cols, axis=1)

med_df = pd.read_csv("/nobackup/users/ericason/mlhc-final-project/clean_data/nafl/med.nafl.csv", delimiter=",", header=0)
med_df.set_index("StudyID", inplace=True)

dem_df = pd.read_csv("/nobackup/users/ericason/mlhc-final-project/clean_data/nafl/dem.nafl.csv", delimiter=",", header=0)
dem_df.set_index("StudyID", inplace=True)

dia_df = pd.read_csv("/nobackup/users/ericason/mlhc-final-project/clean_data/nafl/dia.nafl.csv", delimiter=",", header=0)
dia_df.set_index("StudyID", inplace=True)
dia_df = dia_df.drop(["Code_K76.0", "Censored"], axis=1)

combine_df = lab_df.join([phy_df, med_df, dem_df, dia_df], how="inner")

print(combine_df.head())

print(combine_df.shape)

combine_df.to_csv("/nobackup/users/ericason/mlhc-final-project/clean_data/nafl/combined.large.nafl.csv", sep=",", header=True, index=True)

print("complete")
