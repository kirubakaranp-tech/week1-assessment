#!/usr/bin/env python
# coding: utf-8

# # Week 1 Employee Analysis
# This notebook explores the employee dataset with Pandas.

# ## Load the data

# In[1]:


import pandas as pd

employees = pd.read_csv("../data/employees.csv")
employees.head()


# ## Time one operation

# In[2]:


get_ipython().run_line_magic('timeit', 'employees["salary"].mean()')


# ## Department summary

# In[3]:


department_summary = employees.groupby("department")["salary"].agg(["count", "mean", "max"])
department_summary


# ## Findings
# IT has the largest team, while Finance has the highest individual salary.
