# Guess Age from Name

Let's say you receive an email from some dude named Ayden, and your guess is that he's a young guy based on your gut feeling about that name.
How correct is your guess?

In other words, what does the age distribution look like for males named Ayden?
My [web app](https://name-dater.herokuapp.com/) answers this question.


## Bayes Theorem

Using Bayes Theorem, we can calculate the posterier distribution `P(age | name)`:
```
P(age | name='Ayden')
= P(age and name='Ayden') / P(name='Ayden')
= P(name='Ayden' | age)P(age) / P(name='Ayden')
= P(name='Ayden' | age)P(age) / sum_i P(name='Ayden' | age=i)P(age=i)
```
Using data from the 
[Social Security Baby Names Dataset](https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-level-data),
you can get `P(name | age)`.

Using data from the 
[2016 US Census](https://factfinder.census.gov/bkmk/table/1.0/en/PEP/2016/PEPSYASEXN),
you can get `P(age)` for the currently alive population in 2016.


## Web App

Here's a screenshot of the [web app](https://name-dater.herokuapp.com/), which shows the age distribution for males named Ayden:
![webapp_screenshot](https://user-images.githubusercontent.com/26487650/31509250-ba6a0486-af35-11e7-80f4-0180fe4c8c1a.png)

Your hunch is right -- chances are Ayden is very young.
