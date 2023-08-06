import os
import numpy as np
import requests
import pandas as pd

def search_events(category):
    
    '''
    This function allows users to conduct a search to pull information about natural events from the EONET API
    
    Inputs
    ------
    
    category = a search term of event category input by user
    
    Outputs
    -------
    Dataframe containing all events that match the search query
    
    Example
    -------
    search_events("wildfires")
    Returns a dataframe that contains all natural events related to wildfires
    '''
    import requests
    import json
    import pandas as pd
    

    url = ("https://eonet.gsfc.nasa.gov/api/v3/events?category=" + str(category))
    r = requests.get(url)
    r_data = r.json()
    
    if r.status_code == 200:
        events = r_data['events']
        event_data = []

        for event in events:
                id=event['id']
                title=event['title']
                type_id = event['categories'][0]['id']
                type_title = event['categories'][0]['title']
                coords=event['geometry'][0]['coordinates']
                geo_type =  event['geometry'][0]['type']
                date=event['geometry'][0]['date']


                event_dict = {
                    'id': id,
                    'title':title,
                    'type_id': type_id,
                    'type_title': type_title,
                    'date' : date,
                    'coords': coords,
                    'geo_type': geo_type,  
                }
                event_data.append(event_dict)
        df = pd.DataFrame(event_data)
        display(df)
    else:
        return r.status_code


