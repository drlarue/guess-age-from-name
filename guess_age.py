import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt

class GuessAge:
    """
    Holds the data and provides methods to calculate probability of age given name.
    Inputs:
        * df_raw_name: dataframe with columns ['name', sex', 'yob', 'no_count']
        * df_raw_yob: dataframe with columns ['sex', 'yob', 'no_count']
    """
    def __init__(self, df_raw_name, df_raw_yob):
        self.df_male_name, self.male_name_list = self.master_df_sex(df_raw_name, 1)
        self.df_female_name, self.female_name_list = self.master_df_sex(df_raw_name, 2)

        self.df_male_yob = self.yob_dist_df_sex(df_raw_yob, 1)
        self.df_female_yob = self.yob_dist_df_sex(df_raw_yob, 2)


    def master_df_sex(self, merged_name_df, sex):
        """
        Split df_raw_name by sex then create full yob-name product space
        """
        df_sex = merged_name_df[merged_name_df.sex == sex].copy()
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

        return master_df, unique_names_by_sex


    def yob_dist_df_sex(self, cleaned_yob_dist_df, sex):
        """
        Split df_raw_yob by sex and calculate proportion of yob's
        """
        df_sex = cleaned_yob_dist_df[cleaned_yob_dist_df.sex == sex].copy()
        df_sex['proportion'] = (df_sex.no_count / df_sex.no_count.sum())

        df_sex.set_index(['yob'], inplace=True)

        return df_sex[['proportion']]


    def p_name_given_yob(self, df, yob, name):
        p = df.loc[yob, name] / df.loc[yob, :].sum()
        return p[0]


    def p_yob(self, df, year):
        return df.loc[year].proportion


    def p_yob_given_name(self, sex, raw_name):
        name = raw_name.lower()

        if sex == 'M':
            df_name = self.df_male_name
            df_yob = self.df_male_yob
        elif sex == 'F':
            df_name = self.df_female_name
            df_yob = self.df_female_yob
        else:
            return "Enter 'M' or 'F'"

        l = {}
        p3 = 0

        for i in np.arange(1916, 2017):
            p1 = self.p_name_given_yob(df_name, i, name)
            p2 = self.p_yob(df_yob, i)
            p3 += p1 * p2
            l[i] = p1 * p2

        df = pd.DataFrame(list(l.items()), columns=['yob', 's'])
        df['p'] = df.s / p3

        return df[['yob', 'p']]

    def pdf_plot(self, sex, name):
        """
        Plots pdf of age for the given name among the given sex.
        Inputs:
            * sex: 'M' or 'F'
            * name: e.g., 'Tarzan', 'Jane'
        """
        df = self.p_yob_given_name(sex, name)
        df['age'] = df.yob.apply(lambda x: 2017-x)
        df.sort_values(['age'], inplace=True)

        plt.plot(df.age, df.p)
        plt.xlabel('Age')
        plt.ylabel('Probability')
        plt.xlim([0, 100])
        plt.xticks(range(0, 100, 5))
        plt.title('Age Distribution of {} Named {}'.format('Males' if sex == 'M'
                                                           else 'Females', name.title()))
        return plt.show()
