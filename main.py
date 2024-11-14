import main_cy
import requests
import json 
import os
import time 
# import access_neo4j as neo4j
# neo4j.verify_connection()
print("hay")
def clear():
       os.system('cls') if os.name == 'nt' else os.system('clear')
token_endpoint = 'https://icdaccessmanagement.who.int/connect/token'


client_id = '2369713b-a065-46ed-b75d-66d4e0036f63_86fa9505-8625-4483-91bf-daa538f0af32'

client_secret = 'vTulKBpN1gwKsC0D5Edo1917zLBqJ1HwzOx/xJXZ0ko='

scope = 'icdapi_access'

grant_type = 'client_credentials'

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# set data to post
payload = {'client_id': client_id, 
	    'client_secret': client_secret, 
           'scope': scope, 
           'grant_type': grant_type}
           
# make request

r = requests.post(token_endpoint, data=payload, verify=False).json()
token = r['access_token']


# access ICD API

first_entity = 'http://id.who.int/icd/entity/455013390'

# HTTP header fields to set
headers = {'Authorization':  'Bearer '+token, 
           'Accept': 'application/json', 
           'Accept-Language': 'en',
	    'API-Version': 'v2'}         
# make request           



#Load data from files
with open('already_present_relationships.txt', 'r') as f:
    already_present_relationships = [x.strip() for x in f.readlines()]

f.close()

with open('urls_to_be_processed.txt', 'r') as f:
    urls_to_be_processed = [i.strip() for i in f.readlines()]
f.close()
with open('processed_urls.txt', 'r') as f:
    processed_urls = [i.strip() for i in f.readlines()]
f.close()
# Convert lists to sets for faster lookups






while len(urls_to_be_processed)>0:
       st_time=time.time()
       #get url of the entity to be explored from the url list 
       
       entity_url=urls_to_be_processed[0]

       #get the full data of the entity 
       entity_data=requests.get(entity_url, headers=headers, verify=False).json()
       
       #get the title of the entity
       entity_title=entity_data['title']["@value"]
       
       # check the relationship file if there's a relationship containing the entity url, if yes, update the relationship to contain the entity title instead of entity url
       for relationship in already_present_relationships:
              if entity_url in relationship:
                     updated_relationship=relationship.replace(entity_url, entity_title)
                     already_present_relationships.remove(relationship)
                     already_present_relationships.append(updated_relationship)
       
       #check if the entity has any children urls, and if so , add a "--->" relationship between the entity title and each one of the childern url to the already present relationship and then add those urls to the url list to be processed if not already there or in the processed urls
       for i in entity_data:
              if i =='child':
                     entity_childern_urls= entity_data[i]
                     for url in entity_childern_urls:
                            already_present_relationships.append(entity_title+"--->"+url)
                            if url not in processed_urls:
                                   urls_to_be_processed.append(url)
       #to complete the process, save the changes you made in txt files so thay can be re-used in the next process
       with open('already_present_relationships.txt', 'w') as f:
              for i in set(already_present_relationships):
                     f.write(i+'\n')
       f.close()
       # now that you have the data of the entity, you can say that you have completely processed the entity url, so you can remove it from the url list to be processed and add it to the processed urls, and don't forget to save the changes you made to these two lists in txt files so thay can be re-used in the next process
       urls_to_be_processed.remove(entity_url)
       with open('urls_to_be_processed.txt', 'w') as f:
              for i in set(urls_to_be_processed):
                     f.write(i+'\n')
       f.close()
       
       processed_urls.append(entity_url)
       with open('processed_urls.txt', 'w') as f:
              for i in set(processed_urls):
                     f.write(i+'\n')
       f.close()
       #get some statistical information about the progress
       
       old_parameters=open('parameters.txt', 'r').readlines()
       old_parameters=[float(i.strip()) for i in old_parameters]

       precentage=(len(processed_urls)/(len(urls_to_be_processed)+len(processed_urls)))*100
       precentage=round(precentage, 2)
       
       
       titled_relationship= [i for i in already_present_relationships if 'http' not in i]

       en_time=time.time()
       time_elapse=en_time-st_time
       time_left=time_elapse*len(urls_to_be_processed)
       time_left_det=time.gmtime(time_left)
       
       new_parameters=[precentage, len(urls_to_be_processed) ,len(already_present_relationships) , len(titled_relationship),time_left]

       parameter_ratio=[]
       for i in range(len(new_parameters)):
              if new_parameters[i]>old_parameters[i]:
                     parameter_ratio.append("▲")
              elif new_parameters[i]==old_parameters[i]:
                     parameter_ratio.append("🔹")
              else:
                     parameter_ratio.append("🔻")

       with open('parameters.txt','w') as f:
              for i in new_parameters:
                     f.write(str(i)+"\n")
       #print the number of process and the number of saved relationships and the number of urls to be processed an the number untitled relationships
       clear()
       print(f'''
             TIME LEFT: {time_left_det.tm_hour}h {time_left_det.tm_min}m {time_left_det.tm_sec}s {parameter_ratio[-1]} ({round(1/time_elapse,2)} p/s)
       
       
       Processes completed: {format(len(processed_urls), ",d")}
       
       Precentage of processed data: {precentage} % {parameter_ratio[0]} 

       Unprocessed data: {format(len(urls_to_be_processed),',d')} {parameter_ratio[1]}  {new_parameters[1]-old_parameters[1]}
       
       Saved relationships: {format(len(already_present_relationships),',d')} {parameter_ratio[2]}  {new_parameters[2]-old_parameters[2]}
       
       Titled relationship: {format(len(titled_relationship),',d')}  {parameter_ratio[3]}  ({round((len(titled_relationship)/len(already_present_relationships))*100, 2)} % )
       ''')
       
       
       
print('FINISHED')

