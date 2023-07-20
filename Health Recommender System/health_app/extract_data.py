import boto3
import os
import urllib.request as req

# create a boto3 client for DynamoDB
dynamodb = boto3.client('dynamodb')

# define the table name
table_name = 'adbmsla2'

def get_record(id):
    filter_expression = 'id = :ID'
    expression_attribute_values = {':ID': {'N': str(id)}}
    response = dynamodb.scan(
        TableName=table_name,
        FilterExpression=filter_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    datalist = response['Items']
    temp=dict()
    out = list()
    for ele in datalist:
        temp.clear()
        for key,inner_dict in ele.items():
            n_val = float(inner_dict.get('N',0.0))
            s_val = str(inner_dict.get('S',''))
            if s_val == '':
                temp[key] = n_val
            else:
                temp[key] = s_val
        out.append(dict(temp))
    mimg = req.urlretrieve(out[0]['malariadata'],str(out[0]['malariadata'].split('/')[-1]))[0]
    cimg = req.urlretrieve(out[0]['coviddata'],str(out[0]['coviddata'].split('/')[-1]))[0]
    mcsv = req.urlretrieve(out[0]['mentalhealthdata'],str(out[0]['mentalhealthdata'].split('/')[-1]))[0]
    out[0]['malariadata'] = mimg
    out[0]['coviddata'] = cimg
    out[0]['mentalhealthdata'] = mcsv

    p = os.path.curdir+'/download/'
    org_path = mimg
    target_path = p+'malaria/'+mimg
    os.rename(org_path,target_path)
    org_path = cimg
    target_path = p+'covid/'+cimg
    os.rename(org_path,target_path)
    org_path = mcsv
    target_path = p+'mentalhealth/'+mcsv
    os.rename(org_path,target_path)

    if out[0]['gender'] == 0:
        out[0]['gender'] = 'M'
    else:
        out[0]['gender'] = 'F'
    return out[0] 

def get_final_data(dlist):
    final_dlist = list()
    temp = dict()
    cfilter = ('id','insulin','cholestrol','bp','gender','age','glucose','more')
    for ele in dlist:
        temp.clear()
        for key,inner_dict in ele.items():
            n_val = float(inner_dict.get('N',0.0))
            s_val = str(inner_dict.get('S',''))
            if s_val == '':
                temp[key] = n_val
            else:
                temp[key] = s_val
        temp['more'] = float(temp['id'])

        final_dlist.append(dict((k,temp[k]) for k in cfilter if k in temp ))
    final_clist = []
    final_clist.append({'key': 'id', 'label': 'ID'})
    final_clist.append({'key': 'insulin', 'label': 'Insulin'})
    final_clist.append({'key': 'cholestrol', 'label': 'Cholestrol'})
    final_clist.append({'key': 'bp', 'label': 'BP'})
    final_clist.append({'key': 'gender', 'label': 'Gender'})
    final_clist.append({'key': 'age', 'label': 'Age'})
    final_clist.append({'key': 'glucose', 'label': 'Glucose'})
    final_clist.append({'key': 'more', 'label': 'More'})
    temp['more'] = str(temp['id'])
    return final_dlist, final_clist

def get_diabetes_data():
    #get number of people having diabetes
    filter_expression = 'isDiabetes > :isDiabetes'
    # define the attribute values to be substituted in the filter expression
    expression_attribute_values = {
        ':isDiabetes': {'N': '0.5'}
    }

    response = dynamodb.scan(
    TableName=table_name,
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values
    )
    dlist=response['Items']
    return get_final_data(dlist)

def get_pneumonia_data():
    #get number of people having pneuomonia
    filter_expression = 'isPneuomonoa > :isPneuomonoa'
    # define the attribute values to be substituted in the filter expression
    expression_attribute_values = {
        ':isPneuomonoa': {'N': '0.5'}
    }
    response = dynamodb.scan(
        TableName=table_name,
        FilterExpression=filter_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    plist=response['Items']
    return get_final_data(plist)

def get_depression_data():
    #get number of people having depression
    filter_expression = 'isDepression = :isDepression'
    # define the attribute values to be substituted in the filter expression
    expression_attribute_values = {
        ':isDepression': {'N': '1'}
    }
    response = dynamodb.scan(
        TableName=table_name,
        FilterExpression=filter_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    dplist=response['Items']
    return get_final_data(dplist)

def get_covid_data():
    #get number of people having covid
    filter_expression = 'isCovid > :isCovid'
    # define the attribute values to be substituted in the filter expression
    expression_attribute_values = {
        ':isCovid': {'N': '0.5'}
    }
    response = dynamodb.scan(
        TableName=table_name,
        FilterExpression=filter_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    clist=response['Items']
    return get_final_data(clist)

def get_malaria_data():
    #get number of people having malaria
    filter_expression = 'isMalaria > :isMalaria'
    # define the attribute values to be substituted in the filter expression
    expression_attribute_values = {
        ':isMalaria': {'N': '0.5'}
    }
    response = dynamodb.scan(
        TableName=table_name,
        FilterExpression=filter_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    mlist=response['Items']
    return get_final_data(mlist)

def get_heart_disease_data():
    #get number of people having heartdisease
    filter_expression = 'isHeartDisease = :isHeartDisease'
    # define the attribute values to be substituted in the filter expression
    expression_attribute_values = {
        ':isHeartDisease': {'N': '1'}
    }
    response = dynamodb.scan(
    TableName=table_name,
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values
    )
    hlist=response['Items']
    return get_final_data(hlist)