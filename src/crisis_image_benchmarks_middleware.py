import re
from dateutil.parser import parse

# Define a function to translate labels into concepts
def translate_labels(tweet: dict, labels: dict) -> list:
    '''
    This function is used to translate the labels (classification results of the 4 task) into  concepts.
    According to the labels, if there is no useful information, return an empty list.
    Else, translate the useful labels with another function: translate_useful_labels()
    '''
    if labels['informative']['label'] == 'not_informative' and labels['disaster_types']['label'] == 'not_disaster' and labels['humanitarian']['label'] == 'not_humanitarian':
        return []
    else:
        return translate_useful_labels(tweet, labels)

# Define a function to translate useful labels into concepts
def translate_useful_labels(tweet: dict, labels: dict) -> list:
    '''
    This function is used to translate the useful labels (classification results of the 4 task) into  concepts.
    '''
    concepts = []
    for concept in translate_disaster_types(tweet, labels):
        concepts.append(concept)
    for concept in translate_humanitarian(tweet, labels):
        concepts.append(concept)
    return concepts

# Define a function to translate the label from disaster types task into concepts
def translate_disaster_types(tweet: dict, labels: dict) -> list:
    if labels['disaster_types']['label'] == 'not_disaster':
        return []
    concepts = []
    locations = []
    if 'place_concerned' in tweet.keys():
        locations = tweet['place_concerned'].split('; ')
    if not locations:
        if labels['disaster_types']['label'] != 'other_disaster':
            concepts.append({
                'conceptType': 'potential',
                'potentialName': labels['disaster_types']['label'].capitalize(),
                'status': 'ACTIVE',
                'potentialType': 'Danger',
                'description': 'Image interpretation results from tweet.',
                'propertyLabels': [
                    'Place concerned: Unknown',
                    str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
                ]
            })
        else:
            concepts.append({
                'conceptType': 'potential',
                'potentialName': 'Unrecognized disaster',
                'status': 'ACTIVE',
                'potentialType': 'Danger',
                'description': 'Image interpretation results from tweet.',
                'propertyLabels': [
                    'Place concerned: Unknown',
                    str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
                ]
            })
    else:
        for location in locations:
            if labels['disaster_types']['label'] != 'other_disaster':
                concepts.append({
                    'conceptType': 'potential',
                    'potentialName': labels['disaster_types']['label'].capitalize() + ' in ' + location.replace("'", " "),
                    'status': 'ACTIVE',
                    'potentialType': 'Danger',
                    'description': 'Image interpretation results from tweet.',
                    'propertyLabels': [
                        'Place concerned: '+ location.replace("'", " "),
                        str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
                    ]
                })
            else:
                concepts.append({
                    'conceptType': 'potential',
                    'potentialName': 'Unrecognized disaster' + ' in ' + location.replace("'", " "),
                    'status': 'ACTIVE',
                    'potentialType': 'Danger',
                    'description': 'Image interpretation results from tweet.',
                    'propertyLabels': [
                        'Place concerned: '+ location.replace("'", " "),
                        str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
                    ]
                })
    return concepts

# Define a function to translate the label from humanitarian task into concepts
def translate_humanitarian(tweet: dict, labels: dict) -> list:
    if labels['humanitarian']['label'] == 'affected_injured_or_dead_people':
        return translate_affected_injured_or_dead_people(tweet, labels)
    elif labels['humanitarian']['label'] == 'rescue_volunteering_or_donation_effort':
        return translate_rescue_volunteering_or_donation_effort(tweet, labels)
    elif labels['humanitarian']['label'] == 'infrastructure_and_utility_damage':
        return translate_infrastructure_and_utility_damage(tweet, labels)
    else:
        return []

# Define a function to translate the label 'affected_injured_or_dead_people' into concepts:
def translate_affected_injured_or_dead_people(tweet: dict, labels: dict) -> list:
    concepts = []
    locations = []
    if 'place_concerned' in tweet.keys():
        locations = tweet['place_concerned'].split('; ')
    if not locations:
        concepts.append({
            'conceptType': 'actuality',
            'actualityName': 'People Affected, Injured, or Dead',
            'status': 'ACTIVE',
            'actualityType': 'Damage',
            'description': 'Image interpretation results from tweet.',
            'propertyLabels': [
                'Place concerned: Unknown',
                str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
            ]
        })
        concepts.append({
            'conceptType': 'person',
            'personName': 'Involved People',
            'status': 'ACTIVE',
            'description': 'Image interpretation results from tweet.',
            'propertyLabels': [
                'Place concerned: Unknown',
                str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
            ]
        })
    else:
        for location in locations:
            concepts.append({
                'conceptType': 'actuality',
                'actualityName': 'People Affected, Injured, or Dead' + ' in ' + location.replace("'", " "),
                'status': 'ACTIVE',
                'actualityType': 'Damage',
                'description': 'Image interpretation results from tweet.',
                'propertyLabels': [
                    'Place concerned: ' + location.replace("'", " "),
                    str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
                ]
            })
            concepts.append({
                'conceptType': 'person',
                'personName': 'Involved People' + ' in ' + location.replace("'", " "),
                'status': 'ACTIVE',
                'description': 'Image interpretation results from tweet.',
                'propertyLabels': [
                    'Place concerned: ' + location.replace("'", " "),
                    str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
                ]
            })
    return concepts

# Define a function to translate the label 'rescue_volunteering_or_donation_effort' into concepts:
def translate_rescue_volunteering_or_donation_effort(tweet: dict, labels: dict) -> list:
    concepts = []
    locations = []
    if 'place_concerned' in tweet.keys():
        locations = tweet['place_concerned'].split('; ')
    if not locations:
        concepts.append({
            'conceptType': 'potential',
            'potentialName': 'Rescue Volunteering or Donation Effort',
            'status': 'ACTIVE',
            'potentialType': 'Favorable Circumstance',
            'description': 'Image interpretation results from tweet.',
            'propertyLabels': [
                'Place concerned: Unknown',
                str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
            ]
        })
    else:
        for location in locations:
            concepts.append({
                'conceptType': 'potential',
                'potentialName': 'Rescue Volunteering or Donation Effort' + ' in ' + location.replace("'", " "),
                'status': 'ACTIVE',
                'potentialType': 'Favorable Circumstance',
                'description': 'Image interpretation results from tweet.',
                'propertyLabels': [
                    'Place concerned: ' + location.replace("'", " "),
                    str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
                ]
            })
    return concepts

# Define a function to translate the label 'infrastructure_and_utility_damage' into concepts:
def translate_infrastructure_and_utility_damage(tweet: dict, labels: dict) -> list:
    concepts = []
    locations = []
    if labels['disaster_types']['label'] != 'not_disaster' and labels['disaster_types']['label'] != 'other_disaster':
        typeString = ' Caused by ' +  labels['disaster_types']['label'].capitalize()
    else:
        typeString = ' Caused by Unrecognized Disaster'
    if 'place_concerned' in tweet.keys():
        locations = tweet['place_concerned'].split('; ')
    if not locations:
        concepts.append({
            'conceptType': 'good',
            'goodName': 'Involved Infrastructure and Utility',
            'status': 'ACTIVE',
            'description': 'Image interpretation results from tweet.',
            'propertyLabels': [
                'Place concerned: Unknown',
                str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
            ]
        })
        if labels['damage_severity'] == 'severe':
                concepts.append({
                    'conceptType': 'actuality',
                    'actualityName': 'Severe Damage' + typeString,
                    'status': 'ACTIVE',
                    'actualityType': 'Damage',
                    'description': 'Image interpretation results from tweet.',
                    'propertyLabels': [
                        'Place concerned: Unknown',
                        str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
                    ]
                })
        elif labels['damage_severity'] == 'mild':
            concepts.append({
                'conceptType': 'actuality',
                'actualityName': 'Mild Damage' + typeString,
                'status': 'ACTIVE',
                'actualityType': 'Damage',
                'description': 'Image interpretation results from tweet.',
                'propertyLabels': [
                    'Place concerned: Unknown',
                    str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
                ]
            })
        else:
            concepts.append({
                'conceptType': 'actuality',
                'actualityName': 'Little Damage' + typeString,
                'status': 'ACTIVE',
                'actualityType': 'Damage',
                'description': 'Image interpretation results from tweet.',
                'propertyLabels': [
                    'Place concerned: Unknown',
                    str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
                ]
            })
    else:
        for location in locations:
            concepts.append({
                'conceptType': 'good',
                'goodName': 'Involved Infrastructure and Utility' + ' in ' + location.replace("'", " "),
                'status': 'ACTIVE',
                'description': 'Image interpretation results from tweet.',
                'propertyLabels': [
                    'Place concerned: ' + location.replace("'", " "),
                    str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
                ]
            })
            if labels['damage_severity'] == 'severe':
                concepts.append({
                    'conceptType': 'actuality',
                    'actualityName': 'Severe Damage' + ' in ' + location.replace("'", " ") + typeString,
                    'status': 'ACTIVE',
                    'actualityType': 'Damage',
                    'description': 'Image interpretation results from tweet.',
                    'propertyLabels': [
                        'Place concerned: ' + location.replace("'", " "),
                        str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
                    ]
                })
            elif labels['damage_severity'] == 'mild':
                concepts.append({
                    'conceptType': 'actuality',
                    'actualityName': 'Mild Damage' + ' in ' + location.replace("'", " ") + typeString,
                    'status': 'ACTIVE',
                    'actualityType': 'Damage',
                    'description': 'Image interpretation results from tweet.',
                    'propertyLabels': [
                        'Place concerned: ' + location.replace("'", " "),
                        str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
                    ]
                })
            else:
                concepts.append({
                    'conceptType': 'actuality',
                    'actualityName': 'Little Damage' + ' in ' + location.replace("'", " ") + typeString,
                    'status': 'ACTIVE',
                    'actualityType': 'Damage',
                    'description': 'Image interpretation results from tweet.',
                    'propertyLabels': [
                        'Place concerned: ' + location.replace("'", " "),
                        str(parse(tweet['created_at'])) + ', ' + re.search(r'http.*$', tweet['full_text'])[0]
                    ]
                })
    return concepts