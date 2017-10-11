import numpy as np
import pandas as pd

# Filename format for Baby Names from Social Security Card Applications-National Level Data
# Downloaded & unzipped from:
# https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-level-data
name_filepath = 'raw_data/yob{}.txt'
years = range(1916, 2017)

# Resident Population by Single Year of Age and Sex in the US
# Downloaded only the 2016 data from:
# https://factfinder.census.gov/bkmk/table/1.0/en/PEP/2016/PEPSYASEXN
age_dist_filepath = 'raw_data/PEP_2016_PEPSYASEXN_with_ann.csv'


def merge_name_files(path, yrs):
    """
    path: filename format with placeholder for years to iterate over
    yrs: iterable

    Merge name files across yob to create a single dataframe with the following columns:
        * name
        * sex (1 for M, 2 for F)
        * no_count (number of counts for name)
        * yob (year of birth)
    """
    df_names = []
    for yr in yrs:
        df_yr = pd.read_csv(path.format(yr), names=['name', 'sex', 'no_count'])
        df_yr['yob'] = yr
        df_names.append(df_yr)
    dfs_merged = pd.concat(df_names)

    dfs_merged.loc[dfs_merged.sex == 'M', 'sex'] = 1
    dfs_merged.loc[dfs_merged.sex == 'F', 'sex'] = 2

    return dfs_merged

merged_name_df = merge_name_files(name_filepath, years)


def clean_age_dist(path):
    """
    Clean age distribution data to output a dataframe with the following columns:
        * sex (1 for M, 2 for F)
        * yob (year of birth)
        * no_count (number of counts for yob)
    """
    df = pd.read_csv(path).T
    df.reset_index(inplace=True)

    # drop unnecessary rows incl. median and total (age999)
    df.drop([0, 1, 2, 3, 4, 207, 208], inplace=True)
    # drop unnecessary column
    df.drop([0], axis=1, inplace=True)

    df.rename(columns={1: 'no_count'}, inplace=True)
    df.rename(columns={'index': 'desc'}, inplace=True)

    df['age_in_2016'] = df.desc.apply(lambda x: x.split('_')[-1][3:])
    df['sex'] = df.desc.apply(lambda x: x.split('_')[0][-1:])

    # treat 100+ as 100
    df.loc[df.age_in_2016 == '100plus', 'age_in_2016'] = 100

    df[['no_count', 'age_in_2016', 'sex']] = df[['no_count', 'age_in_2016', 'sex']].astype(int)

    # derive yob from age
    df['yob'] = 2016 - df['age_in_2016']

    return df

cleaned_yob_dist_df = clean_age_dist(age_dist_filepath)


def master_df_sex(df_raw_name, sex):
    """
    Split df_raw_name by sex then create full yob-name product space
    """
    df_sex = df_raw_name[df_raw_name.sex == sex].copy()
    df_sex.drop(['sex'], axis=1, inplace=True)
    df_sex.name = df_sex.name.str.lower()

    # create a list of unique names by sex
    unique_names_by_sex = df_sex.name.unique().tolist()
    unique_names_by_sex.sort()

    years = df_sex.yob.unique().tolist()
    # create every pairing of yob and name
    idx_prod = [years, unique_names_by_sex]
    yob_name_idx = pd.MultiIndex.from_product(idx_prod, names=['yob', 'name'])
    full_idx_df = pd.DataFrame(index=yob_name_idx)

    master_df = pd.merge(full_idx_df.reset_index(), df_sex, on=['yob', 'name'],
                         how='left').set_index(['yob','name']).sort_index()

    master_df.fillna(value=0, inplace=True)

    return master_df


def yob_dist_df_sex(df_raw_yob, sex):
    """
    Split df_raw_yob by sex and calculate proportion of yob's
    """
    df_sex = df_raw_yob[df_raw_yob.sex == sex].copy()
    df_sex['proportion'] = (df_sex.no_count / df_sex.no_count.sum())

    df_sex.set_index(['yob'], inplace=True)

    return df_sex[['proportion']]


df_male_name = master_df_sex(merged_name_df, 1)
df_female_name = master_df_sex(merged_name_df, 2)
df_male_name.to_csv('prep_data/df_male_name.csv')
df_female_name.to_csv('prep_data/df_female_name.csv')

df_male_yob = yob_dist_df_sex(cleaned_yob_dist_df, 1)
df_female_yob = yob_dist_df_sex(cleaned_yob_dist_df, 2)
df_male_yob.to_csv('prep_data/df_male_yob.csv')
df_female_yob.to_csv('prep_data/df_female_yob.csv')
