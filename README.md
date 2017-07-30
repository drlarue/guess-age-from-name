# Guess Age from Name

Say you receive an email from some dude named Ayden, and you guess that he must be a young guy based on your gut feeling about that name.
How correct is your guess?

In other words, what does the age distribution look like for Ayden among males?
This code answers this question.


## Bayes Theorem

Using Bayes Theorem, we can calculate the posterier distribution `P(age | name)`:
```
P(age | name='Ayden')
= P(age and name='Ayden') / P(name='Ayden')
= P(name='Ayden' | age)P(age) / P(name='Ayden')
= P(name='Ayden' | age)P(age) / sum_i P(name='Ayden' | age=i)P(age=i)
```

## Example

Using data from the 
[Social Security Baby Names Dataset](https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-level-data),
you can get `P(name | age)`.

Using data from the 
[2016 US Census](https://factfinder.census.gov/bkmk/table/1.0/en/PEP/2016/PEPSYASEXN),
you can get `P(age)` for the currently alive population in 2016.

```python
from usa_setup import merged_name_df, cleaned_yob_dist_df
from guess_age import GuessAge

usa_age_guesser = GuessAge(merged_name_df, cleaned_yob_dist_df)
usa_age_guesser.pdf_plot('M', 'Ayden')
```

This plots the distribution of age of males named Ayden:
![pdf](https://user-images.githubusercontent.com/26487650/28755961-8d3da422-751a-11e7-85f1-34cf5927dace.png)

Your hunch is right -- chances are Ayden is very young.
