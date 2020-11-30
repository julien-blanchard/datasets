#!/usr/bin/env python
# coding: utf-8

# # **Programming for analytics: CA 1**
# 
# *   **Module owner**: Paul Laird
# 
# *   **Module code**: B9BA100
# 
# *   **Submitted by**: Julien Blanchard
# 
# *   **Student number**: 10564273
# 
# *   **Direct link (my GitHub page)**: [link](https://github.com/julien-blanchard/dbs)
# 
# *   **References**: I have based myself on the following three books for this CA, and would highly recommend them to anyone interested in Python and Data science / Data analytics ([picture here](https://drive.google.com/file/d/1BYaz3KQtj1kYtOGESvXtmkyh2dx-YSKB/view?usp=sharing)):
# 
# > [Data Science from Scratch](https://www.amazon.co.uk/Data-Science-Scratch-Principles-Python-ebook/dp/B07QPC8RZX/ref=sr_1_6?dchild=1&keywords=python+for+data+science&qid=1605271670&sr=8-6) by Joel Grus
# 
# > [Python for Data Analysis](https://www.amazon.co.uk/Python-Data-Analysis-Wes-Mckinney/dp/1491957662/ref=sr_1_1?dchild=1&keywords=data+analysis+with+python&qid=1606428279&sr=8-1) by Wes McKinney (the creator of Pandas)
# 
# > [Python Automation Cookbook](https://www.amazon.co.uk/Python-Automation-Cookbook-automation-processing-ebook/dp/B088NBRT6Z/ref=sr_1_3?dchild=1&keywords=automation+python&qid=1606428364&sr=8-3) by Jaime Buelta
# 
# *   **Python syntax and conventions**: All the variables in this Colab will be written following the same naming convention: "*my_variablename*". Whenever possible, I'll be defining functions. All these functions will be written following the same naming convention: "*make_actionname*".
# 
# 
# *   **Table of contents**
# 
# > 1) Extra work: creating our own txt files with Python
# 
# > 2) CA question 1
# 
# > 3) CA question 2
# 
# > 4) Extra work: some very basic data analysis
# 
# > 5) Extra work: some very basic email automation workflow

# # 1) Creating 3 txt files using Random and Names
# 
# To complete this CA, Paul has asked us to come up with three distinct .txt files:
# 
# *   Employees.txt, which contains one line for each employee with the following information, separated by tab characters (\t):
# 
# *surname | first Name | PPSNumber | standard hours | HourlyRate | OvertimeRate | taxcredit | standardband*
# 
# *   Hours.txt contains the following:
# 
# *dd/mm/yyyy | staffID | hours_worked*
# 
# *   Taxrates.txt contains the following information (%):
# 
# *standardrate | higherrate*
# 
# But rather than creating our employees / hours / rates .txt files manually, why don't we get Python to randomly generate everything for us?

# In[26]:


# we need to install the Names library first
# !pip install names

# these are the libraries we will be working with
import names
import random
import string
import pandas as pd
import numpy as np


# # Txt file 1: employees.txt
# 
# Using the Random and Names library, we're going to create a dataframe that contains all the informations required for the employees.txt file, then remove its header and save the file locally. To be fair, I had never heard of the [Names](https://pypi.org/project/names/) library before. It's actually pretty straightforward!

# In[31]:


# let's try and see how our names generator works
my_rand_name = names.get_full_name()

# according to the official documentation. Random can't generate letters. 
# But we need a letter for our PPS number! Let's be clever :)
# We're using the String library, which has a function that list all letters in the alphabet. 
my_alphabet = list(string.ascii_uppercase)

# we can now randomly pick any letter from the alphabet
my_rand_letter = random.choice(my_alphabet)

# now, onto our random employee IDs
my_rand_id = str(random.randint(1000,9999)) + random.choice(my_alphabet)

# for the hourly salary, any float between 12.0 and 20.0 will do
my_rand_salary = round(random.uniform(12, 20), 2)

# finally, let's print everything
print('Name:', names.get_full_name())
print('Staff ID:', str(random.randint(1000,9999)) + random.choice(my_alphabet))
print('PPS:', str(random.randint(1000000,9999999)) + random.choice(my_alphabet))
print('Hourly wage:', round(random.uniform(12, 20), 2))


# In[3]:


"""
We can now create a simple function that will generate lists, add dictionary keys to these lists, and pass
the whole thing into a Pandas dataframe. As an argument for our function, I have chosen to use the number
of employees that we want to create.
I'm setting 8 as the number of hours as this is the standard daily work hour volume in Ireland
"""
def make_employeesdataframe(howmany):
    my_employees, my_id, my_hours, my_salary, my_pps = [],[],[],[],[]
    for r in range(howmany):
        my_employees.append( names.get_full_name() )
    for r in range(howmany):
        my_id.append( str(random.randint(1000,9999)) + random.choice(my_alphabet) )
    for r in range(howmany):
        my_hours.append( str(8) )
    for r in range(howmany):
        my_salary.append( round(random.uniform(12, 30), 2) )
    for r in range(howmany):
        my_pps.append( str(random.randint(1000000,9999999)) + random.choice(my_alphabet) )
    # when creating a dataframe, the best approach is to use a dictionary, as the keys become the headers
    my_columns = {'name': my_employees, 'staff_id': my_id, 'pps': my_pps, 'hours': my_hours, 'hourly_rate': my_salary}
    df = pd.DataFrame(my_columns)
    return df


# In[4]:


# creating data for 50 employees
df_emp = make_employeesdataframe(51)

# making sure it worked
df_emp.head(5)


# In[5]:


# before we save our dataframe into a txt file, we have to split our name serie into first name and last name
df_emp['first_name'] = df_emp['name'].apply(lambda x: x.split(' ')[0])

# same for our last name, this time in second position, so [1]
df_emp['last_name'] = df_emp['name'].apply(lambda x: x.split(' ')[1])

# we can now drop our old 'name' serie, using axis=1
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html
df_emp = df_emp.drop(['name'], axis=1)

# and now onto our overtime salary. Let's be generous: it will be +30% of our base hourly income
df_emp['overtime_rate'] = df_emp['hourly_rate'].apply(lambda x: x * 1.3)
df_emp['overtime_rate'] = df_emp['overtime_rate'].apply(lambda x: round(x, 2))

# to be honest, I don't understand this tax credit / band stuff
# so I'll just base myself on the following link, sorry if it makes zero sense
# https://www.irishjobs.ie/careeradvice/understanding-your-payslip/

# they say that the tax credit is a % of your income. I'll go for 10%
df_emp['tax_credit'] = df_emp['hourly_rate'].apply(lambda x: (x /100) * 10 )
# standard band is the tax bracket, right? Above this, employees are taxed more. We'll set it at 20E/h
df_emp['standard_band'] = 20

# last thing, Paul wants the txt file to be in a specific order
my_columns = ['first_name', 'last_name', 'staff_id', 'pps', 'hours', 'hourly_rate', 'overtime_rate', 'tax_credit', 'standard_band']
df_emp = df_emp.reindex(columns=my_columns)

# showing our cleaned dataframe
df_emp.sample(3)


# In[6]:


"""
And finally, saving the df as a txt file. I struggled a bit for this, but found help here:
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_string.html
# https://stackoverflow.com/questions/51829923/write-a-pandas-dataframe-to-a-txt-file

Something quite interesting: when using df.to_string I got some weird spacing issues, and my txt file
would end up completely messed up. It seems that the best solution is to stick to df.to_csv and most 
importantly to keep either header or the index (which I had originally removed)
"""

df_emp.to_csv('employees.txt', header=True, index=False, sep=' ')


# # Text file 2: hours.txt
# 
# This is going to be much more straightforward. We're going to use Pandas' date_range() function, and then convert the datetime series to Y-M-D format, as date_range() by default adds hours (0), minutes (0), and seconds (0). The cool thing here is, we can generate a dataframe that is within any time range that we want to, as we can set up our starting and ending dates.

# In[7]:


"""
Defining a very simple function that creates a Pandas dataframe.
Setting the default daily worked hours to 8
Paul asked us to add in a PPS column, so for each day we have our employees covered
Also adding in an "actual worked hours" column, randomized between 4 (half-day) and 12 (who works more
than 12 hours in a day?). As you'll see below, we're using Numpy to generate these random integers
"""

def make_hoursdataframe(my_start, my_end):
    my_dates = pd.date_range(start=my_start, end=my_end)
    my_dict = {'date': my_dates}
    df_hours = pd.DataFrame(my_dict)
    df_hours['hours'] = 8
    df_hours['date'] = df_hours.date.map(lambda x: x.strftime('%Y-%m-%d'))
    return df_hours

# creating our dataframe, covering the second half of 2020
df_hours = make_hoursdataframe('06/1/2020', '12/31/2020')

# now we create a sub_df from our employees.txt, only using the PPS number and the 'expected hours'
# fun fact, for 10 minutes I couldn't merge the df. It turns our that my df_emp['hours'] had become a string...
df_pps = df_emp.filter(['staff_id', 'hours'])
df_pps['hours'] = df_pps['hours'].astype(int)

# LEFT JOIN on 'hours'
df_hours = pd.merge(df_hours, df_pps)

# finally, let's create a randomized 'actual work' column, based on:
# https://docs.scipy.org/doc/numpy-1.15.0/reference/routines.random.html
df_hours['actual_worked_hours'] = np.random.randint(4, 12, df_hours.shape[0])

# we no longer need the 'expected worked hours' as we've JOINed our dataframes
df_hours = df_hours.drop(['hours'], axis=1)

# showing our result
df_hours.head(20)


# In[8]:


# same process as above, when we created our employees.txt file
df_hours.to_csv('hours.txt', header=True, index=False, sep=' ')


# # Text file 3: taxrates.txt
# 
# Ok, I guess I'll have to be very honest here: I don't understand how this whole thing works. I guess I should actually be a little bit more aware of how the Irish tax system is structured, as I've been working in Ireland for over 10 years now.
# 
# Anyway, I'll again use the official [citizen information website](https://www.citizensinformation.ie/en/money_and_tax/tax/income_tax_credits_and_reliefs/introduction_to_income_tax_credits_and_reliefs.html) as a source for this.

# In[13]:


# third and last tine, let's create a dataframe building function!
def make_taxdataframe(working_hours):
    my_x, my_y = [20],[40]
    my_dict = {'standard_rate': my_x, 'higher_rate': my_y, 'hours': working_hours}
    df_tax = pd.DataFrame(my_dict)
    return df_tax

# creating this single row dataframe
df_tax = make_taxdataframe([8])
df_tax


# In[15]:


# and that's our third and last txt file!
# same process as above, when we created our employees.txt file
df_tax.to_csv('taxrates.txt', header=True, index=False, sep=' ')


# # 2) Getting our CA done
# Loading our freshly created txt files, and creating our payslips generating function!!!
# 
# I have uploaded the files onto my GitHub, in case you want to run the code yourself (I have also shared these files with my classmates, so you might see these same files and names again):
# *   [employees txt](https://github.com/julien-blanchard/dbs/blob/main/employees.txt)
# *   [hours txt](https://github.com/julien-blanchard/dbs/blob/main/hours.txt)
# *   [taxrates txt](https://github.com/julien-blanchard/dbs/blob/main/taxrates.txt)

# In[1]:


# importing our main module, in case we're doing this second step independantly from the first one
import pandas as pd


# In[3]:


# as weird as it seems, Pandas seems to read txt files through its read_csv function
# https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html
df_employees = pd.read_csv('employees.txt', sep=' ')
# adding in a full name series, as several people might share the same first or last name, right?
df_employees['full_name'] = df_employees.apply(lambda x:
                                               x['first_name'] 
                                               + ' ' 
                                               + x['last_name'],
                                               axis=1
                                              )

# next, let's load our hours.txt file. Same process, different dataframe name
df_hours = pd.read_csv('hours.txt', sep=' ')

# last but not least, here comes our taxrates.txt file
df_tax = pd.read_csv('taxrates.txt', sep=' ')


# # Function description:
# 
# **Foreword**:
# 
# I have chosen to go for pure Pandas, instead of relying on a for loop approach. However, as I wouldn't want to be penalised for not using one concept over another, I have made sure to use a different approach for the bonus sections. My initial approach was to define the three following classes: Employee, Hours, Tax. It would have looked a bit like this:
# 
# 
# ```
# class Employee:
#   def __init__(self, name):
#     self.by_name = df.loc[ (df['first_name'] == name)]
#   def get_filtered_df(self):
#     return self.by_name
#   def get_salary(self):
#     return self.by_name.at[0, 'hourly_rate']
# ```
# 
# **Chosen approach and basic requirement analysis**
# 
# However, I changed my strategy after attending several classes for our *Requirement Analysis* module. Our teacher explained to us that as Business Analysts, our priority was our client, and that it was essential to focus on clarity and feasibility. This is why I changed my approach to using pure Pandas for this exercise, and here is why:
# 
# *Problem recognition*:
# 
# *   Identifying our **stakeholders**: Who is our "client" here? **Who are we building this payslip generator for**? Who are the people who will use it? What type of data structure are they familiar with? 
# *   A quick search for "**Payroll specialist**" on Indeed ([link](https://ie.indeed.com/jobs?q=payroll+specialist&l=dublin)) shows that the most sought after skill for this type of role is **advanced Excel**. This most likely means that the people who work with payslips are accustomed to working with **tabular data**, which is exactly what Pandas provides.
# 
# *Quality function deployment (QFD)*:
# 
# *   Normal requirement: All our Payroll departments seems to want, is a simplified and automated way to generate individual payslips
# *   Expected requirement: Our Payroll department will most likely want to **store all this data** somewhere (probably on a monthly or quarterly basis). As we're merging several dataframes into a single dataframe (*df_temp*), all we would need to do is remove all the *print()* part from our function and replace these lines with *return df_temp*
# *   Expected requirement: Having a line by line, pure Pandas approach, will **allow non Python friendly people to make basic amendments** to the code. For this purpose, I have chunked the function you will see below into separate parts: dataframe handling, series handling, and printing. 
# *   Exciting requirement: Using a Pandas dataframe will allow our Payroll department to use a library like [XLWings](https://www.xlwings.org/) and get familiar with Python. On a side note, [O'Reilly just published a book](https://www.oreilly.com/library/view/python-for-excel/9781492080992/) written by the person who created **XLWings**. I have personally never used this library, but the book's table of content seems to focus greatly on implementing Python in "traditional" and "Excel oriented" businesses like **banks or insurance companies**.
# *   Exciting requirement: We could then create very fancy looking **pdf files** using an open source framework such as [ReportLab](https://www.reportlab.com/opensource/). Coincidentally, the official documentation for ReportLab cites Pandas as one of its better supported data sources.
# *   Exciting requirement: Last but not least, using a Pandas dataframe makes it quite easy to automate an email workflow, using [Smtplib](https://docs.python.org/3/library/smtplib.html)
# 
# **Methodology**:
# 
# *   One important thing is: most people don't work weekends! I have found a function in Pandas that transforms a YY-MM-DD datetime serie into days of the week, and I have then removed Saturdays and Sundays from our dataframe. Funnily enough, I'm writing this line on a Saturday at 11am, I guess we can call this bad karma :)
# 
# *   Another thing worth mentioning here: in Pandas, we don't need to specify the name of the columns that
# we are doing our JOIN on, unless they have different names. Here, all our txt files have a column named 'hours' and contain the exact same value: 8. No need to specify anything, Pandas does it for us. How cool is that? In SQL, we'd probably have wanted to come up with something along those lines:
# 
# ```
# WITH 
#     t2 AS (SELECT col2 FROM whatever_table2),
#     t3 AS (SELECT col2 FROM whatever_table3)
# SELECT
#     t1.col1, t2.col2, t3.col2
# FROM t1
# LEFT JOIN t2 ON t1.pps_number = t2.pps_number
# LEFT JOIN t3 ON t1.pps_number = t3.pps_number
# ```
# 
# * My whole idea is to filter out our *Employees.txt* by **employee_name**, our *Hours.txt* by **start_day** and **end_day**, and then to merge / left join all dataframes together
# 
# * What I do then is fairly straightforward: I **systematically create new series / columns**, based on the calculations I need. For instance you'll see a new serie for overtime hours, another one that transforms a date into a day or month string, etc...
# 
# **What I could improve**:
# 
# *   I only started learning Python about 3 years ago. Before that, and for many years, I was mainly an SQL user. The consequence of relaying for so many years on SQL and Excel is that I systematically tend to approach problems in terms of **tabular data**. It is quite difficult for me to approach data analysis and data visualisation issues in a more "programming" compliant mode.
# *   Because I merge dataframes and create new columns, we're a risk of gathering too much data and getting a **result overflow**. If we had more employees and a much larger timeframe, we could start running into some issues. To avoid that, we could break down our employees.txt by department (sales, HR, etc...) and our hours.txt by year.
# * I tend to to rely too much on **libraries / modules**, and not enough on "pure python". I think I would actually struggle more, but also learn a lot more, by not using Pandas. It wouldn't be suited for our Payroll department, but it would probably be an interesting exercise.

# In[4]:


def make_payslip(employee_name, start_day, end_day):
    """
    What we are doing here:
    # Filtering out our name and date range
    # Merging our dataframes, one at a time
    """
        # dataframes manipulation
    df_refinedhours = df_hours.loc[ (df_hours['date'] >= start_day) & (df_hours['date'] <= end_day) ]
    df_temp = df_employees.loc[ df_employees['full_name'] == employee_name]
    df_temp = pd.merge(df_refinedhours, df_temp)
    df_temp = pd.merge(df_temp, df_tax)
    """
    What we are doing here:
    # Before we start, I really dislike working with time series.
    It always takes me quite a bit a trial and error before I manage to get to what I want
    # So, we're converting our date serie to datetime format, then we extract the day of the week,
    then we extract the month, and then we remove our Saturdays and Sundays
    """
    # adding in some datetime series
    df_temp['date'] = pd.to_datetime(df_temp['date'])
    df_temp['day_name'] = df_temp['date'].dt.day_name()
    df_temp['month_name'] = df_temp['date'].dt.month_name()
    my_working_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    df_temp = df_temp.loc[ df_temp['day_name'].isin(my_working_days)]
    """
    What we are doing here:
    # We're using anonymous functions to create 2 new columns:
    one that tells you how many overtime hours you have worked, and a second one
    that shows how many regular hours you have worked
    # on a side note, if you apply a lambda function on a whole dataframe and not on a single serie,
    you HAVE to add axis=1 at the end, or you'll get an error code
    """
    # dealing with overtime work
    df_temp['overtime_worked'] = df_temp.apply(lambda x: 
                                               (x['actual_worked_hours'] - x['hours']) 
                                               if (x['actual_worked_hours'] > x['hours']) else 0, 
                                               axis=1
                                              )
    df_temp['regular_worked'] = df_temp.apply(lambda x: 
                                              x['actual_worked_hours'] 
                                              - x['overtime_worked'], 
                                              axis=1
                                             )
    df_temp['regular_paid'] = df_temp['regular_worked'] * df_temp['hourly_rate']
    df_temp['overtime_paid'] = df_temp['overtime_worked'] * df_temp['overtime_rate']
    """
    What we are doing here:
    # Ok, this is my moment of shame. As you'll see further down, I'm relying a lot on
    the at() function in Pandas to get my first row value. And for a good hour, whenever 
    I was changing the employee name, I would get no result. I then realised that my main
    dataframe was keeping the original indexing for each employee... :( I solved the issue
    by resetting the index!
    # 
    """
     # resetting our index to avoid indexing errors
    df_temp.reset_index(drop=True, inplace=True)
    """
    What we are doing here:
    # As mentioned above, I like SQL, and I went for a GROUP BY aggregation.
    # I really recommend this amazing article https://www.shanelynn.ie/summarising-aggregation-and-grouping-data-in-python-pandas/
    """
    # data aggregation
    my_groupby_regular = df_temp.groupby(
        ['full_name','month_name','hourly_rate'],
        as_index=False).agg(
        {'regular_worked':'sum', 'regular_paid':'sum'}
    )
    my_groupby_overtime = df_temp.groupby(
        ['full_name','month_name', 'overtime_rate'],
        as_index=False).agg(
        {'overtime_worked':'sum', 'overtime_paid':'sum'}
    )
    """
    What we are doing here:
    # Ok, I have one problem, and this problem isn't python related: I'm not sure I understand how the
    different tax bands work. Here's how I understand things: taxes in Ireland work by bracket, or ladder.
    Here we have a standard_band at 20 Euros per/hour. It means if person A and B make respectively
    17 and 19 Euros per/hour, they are taxed the same. However, person C who makes 21 falls under the upper bracket
    and is taxed more. Conveniently, Paul put the under 20E p/h bracket at 20% and the under 40E p/h bracket 
    at 40%. This is what you'll see in below for my_total_standardtaxes and my_total_highertaxes
    # as for the rest, othing fancy I guess, but I didn't want my print() statements to be too long,
    so I'm doing some final calculations here
        
    """
    # calculations
    my_total_standardtaxes = (
        (((sum(df_temp.hours) * df_temp.at[0, 'hourly_rate']) / 100) * df_temp.at[0, 'standard_rate']) 
        if (df_temp.at[0, 'hourly_rate'] <= df_temp.at[0, 'standard_rate']) 
        else 0
        )
    my_total_highertaxes =(
        (((sum(df_temp.hours) * df_temp.at[0, 'hourly_rate']) / 100) * df_temp.at[0, 'higher_rate']) 
        if (df_temp.at[0, 'hourly_rate'] > df_temp.at[0, 'standard_rate']) 
        else 0
        )    
    my_taxcredit = round(df_temp.tax_credit.sum())
    my_totalreductions = my_total_standardtaxes + my_total_highertaxes
    my_grosspay = (df_temp.regular_paid.sum() + df_temp.overtime_paid.sum()).round(4)
    my_startdate, my_enddate = df_temp.date.dt.date.min(), df_temp.date.dt.date.max()
    """
    What we are doing here:
    # Quick note: here, we could remove all the print() statements below and instead
    put return df_temp. This way, our Payroll department would be able to store the payslips
    #  As you can see I'm using df.at[] which conveniently returns any cell within our dataframe
    following x and y locations. I'm always taking the first indexed position
    """
    print('#########################################################################')
    print('StaffID:', df_temp.at[0,'staff_id'])
    print('Staff Name:', df_temp.at[0,'full_name'])
    print('PPSN:', df_temp.at[0,'pps'])
    print(f'Date covered: from {my_startdate} to {my_enddate}')
    print('Number of days covered in this payslip:', df_temp.date.count())
    print('###########################################################')
    print('REGULAR')
    print(my_groupby_regular)
    print('OVERTIME')
    print(my_groupby_overtime)
    print('###########################################################')
    print('Gross pay:\t', my_grosspay)
    print('###########################################################')
    print(f'Standard band (if applies):\t {my_total_standardtaxes}')
    print(f'Higher rate (if applies):\t {my_total_highertaxes}')
    print('Total deductions:', my_totalreductions)
    print('Tax credit:\t', my_taxcredit)
    print('Net deductions:\t', (my_totalreductions - my_taxcredit).round(2))
    print('Net pay:\t', (my_grosspay + my_taxcredit - my_totalreductions).round(2))


# In[36]:


"""
Getting a few random employee mames, for our function below.
Just run this cell as many times as needed, and pick whichever name you see below to create a payslip
"""
# using a simple for loop for this
for x,y in enumerate(df_employees.full_name.sample(4)):
    print('Sample employee name %d:\n'%(x+1),y)


# In[5]:


"""
There we go, we can now pass three arguments into our function: the employee's name, a start date,
and an end date. This way, we can pick one day, one month, five weeks, etc...
Of course, if we pick a Saturday or a Sunday, or if we input 'Xdfsfs' as an employee name, we'll
get an error. So I'm adding an error exception message.
"""
# calling our previously created function
try:
    make_payslip('Danny Crews', '2020-10-01', '2020-11-02')
except:
    print('You have picked a wrong employee name, or a weekend day!')


# In[17]:


"""
And now if we want to apply this function to several employees
I'm limiting it to 2 as I don't want to this ipynb file to double in size :)
"""
for employee in df_employees.full_name.to_list()[:2]:
    print(make_payslip(employee, '2020-10-01', '2020-11-02'))


# # Next, onto the second question of our CA!
# 
# "*Also output the weekly average gross pay for all workers each week, and the six-week rolling average gross pay for each employee with over six weeks' pay records*"
# 
# Ok, for this is the tricky part. Not in terms of using Python, but in terms of understanding the question. We actually had a 30 minute video conference call with my group, during which we all tried to explain how we thought we understood what Paul wanted here. My approach is the following:
# 
# *   Paul wants first an ouput per week, and then a second output per employee over a 6 week period of time. it means that in both cases our function parameters have to be '**start_week**' and '**end_week**'. Indeed, if Paul wants two functions that very much do the same thing (as this is one single CA question), then we have to make sure our function parameters work for the two ouputs he wants.
# 
# *   So, to achieve this, we're first goung to make some very slight amendments to the function we defined in question 1, but the overall logic, structure, and approach will remain the same.
# 
# *   Then we're write add two additional arguments to our new function that should allow our Payroll department to be able to output some very useful data: the first one will be **GROUP BY** argument, allowing us to output data by week, or month, or employee name, etc... And the second one will define how we want our data **aggregated** in our GROUPed BY clause.
# 
# Without further ado, let's jump over to the first part: "*output the weekly average gross pay for all workers each week*"

# In[13]:


def make_weeklygrossaverage(start_week, end_week, group_by, aggregated):
    """
    What we are doing here:
    # merging our dataframes, the same way we did before
    """
    df_temp = pd.merge(df_employees, df_hours)
    df_temp = pd.merge(df_temp, df_tax)
    """
    What are doing here:
    # I found this super useful function in Pandas that return the number of the week for any given date.
    For instance, as I'm finishing this we're on Saturday 28th October 2020 and therefore on week 48 this year
    # One caveat though: depending on which version of Pandas you are using, you will either need to use:
    .dt.week
    OR
    .dt.isocalendar().week
    """
    # again, adding in some datetime series, with this time a week count
    df_temp['date'] = pd.to_datetime(df_temp['date'])
    df_temp['day_name'] = df_temp['date'].dt.day_name()
    # adding a month column is an extra, but it'll make sense later
    df_temp['month_name'] = df_temp['date'].dt.month_name()    
    
    # df_temp['week_number'] = df_temp['date'].dt.isocalendar().week
    df_temp['week_number'] = df_temp['date'].dt.week
    
    # removing weekend days again
    my_working_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    df_temp = df_temp.loc[ df_temp['day_name'].isin(my_working_days)]
    df_temp = df_temp.loc[ (df_temp['week_number'] >= start_week) & (df_temp['week_number'] <= end_week) ]
    
    # Dealing with overtime / regular work the same way we did before
    df_temp['overtime_worked'] = df_temp.apply(lambda x: 
                                               (x['actual_worked_hours'] - x['hours']) 
                                               if (x['actual_worked_hours'] > x['hours']) else 0, 
                                               axis=1
                                              )
    df_temp['regular_worked'] = df_temp.apply(lambda x: 
                                              x['actual_worked_hours'] 
                                              - x['overtime_worked'], 
                                              axis=1
                                             )
    
    # for this last column, we are simply adding our 2 previously created series!
    df_temp['total_gross_paid'] = df_temp.apply(lambda x:
                                              (x['regular_worked'] * x['hourly_rate'])
                                              + (x['overtime_worked'] * x['overtime_rate']),
                                              axis=1
                                              )
    
    # and finally, using once again a GROUP BY aggregation, I'm getting the average gross pay by week
    df_weeklygrossaverage = df_temp.groupby(group_by, as_index=False).agg({'total_gross_paid': aggregated})
    # this is completely optional, but I'm renaming the headers to match Paul's
    # Please note that inplace=True means we're saving our changes to the dataframe
    df_weeklygrossaverage.rename(columns={'total_gross_paid': 'aggregated'}, inplace=True)
    return df_weeklygrossaverage

# if you want all the weeks for the year simply pass 0,100 as arguments (though there are only 56 weeks per year)
# as you can see, I'm aggregating by week number, and getting the mean
# we're doing some sort of SELECT week_number, AVG(salary) FROM df GROUP BY week_number
my_output = make_weeklygrossaverage(0, 100, 'week_number', 'mean')
# the reason why we're not getting more weeks covered is that my hours.txt only has values from June to December
my_output


# Now, onto the second part of this question: "*and (also output) the six-week rolling average gross pay for each employee with over six weeks' pay records*"
# 
# What we're doing here is very simple: instead of doing a **GROUP BY** on weeks, we're doing a **GROUP BY** on employee names.
# 
# In other words, we're going from this:
# ```
# df_weeklygrossaverage = df_temp.groupby('week_number', as_index=False).agg({'total_gross_paid': 'mean'})
# ```
# to this:
# ```
# df_weeklygrossaverage = df_temp.groupby('full_name', as_index=False).agg({'total_gross_paid': 'mean'})
# ```

# In[14]:


# if you want all the weeks for the year simply pass 0,100 as arguments (though there are only 56 weeks per year)
# and this time, we're aggregating by name
my_output = make_weeklygrossaverage(50, 55, 'full_name', 'mean')
# the reason why we're not getting more weeks covered is that my hours.txt only has values from June to December
my_output


# In[16]:


# and now the cool thing, we can GROUP BY other stuff, like months!
my_output = make_weeklygrossaverage(0, 100, 'month_name', 'mean')
# the reason why we're not getting more weeks covered is that my hours.txt only has values from June to December
my_output


# # 3) Extra 1: Having some fun with our dataframe
# 
# What if we added some more series, like email addresses, age, role, etc..?
# 
# To do so, we're going to create a fictional company named "MScBizAnalyticsDBS". What do we do? We sell paper, [of course](https://media4.giphy.com/media/5wWf7GR2nhgamhRnEuA/giphy.gif?cid=ecf05e47m5len2ftyls2jzt0l43y5msp07fskijbp23eftof&rid=giphy.gif).

# In[3]:


# we'll be needing some additional libraries for this
import numpy as np
import pandas as pd
import altair as alt


# In[4]:


# importing our df
df = pd.read_csv('employees.txt', sep=' ')

# first, let's create a randomized age column, based on:
# https://docs.scipy.org/doc/numpy-1.15.0/reference/routines.random.html
df['age'] = np.random.randint(18, 61, df.shape[0])


# In[5]:


"""
Next, let's assign an email address to each employee
"""

df['full_name'] = df.apply(lambda x: x['first_name'] + ' ' + x['last_name'], axis=1)

df['email'] = df.apply(lambda x: x['first_name'] + '.' + x['last_name'] + '@MScBizAnalyticsDBS.com', axis=1)
df['email'] = df['email'].apply(lambda x: x.lower())


# In[6]:


# and finally, let's try and see who's doing what, based on the salary column

# let's define an upper tier salary base, combining the salary mean and standard deviation
my_upper_tier = df.hourly_rate.mean() + df.hourly_rate.std()
my_string = 'Managers in this company make more than: {x} EUR per hour'
my_salary = round(df.hourly_rate.mean() + df.hourly_rate.std(), 2)
print(my_string.format(x=my_salary))

# we can also create a categorical serie, based on the simple calculation we just established
def make_company_role(salary):
    if salary >= my_upper_tier:
        return 'manager'
    else:
        return 'employee'

# applying this function to a new serie
df['role'] = df['hourly_rate'].apply(make_company_role)


# In[7]:


# showing what columns we now have
df.sample(1)


# In[8]:


# we can now get a grouped by overview of our company
df_temp = df.groupby('role', as_index=False).agg( {'hourly_rate': 'mean', 'age': 'mean'} )
df_temp


# In[9]:


"""
Ok, so for this part, I have to say that I'm a big fan of a visualisation library called Altair.
It can output interactive charts, like Bokeh or Plotly, but is much easier to use.
Simply put your mouse cursor over the charts below and you'll see some interactive data
Over the past few months at work, I have tended to use Altair more frequently than Seaborn
"""
# creating a left chart forst
my_leftchart = alt.Chart(df).mark_bar().encode( # we have selected df as our dataframe
    x=alt.X('hourly_rate:Q', bin=True), # our X, in quantitative format
    y=alt.Y('count()'),
    color=alt.Color('role', scale=alt.Scale(scheme='lightgreyred')), # this works like 'hue' in Seaborn
    tooltip = [alt.Tooltip('full_name'), # it's this part that determine which serie you want to make interactive
               alt.Tooltip('hourly_rate'),
               alt.Tooltip('overtime_rate')]
).properties( # nothing crazy here, just our chart size and title
    width=350,
    height=250,
    title='Hourly rate distribution'
).interactive()

my_rightchart = alt.Chart(df).mark_bar().encode(
    x=alt.X('age:Q', bin=True),
    y=alt.Y('count()'),
    color=alt.Color('role', scale=alt.Scale(scheme='lightgreyred')),
    tooltip = [alt.Tooltip('full_name'),
               alt.Tooltip('age')]
).properties(
    width=350,
    height=250,
    title='Age distribution'
).interactive()

alt.hconcat(my_leftchart, my_rightchart).configure_axis( # concatenating our 2 charts
    grid=False
).configure_view(
    strokeWidth=0
).configure_title(
fontSize=20
)


# So what can we see from the two charts above?
# *   We have a rather strange salary distribution (left chart), as we can see that most of our employees are either on the lowest extreme of the salary range, or on the higher extreme of the salary range. Maybe we should consider offering a more balanced retribution approach?
# *   The bar chart on the right seems to indicate that most of our employees are between the age of 20 and 25, while most of our managers are betweem 45 and 50 years old. This should raise some questions: Why are our employees so young? Could this be related to the salary imbalance we saw on the other chart? This might indicate that we're good at hiring younger people, but maybe not at keeping them?

# # 4) Extra 2: Automating payslip emails
# 
# For our last part, I won't go into anything too fancy. Ideally, we would want to remove all the print() lines from our CA function, and replace them with '*return df_temp*', which would then create a single dataframe per employee.
# 
# We could then loop througn all our employees, and create an individual dataframe for each, or for some of them.

# In[27]:


# let's import all the modules we will need for this exercise
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys


# In[ ]:


def make_payslip_email(sender, receiver, password, subject, payslip_df):
    # account and message
    my_sender_email = sender  # I created this address specifically for this project!
    my_receiver_email = receiver  # Enter receiver address
    my_password = password # Please open the password.txt file I have attached to my CA submission 

    # let's get started!
    my_message = MIMEMultipart()
    # Here we're defining our subject. Instead of 'Your' we could use an f string loop through our employees' name
    my_message['Subject'] = subject
    # That's pretty straightforward
    my_message['From'] = my_sender_email
    # more interesting: it's in list format! Which means we could again loop through our employees, add some conditions, etc..
    my_recipients = [my_receiver_email] 
    # this part I'm not sure of, but it seems to work. I basically used the default setting from the official library 
    # documentation: https://docs.python.org/2.0/lib/SMTP-example.html
    my_emaillist = [m.strip().split(',') for m in my_recipients]
    # that's quite cool: we can add some HTML formatting and simply add our Pandas dataframe at the end!!
    my_html = """    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(payslip_df.to_html()) # here I have put df_temp as my payslip_df, but each payslip would be unique and generated through a loop
    # we're going for hmtl, which is the default format
    my_email = MIMEText(my_html, 'html')
    # and finally, we attach the email
    my_message.attach(my_email)
    """
    So here I ran into some issues. Though I have activated the gMail account, it seems that because my
    account is too recent and because I haven't sent enough emails, I'm in some sort of restricted accounts pool.

    To bypass that, if you get an authentification error, follow these steps:
    1. Confirm that recent logins really were from you on the [Google account security page](https://myaccount.google.com/security)
    2. Unlock the account by [entering a captcha](http://www.google.com/accounts/DisplayUnlockCaptcha).

    I found the solution here: https://help.pythonanywhere.com/pages/SMTPForFreeUsers

    """
    # let's create an SMTP session. Port 587 is the official gMail port
    # https://support.google.com/a/answer/176600?hl=en
    my_session = smtplib.SMTP('smtp.gmail.com', 587) 
    # start TLS for security 
    my_session.starttls() 
    # Authentication 
    my_session.login(my_sender_email, my_password)
    # sending the mail 
    send_payslip = my_session.sendmail(message['From'], my_emaillist , my_message.as_string()) 
    return send_payslip
    
make_payslip_email('dbsstudentproject2020@gmail.com','suzanne.rievley@mscbizanalyticsdbs.com','xxxxxxx','Your payslip',df_temp)


# # Final words
# 
# That's pretty much it! I hope you have enjoyed reading this ipnyb file as much as I gave enjoyed writing it.
# 
# Thanks for your time!
