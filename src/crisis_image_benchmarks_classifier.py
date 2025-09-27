# Setup
import numpy as np
import torch
import torch.nn as nn
from torchvision import transforms
from efficientnet_pytorch import EfficientNet
from skimage import io
from PIL import Image


# Global constants
IMG_SIZE = 240
MODEL_DIR = '../resources/neural-networks/'
DEVICE = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
TRANSFORM = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.CenterCrop(IMG_SIZE),
    transforms.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])
])
# Set dictionary for different task
DIC = {
    0: {
        'name': 'informative',
        'short': 'info',
        'label_names': ['informative', 'not_informative'],
        'decoder': {
            0: 'informative',
            1: 'not_informative'
        }
    },
    1: {
        'name': 'disaster_types',
        'short': 'disaster_types',
        'label_names': ['earthquake', 'fire', 'flood', 'hurricane', 'landslide', 'not_disaster', 'other_disaster'],
        'decoder': {
            0: 'earthquake',
            1: 'fire',
            2: 'flood',
            3: 'hurricane',
            4: 'landslide',
            5: 'not_disaster',
            6: 'other_disaster'
        }
    },
    2: {
        'name': 'humanitarian',
        'short': 'hum',
        'label_names': ['affected_injured_or_dead_people', 'infrastructure_and_utility_damage', 'not_humanitarian', 'rescue_volunteering_or_donation_effort'],
        'decoder': {
            0: 'affected_injured_or_dead_people',
            1: 'infrastructure_and_utility_damage',
            2: 'not_humanitarian',
            3: 'rescue_volunteering_or_donation_effort'
        }
    },
    3: {
        'name': 'damage_severity',
        'short': 'damage',
        'label_names': ['little_or_none', 'mild', 'severe'],
        'decoder': {
            0: 'little_or_none',
            1: 'mild',
            2: 'severe'
        }
    }
}

# Definition of classes
# Define the class for pre-trained model using crisis image benchmarks dataset
class CrisisModel(nn.Module):
    def __init__(self, label_names):
        super().__init__()
        self.model = EfficientNet.from_pretrained('efficientnet-b1')
        self.model._fc = nn.Linear(self.model._fc.in_features, len(label_names))
        for param in self.parameters():
            param.require_grad = False

    def forward(self, xb):
        return self.model(xb)

    def freeze(self):
        for param in self.model.parameters():
            param.require_grad = False
    
    def unfreeze(self):
        for param in self.model.parameters():
            param.require_grad = True

    def __repr__(self):
        return f"{self.model}"
    
    def __str__(self):
        summary(self.model, (3, self.IS, self.IS))
        text_ = \
        f'''
            Model Name: {self.model_name}
            FC Layer input: {self.num_ftrs}
        '''
        return text_



# Definition of functions
# Define a function to load pre-trained model
def load_model(task) -> object:
    '''
    task = 0 -> informativeness
    task = 1 -> disaster types
    task = 2 -> humanitarian
    task = 3 -> damage severity
    '''
    model = CrisisModel(DIC[task]['label_names'])
    model_path = MODEL_DIR + DIC[task]['name'] + '.pth'
    if torch.cuda.is_available():
        model.load_state_dict(torch.load(model_path))
    else:
        model.load_state_dict(torch.load(model_path, map_location = torch.device('cpu')))
    model.freeze()
    return model.to(DEVICE)

# Define a function to load all pre-trained models
def load_models(verbose = False):
    info_model = load_model(0)
    info_model.eval()
    if verbose:
        print("Pre-trained informative classifier loaded")
        print('')
    type_model = load_model(1)
    type_model.eval()
    if verbose:
        print("Pre-trained disaster type classifier loaded")
        print('')
    hum_model = load_model(2)
    hum_model.eval()
    if verbose:
        print("Pre-trained humanitarian classifier loaded")
        print('')
    damage_model = load_model(3)
    damage_model.eval()
    if verbose:
        print("Pre-trained damage severity classifier loaded")
        print('')
    
    models = {
        'informative': info_model,
        'disaster_types': type_model,
        'humanitarian': hum_model,
        'damage_severity': damage_model
    }
    labels = {
        'informative': DIC[0]['label_names'],
        'disaster_types': DIC[1]['label_names'],
        'humanitarian': DIC[2]['label_names'],
        'damage_severity': DIC[3]['label_names']
    }
    decoders = {
        'informative': DIC[0]['decoder'],
        'disaster_types': DIC[1]['decoder'],
        'humanitarian': DIC[2]['decoder'],
        'damage_severity': DIC[3]['decoder']
    }
    result = {
        'models': models,
        'labels': labels,
        'decoders': decoders
    }
    return result

# Define a function to transform the image to meet the requirement of pretrained model
def transform_img(path, transform = TRANSFORM):
    '''
    path could be the local path or the url of the image
    '''
    #img = read_image(path, mode = ImageReadMode.RGB) / 255
    img = io.imread(path)
    img = np.array(Image.fromarray(img).convert('RGB')) / 255.0
    img = torch.tensor(np.moveaxis(img, -1, 0))
    img = img.type(dtype = torch.float32)
    img = transform(img)
    return img.to(DEVICE)

# Define a function to classify image into different labels
def classify_img(path, model, decoder, transform = TRANSFORM):
    img = transform_img(path, transform).unsqueeze(0)
    model.eval()
    prob = model(img)
    pred = decoder[np.argmax(prob.detach().cpu().numpy())]
    res = {
        'label': pred,
        'probability': nn.functional.softmax(prob, dim = 1).cpu().detach().numpy().max()
    }
    return res

# Define a function to classify image with the four classifiers
def cib_classify_img(path, pretrain, transform = TRANSFORM):
    img = transform_img(path, transform).unsqueeze(0)
    res = {
        'informative': classify_img(path, pretrain['models']['informative'], pretrain['decoders']['informative']),
        'disaster_types': classify_img(path, pretrain['models']['disaster_types'], pretrain['decoders']['disaster_types']),
        'humanitarian': classify_img(path, pretrain['models']['humanitarian'], pretrain['decoders']['humanitarian']),
        'damage_severity': classify_img(path, pretrain['models']['damage_severity'], pretrain['decoders']['damage_severity'])
    }
    return res