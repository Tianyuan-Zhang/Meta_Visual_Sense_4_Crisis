import json
from dateutil.parser import parse
from skimage import io
import os
import sys

import rioda_python_driver as riopy
import crisis_image_benchmarks_classifier as cibClassifier
import crisis_image_benchmarks_middleware as cibMiddleware

DATASET = {
    '2018 Aude Flood': {
        'dataset type': 'json',
        'json path': '../resources/twitter-datasets/2018-aude-flood/2018-aude-flood-tweets.json',
        'images folder': '../resources/twitter-datasets/2018-aude-flood/2018-aude-flood-images/'
    },
    '2018 Aude Flood from Diego Kozlowski': {
        'dataset type': 'json',
        'json path': '../resources/twitter-datasets/2018-aude-flood/2018-aude-flood-tweets-from-diego-kozlowski.json',
        'images folder': '../resources/twitter-datasets/2018-aude-flood/2018-aude-flood-images-from-diego-kozlowski/'
    }
}

# define a function to parse the time stamp of a tweet
def get_time_stamp(tweet: dict):
    return parse(tweet['created_at'])

# define a function to load twitter dataset from .json
def load_tweets_from_json(path = None, dataset = None) -> list:
    '''
    dataset: pre-defined dataset, chosen from the following options:
        '2018 Aude Flood'
        '2018 Aude Flood from Diego Kozlowski'
    '''
    tweets = []
    if dataset:
        jsonPath = DATASET[dataset]['json path']
    elif path:
        jsonPath = path
    else:
        return tweets
    for line in open(jsonPath, 'r'):
        tweets.append(json.loads(line))
    tweets.sort(key = get_time_stamp)
    return tweets

# Define a function to fetch images from single tweet
def fetch_imgs(tweet, online = True, folderPath = None, dataset = None):
    '''
    dataset: pre-defined dataset, chosen from the following options:
        '2018 Aude Flood'
        '2018 Aude Flood from Diego Kozlowski'
    '''
    imgs = []
    medias_json = json.dumps(tweet['extended_entities']['media'])
    medias_dict = json.loads(medias_json)
    media_count = len(medias_dict)
    img_urls = []
    for i in range(media_count):
        media_dict = medias_dict[i]
        if media_dict["type"] == 'photo':
            img_urls.append(media_dict["media_url"])
    img_count = len(img_urls)
    
    if online:
        for i in range(img_count):
            try:
                img = io.imread(img_urls[i])
                imgs.append(img)
            except:
                continue
    else:
        if dataset:
            imageFolder = DATASET[dataset]['images folder']
        else:
            imageFolder = folderPath
        for i in range(img_count):
            try:
                img = io.imread(imageFolder + tweet['id_str'] + "_" + str(i + 1) + ".jpg")
            except:
                try:
                    img = io.imread(imageFolder + tweet['id_str'] + "_" + str(i + 1) + ".png")
                except:
                    continue
            imgs.append(img)
    return imgs

# Define a function to fetch images' paths from single tweet
def fetch_imgs_paths(tweet, online = True, folderPath = None, dataset = None):
    '''
    dataset: pre-defined dataset, chosen from the following options:
        '2018 Aude Flood'
        '2018 Aude Flood from Diego Kozlowski'
    '''
    paths = []
    medias_json = json.dumps(tweet['extended_entities']['media'])
    medias_dict = json.loads(medias_json)
    media_count = len(medias_dict)
    img_urls = []
    for i in range(media_count):
        media_dict = medias_dict[i]
        if media_dict["type"] == 'photo':
            img_urls.append(media_dict["media_url"])
    img_count = len(img_urls)
    
    if online:
        return img_urls
    else:
        if dataset:
            imageFolder = DATASET[dataset]['images folder']
        else:
            imageFolder = folderPath
        for i in range(img_count):
            jpgPath = imageFolder + tweet['id_str'] + "_" + str(i + 1) + ".jpg"
            pngPath = imageFolder + tweet['id_str'] + "_" + str(i + 1) + ".png"
            if os.path.isfile(jpgPath):
                paths.append(os.path.abspath(jpgPath))
            elif os.path.isfile(pngPath):
                paths.append(os.path.abspath(pngPath))
    return paths

# Define a function to classify a single tweet if images exist with cib classifier
def cib_classify_tweet(tweet: dict, pretrain, online = True, folderPath = None, dataset = None):
    '''
    dataset: pre-defined dataset, chosen from the following options:
        '2018 Aude Flood'
        '2018 Aude Flood from Diego Kozlowski'
    '''
    results = []
    paths = fetch_imgs_paths(tweet, online, folderPath, dataset)
    for path in paths:
        results.append(cibClassifier.cib_classify_img(path, pretrain))
    return results

# Define a function to translate the classification results of a single tweet with cib middleware
def cib_translate_tweet(tweet: dict, classifyResults):
    concepts = []
    for result in classifyResults:
        for concept in cibMiddleware.translate_labels(tweet, result):
            concepts.append(concept)
    return concepts

# Define a end-to-end function to interpret a single tweet and instantiate concepts with cib tasks
def cib_interpret_tweet(
    tx,
    currentKnowledgeSpaceName,
    currentCollaborationName,
    tweet: dict,
    pretrain,
    online = True,
    folderPath = None,
    dataset = None,
    verbose = False
):
    '''
    dataset: pre-defined dataset, chosen from the following options:
        '2018 Aude Flood'
        '2018 Aude Flood from Diego Kozlowski'
    '''
    cibLabels = cib_classify_tweet(tweet, pretrain, online, folderPath, dataset)
    cibConcepts = cib_translate_tweet(tweet, cibLabels)
    for concept in cibConcepts:
        riopy.instantiate_concept(tx, concept, currentKnowledgeSpaceName, currentCollaborationName, verbose)