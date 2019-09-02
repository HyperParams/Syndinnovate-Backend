#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd


# \copy (Select * From reviews) To 'resources/reviews_data.csv' With CSV

# In[53]:


df = pd.read_csv('resources/reviews_data.csv',names=['id',
 'mobilenumber',
 'digitalscore',
 'is_specially_abled',
 'waitingtime',
 'oncountertime',
 'cancellations',
 'review',
 'ratings',
 'POV'
])


# In[58]:


df.head()


# In[59]:


data = df[['digitalscore', 'is_specially_abled', 'waitingtime', 'oncountertime', "POV", "ratings"]].values
rows=data[:,4]==9
new=data[rows]
new


# In[67]:


columns = {
    0:'digitalscore',
    1:'is_specially_abled',
    2:'waitingtime',
    3:'oncountertime',
    4:"POV",
    5:"ratings"
}


# In[72]:


data = df[['digitalscore', 'is_specially_abled', 'waitingtime', 'oncountertime', "POV", "ratings"]].values
min_rating = min(data[:, -1])
max_rating = max(data[:, -1])
variances = []
ratings = []
for i in range(min_rating, max_rating+1):
    temp=data[:,-1]==rating
    rows=data[temp]
    if rows.shape[0]==0:
        continue
    ratings.append(i)
for rating in ratings:
    temp=data[:,-1]==rating
    rows=data[temp]
    column_variances = []
    for column in range(6):
        x_bar = rows[:,column].mean()
        column_variances.append(((rows[:,column]-x_bar)**2).mean())
    variances.append((column_variances.index(min(column_variances)), min(column_variances)))
variances


# In[ ]:


with open('resources/params.dat', 'rb') as file:
    try:
        dictionary = pickle.load(file)
    except EOFError:
        pass
min_change = dictionary["min_change"]
max_change = dictionary["max_change"]


# In[73]:


# ratings= [1,2,3,4,5,6,7,8,9,10]
steps = len(ratings)
step_width = (max_change-min_change)/(steps)
changes = [max_change-i*step_width for i in range(steps)]
changes


# In[ ]:


with open('resources/weights.dat', "rb") as file:
    try:
        weights = pickle.load(file)
    except EOFError:
        pass


# In[ ]:


for i in range(len(variances)):
    column = columns[variances[i][0]]
    if column=="oncountertime":
        continue
    weights[column]+=changes[i]


# In[ ]:


with open('resources/weights.dat', "wb") as file:
    pickle.dump(weights, file)

pi=df.ratings.mean()
pii = pi - params['pi'][-1]
params['pi'].append(pi)
params['pii'].append(pii)
with open('resources/params.dat', 'wb') as file:
    pickle.dump(params, file)
