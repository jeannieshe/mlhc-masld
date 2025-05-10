print("starting import")

import pandas as pd
import gc

dia = pd.read_csv('/nobackup/users/ericason/mlhc-final-project/data/NAFLpatients_Jan2025request/Dia_all.use.final.txt', sep='\t', quotechar='"', header=0)

print("read in file: ", len(dia['StudyID'].unique()))

# subset by before ICD11
dia = dia[(dia['Dia.before.ICD11'] == 'y')] # & (dia['Dia.Age.90'] <= 30)]
print("ICD 10: ", len(dia['StudyID'].unique()))

# remove those younger than 30
dia = dia[(dia['Dia.Age.90'] >= 30)]
print("Age >= 30: ", len(dia['StudyID'].unique()))


# only keep those diagnosed with K76.0 (meaning they have NAFL)
dia = dia.groupby("StudyID").filter(
    lambda group: (group['Code'] == 'K76.0').any())
print("NAFL (K76.0): ", len(dia['StudyID'].unique()))

worsening_progression_codes = ['K75.81', 'K75.89', 'K72.00', 'K72.01','K72.10',
                     'K72.11','K72.90','K72.91','K74.0','K74.00',
                     'K74.01','K74.02','K74.1','K74.2','K74.60',
                     'K74.69','C22.0','C22.1','C22.2','C22.3','C22.4',
                     'C22.7','C22.8','C22.9',]

# remove those diagnosed with conditions including MASH or worse before diagnosis with MASLD
remove = dia[(dia['Code'].isin(worsening_progression_codes)) & (dia['Dia.daysfrom_firstNAFL'] <= 0)]
rm_patients = remove['StudyID'].unique()
dia = dia[~dia['StudyID'].isin(rm_patients)]
print("Conditions before NAFL: ", len(dia['StudyID'].unique()))

# remove those diagnosed with a condition to exclude
supp_table = pd.read_csv('/nobackup/users/ericason/mlhc-final-project/data/SupplementaryTable_S1.csv', sep=',', quotechar='"', header=0)
print(supp_table.head())
exclude_codes = list(supp_table.iloc[:,0])
remove = dia[(dia['Code'].isin(exclude_codes))]
rm_patients = remove['StudyID'].unique()
dia = dia[~dia['StudyID'].isin(rm_patients)]
print("After removing exclusion: ", len(dia['StudyID'].unique()))

# create the outcome column denoting binary outcome for any progression codes
dia['Outcome'] = dia.groupby('StudyID')['Code'].transform(lambda x: x.isin(worsening_progression_codes).any())

filtered = dia[dia['Code'].isin(worsening_progression_codes)]

# for each StudyID, find the smallest "Dia.daysfrom_firstNAFL"
min_days = filtered.groupby('StudyID')['Dia.daysfrom_firstNAFL'].min()

# map the result back to the original dataset
dia['DaysUntilFirstProgression'] = dia['StudyID'].map(min_days)

# create column to track censoring
dia['Censored'] = dia['DaysUntilFirstProgression'].isna()
print(dia['Censored'])
print(dia['Censored'].sum())

# fill patients who had no progression with the last recorded date
dia['DaysUntilFirstProgression'] =dia['DaysUntilFirstProgression'].fillna(dia.groupby('StudyID')['Dia.daysfrom_firstNAFL'].transform('max'))
print("NA in progression column: ", dia['DaysUntilFirstProgression'].isna().sum())

all_liver_codes = ['K75.81', 'K75.89', 'K72.00', 'K72.01','K72.10',
                     'K72.11','K72.90','K72.91','K74.0','K74.00',
                     'K74.01','K74.02','K74.1','K74.2','K74.60',
                     'K74.69','C22.0','C22.1','C22.2','C22.3','C22.4',
                     'C22.7','C22.8','C22.9',
                    'K76.1','K76.2','K76.3',
                   'K76.4','K76.6','K76.7','K76.81','K76.82','K76.89',
                    'K76.9','K77','C18.3','C78.7','C7B.02','D37.6',]

print("Days until first progression: ", len(dia['StudyID'].unique()))


# remove all rows with Code in all_liver_codes
dia_1 = dia[~dia['Code'].isin(all_liver_codes)]
print("Liver codes removed: ", len(dia_1['StudyID'].unique()))

# drop unnecessary cols
dia_1 = dia_1.drop(columns=['Diagnosis_Name', 'Diagnosis_Flag', 'Inpatient_Outpatient', 'Code_Type', 'Dia.Age.90', 'Dia.daysfrom_firstNAFL', 'Dia.before.ICD11'])

print(dia_1.shape)

gc.collect()

# filter for diagnoses that occur in more than 100 patients

result = pd.crosstab(dia_1['Code'], dia_1['StudyID']).astype(bool)

counts = result.sum(axis=1)
counts = counts[counts >= 100]
keep_diag = counts.index

print(keep_diag)

dia_1 = dia_1[dia['Code'].isin(keep_diag)]

print(dia_1.shape)
print(len(dia_1['Code'].unique()))

dia_encoded = pd.get_dummies(
        dia_1,
        columns=["Code"])

dia_encoded = dia_encoded.groupby("StudyID", as_index=False).max()

print(len(dia_encoded['StudyID'].unique()))


dia_encoded.to_csv("/nobackup/users/ericason/mlhc-final-project/clean_data/nafl/dia.nafl.csv", sep=",", header=True, index=False)
