import chart_studio.plotly as py
from plotly.graph_objs import *
import os
import boto3
py.sign_in('srinidhibits', 'lPLQerip7xcwD4SGWClB')

# define the table name
table_name = 'adbmsla2'

agegr = [ "25-40", "40-60", "60-70", "70-80", "80-100" ]
# Define age groups
age_groups = [(25, 40), (40, 60), (60, 70), (70, 80),(80,100)]

def init_cnt():
# Initialize counters
    counts = {}
    for gender in [0, 1]:
        counts[gender] = {}
        for age_group in age_groups:
            counts[gender][age_group] = 0
    return counts

def get_lists(dict1):
    list1 = []
    list2 = []
    for i in dict1:
        for ele in dict1[i]:
            list1.append(dict1[i][ele])
    list2 = list1[5:]
    list1 = list1[0:5]
    return list1, list2

def get_summary():
    # create a boto3 client for DynamoDB
    dynamodb = boto3.client('dynamodb')
    #get number of people having covid
    filter_expression = 'isCovid > :isCovid'
    # define the attribute values to be substituted in the filter expression
    expression_attribute_values = {':isCovid': {'N': '0.5'}}
    response = dynamodb.scan(
    TableName=table_name,
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values
    )
    clist=response['Items']
    nCovid=len(clist)

    #get number of people having pneuomonia
    filter_expression = 'isPneuomonoa > :isPneuomonoa'
    # define the attribute values to be substituted in the filter expression
    expression_attribute_values = {':isPneuomonoa': {'N': '0.5'}}
    response = dynamodb.scan(
    TableName=table_name,
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values
    )
    plist=response['Items']
    nPneuomia=len(plist)

    #get number of people having malaria
    filter_expression = 'isMalaria > :isMalaria'
    # define the attribute values to be substituted in the filter expression
    expression_attribute_values = {':isMalaria': {'N': '0.5'}}
    response = dynamodb.scan(
    TableName=table_name,
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values
    )
    mlist=response['Items']
    nMalaria=len(mlist)

    #get number of people having diabetes
    filter_expression = 'isDiabetes > :isDiabetes'
    # define the attribute values to be substituted in the filter expression
    expression_attribute_values = {':isDiabetes': {'N': '0.5'}}
    response = dynamodb.scan(
    TableName=table_name,
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values
    )
    dlist=response['Items']
    nDiabetes = len(dlist)

    #get number of people having depression
    filter_expression = 'isDepression = :isDepression'
    # define the attribute values to be substituted in the filter expression
    expression_attribute_values = {':isDepression': {'N': '1'}}
    response = dynamodb.scan(
    TableName=table_name,
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values
    )
    dplist=response['Items']
    nDepression=len(dplist)

    #get number of people having heartdisease
    filter_expression = 'isHeartDisease = :isHeartDisease'
    # define the attribute values to be substituted in the filter expression
    expression_attribute_values = {':isHeartDisease': {'N': '1'}}
    response = dynamodb.scan(
    TableName=table_name,
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values
    )
    hlist=response['Items']
    nHeartDisease=len(hlist)

    trace1 = {
    "type": "pie", 
    "labels": ["COVID", "Pneumonia", "Malaria", "Diabetes","Depression","Heart"], 
    "values": [nCovid,nPneuomia,nMalaria,nDiabetes,nDepression,nHeartDisease]
    }
    data = Data([trace1])
    layout = {
    "title": "Patient Summary", "title_x":0.5
    }
    fig = Figure(data=data, layout=layout)
    #plot_url = py.plot(fig)
    img_path = '/image/summary.png'
    fig.write_image(os.path.curdir + '/static' + img_path)

    # Creating Dict
    diseaseDict = dict()
    diseaseDict['Malaria'] = nMalaria
    diseaseDict['Pneumonia'] = nPneuomia
    diseaseDict['Depression'] = nDepression
    diseaseDict['Covid'] = nCovid
    diseaseDict['Diabetes'] = nDiabetes
    diseaseDict['Heart Disease'] = nHeartDisease

    return img_path, diseaseDict 

def get_malaria():
    counts = init_cnt()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    # Scan the table and count Covid cases by gender and age group
    response = table.scan()

    for item in response['Items']:
        age = item['age']
        gender = item['gender']
        isMalaria = item['isMalaria']
        
        for age_group in age_groups:
            if age >= age_group[0] and age < age_group[1]:
                if isMalaria > 0.5:
                    counts[gender][age_group] += 1

    dict1 = counts
    list1, list2 = get_lists(dict1)
    trace1 = {
    "uid": "ed7f19ca-f978-11e8-b282-dd9f566f05e1", 
    "name": "Men", 
    "type": "bar", 
    "x": agegr, 
    "y": list1, 
    "marker": {"color": "rgb(0,138,184)"}
    }
    trace2 = {
    "uid": "ed7f19cb-f978-11e8-a521-dd9f566f05e1", 
    "name": "Women", 
    "type": "bar", 
    "x": agegr, 
    "y": list2,
    "marker": {"color": "rgb(204,102,153)"}
    }
    data = Data([trace1, trace2])
    layout = {
    "title": "Malaria Patients by Age and Gender", "title_x":0.5, 
    "barmode": "group"
    }
    fig = Figure(data=data, layout=layout)
    img_path = '/image/malaria.png'
    fig.write_image(os.path.curdir + '/static' + img_path)
    return  img_path

def get_pneumonia():
    counts = init_cnt()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.scan()

    for item in response['Items']:
        age = item['age']
        gender = item['gender']
        isPneuomonoa = item['isPneuomonoa']
        
        for age_group in age_groups:
            if age >= age_group[0] and age < age_group[1]:
                if isPneuomonoa > 0.5:
                    counts[gender][age_group] += 1
    dict1 = counts
    list1, list2 = get_lists(dict1)
    trace1 = {
    "uid": "ed7f19ca-f978-11e8-b282-dd9f566f05e1", 
    "name": "Men", 
    "type": "bar", 
    "x": agegr, 
    "y": list1, 
    "marker": {"color": "rgb(0,138,184)"}
    }
    trace2 = {
    "uid": "ed7f19cb-f978-11e8-a521-dd9f566f05e1", 
    "name": "Women", 
    "type": "bar", 
    "x": agegr, 
    "y": list2,
    "marker": {"color": "rgb(204,102,153)"}
    }
    data = Data([trace1, trace2])
    layout = {
    "title": "Pneumonia Patients by Age and Gender", "title_x":0.5, 
    "barmode": "group"
    }
    fig = Figure(data=data, layout=layout)

    img_path = '/image/pneumonia.png'
    fig.write_image(os.path.curdir + '/static' + img_path)
    return img_path

def get_depression():
    counts = init_cnt()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    # Scan the table and count Covid cases by gender and age group
    response = table.scan()

    for item in response['Items']:
        age = item['age']
        gender = item['gender']
        isDepression = item['isDepression']
        
        for age_group in age_groups:
            if age >= age_group[0] and age < age_group[1]:
                if isDepression ==1:
                    counts[gender][age_group] += 1
    dict1 = counts
    list1, list2 = get_lists(dict1)
    trace1 = {
    "uid": "ed7f19ca-f978-11e8-b282-dd9f566f05e1", 
    "name": "Men", 
    "type": "bar", 
    "x": agegr, 
    "y": list1, 
    "marker": {"color": "rgb(0,138,184)"}
    }
    trace2 = {
    "uid": "ed7f19cb-f978-11e8-a521-dd9f566f05e1", 
    "name": "Women", 
    "type": "bar", 
    "x": agegr, 
    "y": list2,
    "marker": {"color": "rgb(204,102,153)"}
    }
    data = Data([trace1, trace2])
    layout = {
    "title": "Depression Patients by Age and Gender", "title_x":0.5, 
    "barmode": "group"
    }
    fig = Figure(data=data, layout=layout)
    img_path = '/image/depression.png'
    fig.write_image(os.path.curdir + '/static' + img_path)
    return img_path

def get_covid():
    counts = init_cnt()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    # Scan the table and count Covid cases by gender and age group
    response = table.scan()

    for item in response['Items']:
        age = item['age']
        gender = item['gender']
        is_covid = item['isCovid']
        
        for age_group in age_groups:
            if age >= age_group[0] and age < age_group[1]:
                if is_covid > 0.5:
                    counts[gender][age_group] += 1
    dict1 = counts
    list1, list2 = get_lists(dict1)
    trace1 = {
    "uid": "ed7f19ca-f978-11e8-b282-dd9f566f05e1", 
    "name": "Men", 
    "type": "bar", 
    "x": agegr, 
    "y": list1, 
    "marker": {"color": "rgb(0,138,184)"}
    }
    trace2 = {
    "uid": "ed7f19cb-f978-11e8-a521-dd9f566f05e1", 
    "name": "Women", 
    "type": "bar", 
    "x": agegr, 
    "y": list2,
    "marker": {"color": "rgb(204,102,153)"}
    }
    data = Data([trace1, trace2])
    layout = {
    "title": "COVID Patients by Age and Gender", "title_x":0.5, 
    "barmode": "group"
    }
    fig = Figure(data=data, layout=layout)
    img_path = '/image/covid.png'
    fig.write_image(os.path.curdir + '/static' + img_path)
    return img_path

def get_diabetes():
    counts = init_cnt()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    # Scan the table and count Covid cases by gender and age group
    response = table.scan()

    for item in response['Items']:
        age = item['age']
        gender = item['gender']
        isDiabetes = item['isDiabetes']
        
        for age_group in age_groups:
            if age >= age_group[0] and age < age_group[1]:
                if isDiabetes > 0.5:
                    counts[gender][age_group] += 1
    dict1 = counts
    list1, list2 = get_lists(dict1)
    trace1 = {
    "uid": "ed7f19ca-f978-11e8-b282-dd9f566f05e1", 
    "name": "Men", 
    "type": "bar", 
    "x": agegr, 
    "y": list1, 
    "marker": {"color": "rgb(0,138,184)"}
    }
    trace2 = {
    "uid": "ed7f19cb-f978-11e8-a521-dd9f566f05e1", 
    "name": "Women", 
    "type": "bar", 
    "x": agegr, 
    "y": list2,
    "marker": {"color": "rgb(204,102,153)"}
    }
    data = Data([trace1, trace2])
    layout = {
    "title": "Diabetes Patients by Age and Gender", "title_x":0.5, 
    "barmode": "group"
    }
    fig = Figure(data=data, layout=layout)
    img_path = '/image/diabetes.png'
    fig.write_image(os.path.curdir + '/static' + img_path)
    return img_path

def get_heart_disease():
    counts = init_cnt()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    # Scan the table and count Covid cases by gender and age group
    response = table.scan()

    for item in response['Items']:
        age = item['age']
        gender = item['gender']
        isHeartDisease = item['isHeartDisease']
        
        for age_group in age_groups:
            if age >= age_group[0] and age < age_group[1]:
                if isHeartDisease ==1:
                    counts[gender][age_group] += 1
    dict1 = counts
    list1, list2 = get_lists(dict1)
    trace1 = {
    "uid": "ed7f19ca-f978-11e8-b282-dd9f566f05e1", 
    "name": "Men", 
    "type": "bar", 
    "x": agegr, 
    "y": list1, 
    "marker": {"color": "rgb(0,138,184)"}
    }
    trace2 = {
    "uid": "ed7f19cb-f978-11e8-a521-dd9f566f05e1", 
    "name": "Women", 
    "type": "bar", 
    "x": agegr, 
    "y": list2,
    "marker": {"color": "rgb(204,102,153)"}
    }
    data = Data([trace1, trace2])
    layout = {
    "title": "Heart Patients by Age and Gender", "title_x":0.5, 
    "barmode": "group"
    }
    fig = Figure(data=data, layout=layout)
    img_path = '/image/heart_disease.png'
    fig.write_image(os.path.curdir + '/static' + img_path)
    return img_path