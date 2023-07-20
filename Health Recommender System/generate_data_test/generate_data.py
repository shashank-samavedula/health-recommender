#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import numpy as np
import os
import boto3


# In[19]:


s3_resource = boto3.resource('s3')

# set the bucket name and file name
bucket_name = 'adbmsla2'


# In[20]:


#generate 500 female (gender value as 1) and then change gender value as 0 and generate 500 male records
age=[]
gender=[]
chestpaintype=[]
bp=[]
cholestrol=[]
fbs = [random.randint(0, 1) for i in range(500)]
ekg=[random.randint(0, 2) for i in range(500)]
maxhr=[]
enigma = [random.randint(0, 1) for i in range(500)]
stdp = np.random.uniform(low=0.0, high=4.0, size=500)
slope=[random.randint(1, 2) for i in range(500)]
vessels=[]
thalium=[]
skinthickness=[]
insulin=[]
diabetesp=np.random.uniform(low=0.0, high=2.0, size=500)
pregencies=[]
glucose=[]
for i in range(500):
 age.append(random.randint(25, 80))
 gender.append(1)
 chestpaintype.append(random.randint(1, 4))
 bp.append(random.randint(100, 180))
 cholestrol.append(random.randint(100, 570))
 maxhr.append(random.randint(100, 200))
 vessels.append(random.randint(0,3))
 thalium.append(random.randint(3,7))
 skinthickness.append(random.randint(0,60))
 insulin.append(random.randint(0,900))
 pregencies.append(random.randint(0,10))
 glucose.append(random.randint(70,200))


# In[21]:


#get random malaria image
malariadata=[]
# list files in directory
directory = '/home/ubuntu/data/malariadata/'
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
for i in range(500):
 selected_file = random.choice(files)
 readfile=directory+selected_file
 file_name = str(i+500)+'_malaria.png'
 s3_resource.Bucket(bucket_name).upload_file(readfile,file_name )
 # get the object URL
 object_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
 malariadata.append(object_url)
#get random covid image
coviddata=[]
# list files in directory
directory = '/home/ubuntu/data/covid19data/'
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
for i in range(500):
 selected_file = random.choice(files)
 readfile=directory+selected_file
 file_name = str(i+500)+'_covid.jpeg'
 s3_resource.Bucket(bucket_name).upload_file(readfile,file_name )
 # get the object URL
 object_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
 coviddata.append(object_url)
#get random mentalhealthfile
mentalhealthdata=[]
# list files in directory
directory = '/home/ubuntu/data/mentalhealthdata/'
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
for i in range(500):
 selected_file = random.choice(files)
 readfile=directory+selected_file
 file_name = str(i+500)+'_mentalh.csv'
 s3_resource.Bucket(bucket_name).upload_file(readfile,file_name )
 # get the object URL
 object_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
 mentalhealthdata.append(object_url)



# In[22]:


dynamodb = boto3.client('dynamodb')
for i in range(500):
  response = dynamodb.put_item(
        TableName='adbmsla2n',
        Item={
            'id': {'N': str(i+500)},
            'age': {'N': str(age[i])},
            'gender': {'N': str(gender[i])},
            'chestpaintype': {'N': str(chestpaintype[i])},
            'bp': {'N': str(bp[i])},
            'cholestrol':{'N':str(cholestrol[i])},
            'fbs':{'N':str(fbs[i])},
            'ekg':{'N':str(ekg[i])},
            'maxhr':{'N':str(maxhr[i])},
            'enigma':{'N':str(enigma[i])},
            'stdp':{'N':str(stdp[i])},
            'slope':{'N':str(slope[i])},
            'vessels':{'N':str(vessels[i])},
            'thalium':{'N':str(thalium[i])},
            'skinthickness':{'N':str(skinthickness[i])},
            'insulin':{'N':str(insulin[i])},
            'diabetesp':{'N':str(diabetesp[i])},
            'pregencies':{'N':str(pregencies[i])},
            'glucose':{'N':str(glucose[i])},
            'malariadata': {'S': malariadata[i]},
            'coviddata': {'S': coviddata[i]},
            'mentalhealthdata': {'S': mentalhealthdata[i]}
            }
           
          )
  print(response)


# In[3]:


response = dynamodb.scan(
    TableName='adbmsla2',
    Select='COUNT'
)
count = response['Count']
print(f"Number of rows in table: {count}")


# In[8]:


import boto3

# create a DynamoDB client
dynamodb = boto3.client('dynamodb')
attrlist=[]
valuelist=[]
# scan the DynamoDB table and print each item
response = dynamodb.scan(TableName='adbmsla2')
items = response['Items']
print(type(items))
with open ('/home/ubuntu/data/temp/testdata.txt','w') as f:
    f.write(str(items))
print(len(items))
for item in items:
  #print(item)
  i=5
print(item)
#for ele in item:
#    attrlist.append(ele)
#    for k in item[ele]:
#        valuelist.append((item[ele][k]))
#    #print(item[ele])
#print(attrlist)
#print(type(valuelist[0]))


# In[ ]:


#sample item from dynamo DB
item={'glucose': {'N': '157'}, 'mentalhealthdata': {'S': 'https://adbmsla2.s3.amazonaws.com/735_mentalh.csv'}, 'ekg': {'N': '0'}, 'enigma': {'N': '0'}, 'malariadata': {'S': 'https://adbmsla2.s3.amazonaws.com/735_malaria.png'}, 'insulin': {'N': '783'}, 'stdp': {'N': '2.171652076245886'}, 'pregencies': {'N': '5'}, 'cholestrol': {'N': '195'}, 'gender': {'N': '1'}, 'maxhr': {'N': '169'}, 'bp': {'N': '128'}, 'chestpaintype': {'N': '2'}, 'coviddata': {'S': 'https://adbmsla2.s3.amazonaws.com/735_covid.jpeg'}, 'skinthickness': {'N': '21'}, 'diabetesp': {'N': '0.9929540597752751'}, 'thalium': {'N': '6'}, 'slope': {'N': '1'}, 'fbs': {'N': '0'}, 'vessels': {'N': '2'}, 'id': {'N': '735'}, 'bmi': {'N': '44.44315832975757'}, 'age': {'N': '63'}}


# In[17]:


import urllib.request

s3_url = item['malariadata']['S']
print(s3_url)
response = urllib.request.urlopen(s3_url)
data = response.read()
print(type(data))
with open('/home/ubuntu/data/temp/test.png','wb') as f:
    f.write(data)


# In[2]:


import boto3
import numpy as np

# create a DynamoDB client
dynamodb = boto3.client('dynamodb')
bmi = np.random.uniform(low=0.0, high=55.0, size=1000)

# scan the table to retrieve all items
response = dynamodb.scan(TableName='adbmsla2')
items = response['Items']

# add a new column to each item
i=0
for item in items:
    item['bmi'] = {'N': str(bmi[i])}
    i=i+1

    # write the updated item back to the table
    dynamodb.put_item(TableName='adbmsla2', Item=item)

