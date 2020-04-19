%load_ext autoreload

%autoreload 2

example = {
    'ingenuo':[{
        'flash': ['naive'],
        'datetime': '2020-04-16T19:16:29.574854+02:00',
        'tags': ['adjective', 'masculine'],
        'times_flashed': 0,
        'times_correct': 0,
        'notes': ['No soy ingenuo'],
        'siblings': []
    }],
    'raya':[{
        'flash': ['line', 'stripe'],
        'datetime': '2020-04-16T19:19:29.574854+02:00',
        'tags': ['noun', 'feminine'],
        'times_flashed': 0,
        'times_correct': 0,
        'notes': ['Un vestido con rayas', 'Conecta los puntos con rayas'],
        'siblings': []
    },
    {
        'flash': ['line of drugs'],
        'datetime': '2020-04-16T19:21:29.574854+02:00',
        'tags': ['noun', 'feminine', 'slang'],
        'times_flashed': 0,
        'times_correct': 0,
        'notes': ['Prepara una raya de cocaína!'],
        'siblings': []
    }]
}

from battyflash.utils import store_json, load_json

store_json(example, 'data')
data = load_json('data')

data == example



######################################
####### SKELETON PROGRAMME ###########
######################################

## 1. Which project to work on?
###############################
import os
from battyflash.utils import store_json, load_json

flashpack = input('Which Flashpack would you like to use?\n')
flashdir = os.path.join('/Users/tom/.battyflash/data', flashpack)
data = load_json(flashdir)
if not data:
    print('Flashpack does not exist, creating new Flashpack')

## 2. Building dataset
######################
from battyflash.packs import query_entry, add_entry, flash_from_data

# TODO: Better word than "entry"
print('Lets begin by adding an entry')

while True:
    name, entry = query_entry(flashpack)
    if not name:
        break
    add_entry(data, name, entry)

store_json(data, flashdir)


## 3. Quizzing
##############
import os

flashpack = input('Which Flashpack would you like to use?\n')
flashdir = os.path.join('/Users/tom/.battyflash/data', flashpack)
data = load_json(flashdir)

print('For each item, respond with the flash, to exit, return nothing\n')
flash_from_data(data)

store_json(data, flashdir)

## 3. Report Performance
########################

# performance(data)








