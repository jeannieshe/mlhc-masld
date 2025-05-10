import pandas as pd

med_nafl = pd.read_csv("/nobackup/users/ericason/mlhc-final-project/data/NAFLpatients_Jan2025request/Med_all.use.final.txt", header=0, delimiter="\t")


# remove code types that appear very little
codes_to_include = list(med_nafl['Code_Type'].value_counts()[med_nafl['Code_Type'].value_counts() > 20].index)

med_nafl = med_nafl[med_nafl['Code_Type'].isin(codes_to_include)]
med_nafl['MedType_Code'] = med_nafl['Code_Type'] + "_" + med_nafl['Code']


# remove medication days from first NAFL if they are not numbers
med_nafl = med_nafl[(med_nafl['Med.daysfrom_firstNAFL'] != 'n') & (med_nafl['Med.daysfrom_firstNAFL'] != 'y')]
# filter for within 2 years
med_nafl = med_nafl[(med_nafl['Med.daysfrom_firstNAFL'].astype(int) > -730) & (med_nafl['Med.daysfrom_firstNAFL'].astype(int) < 0)]
# restrict to Med.before.ICD11
med_nafl = med_nafl.loc[med_nafl['Med.before.ICD11'] == 'y',]


# drop duplicates
med_nafl = med_nafl[['StudyID', 'MedType_Code']] # only keep certain columns
med_nafl.drop_duplicates(subset=['StudyID', 'MedType_Code'], keep='first', inplace=True) # deduplicate based on medication per patient

one_hot_med_nafl = pd.get_dummies(med_nafl, columns=['MedType_Code']) # one-hot encode
one_hot_med_nafl = one_hot_med_nafl.groupby('StudyID', as_index=False).max()

# restrict to medications that appear in at least 100 patients
one_hot_med_nafl = one_hot_med_nafl.loc[:,one_hot_med_nafl.sum() >= 100]

# save code to csv
one_hot_med_nafl.to_csv("/nobackup/users/ericason/mlhc-final-project/clean_data/nafl/med.nafl.csv", header=True, index=False, sep=",")
