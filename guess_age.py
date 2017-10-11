import numpy as np
import pandas as pd
#from matplotlib import pyplot as plt # remove for heroku app

class GuessAge:
    """
    Loads the data and provides methods to calculate probability of age given name.
    """
    def __init__(self):
        self.df_male_name = pd.read_csv('prep_data/df_male_name.csv', index_col=[0, 1])
        self.df_female_name = pd.read_csv('prep_data/df_female_name.csv', index_col=[0, 1])

        self.male_name_list = self.df_male_name.loc[1916, :].index.tolist()
        self.female_name_list = self.df_female_name.loc[1916, :].index.tolist()

        self.df_male_yob = pd.read_csv('prep_data/df_male_yob.csv', index_col=0)
        self.df_female_yob = pd.read_csv('prep_data/df_female_yob.csv', index_col=0)


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


    '''
    def pdf_plot(self, sex, name):
        """
        Plots pdf of age for the given name among the given sex.
        Inputs:
            * sex: 'M' or 'F'
            * name: e.g., 'Tarzan', 'Jane'
        """
        if ((sex == 'M' and name.lower() not in self.male_name_list) or
                (sex == 'F' and name.lower() not in self.female_name_list)):
            return ("Sorry, the database doesn't contain any {} named {}".
                    format('males' if sex == 'M' else 'females', name.title()))

        else:
            df = self.p_yob_given_name(sex, name)
            df['age'] = df.yob.apply(lambda x: 2017-x)
            df.sort_values(['age'], inplace=True)

            plt.plot(df.age, df.p)
            plt.xlabel('Age')
            plt.ylabel('Probability')
            plt.xlim([1, 100])
            plt.xticks(range(0, 100, 5))
            plt.title('Age Distribution of {} Named {}'.
                      format('Males' if sex == 'M' else 'Females', name.title()))
            return plt.show()
    '''
