import copy
import itertools
import random

import pendulum
import numpy as np

def query_entry(flashpack):
    """
    Query user to input flashpack information
    """
    print('Enter nothing to continue onto the next question\n')
    print('It is mandatory to have at least one response for questions marked *\n')
    
    front = input(f'Which word or phrase would you like to store in "{flashpack}"?*\n')
    if not front:
        return None, None

    flashdata = []
    more = 'c'
    while not flashdata or more == 'c':
        datetime = pendulum.now().to_iso8601_string()

        flash = query_list(f'What should be flashed for "{front}"?*\n', min_length=0)
        tags = query_list('Any tags?\n')
        notes = query_list('Any notes?\n')

        print(f'Note: Siblings will only be stored if your input already exists in {flashpack}\n')
        siblings = query_list('Any siblings?\n')

        flashdata.append({
            'flash': flash,
            'datetime': datetime,
            'tags': tags,
            'times_flashed': 0,
            'times_correct': 0,
            'notes': notes,
            'siblings': siblings
        })

        more = input(f'Enter "c" to add more flash data for {front}')

    return front, flashdata


def add_entry(data, name, entry):
    """
    Add <entry> to <data> under <name>
    """
    if name in data:
        data[name].append(entry)
    else:
        data[name] = entry


def query_list(message, min_length=-1, continue_char=''):
    """
    Repeatedly query for <message> returning answers in list
    
    <min_length> is minimum legnth of list before returning,
        (-1 means no minimum)
    <continue_char> terminates querying
    """
    l = []
    while (continue_char not in l) or (len(l) <= min_length):
        l.append(input(message))

    # TODO: fix this
    # -1 is c always
    l.pop(-1)
    return l


def flash_from_data(data, tags=None):
    """
    Randomly select a term from <data> and quiz on the flash
    Increment counters in data if chosen

    tags: list
        filter data by tags in this list, if None, use all
    """
    total_correct = 0
    total_guessed = 0

    if tags:
        filt_data = filter_by_tags(data, tags)
    else:
        filt_data = data

    # TODO: Filter data by requirements...
    #data = filter_data(data)
    data_ls = list(data.items())
    success_metrics = [extract_success_metric(d) for w,d in data_ls]    
    sorted_data = [data_ls[i] for i in weighted_sort(success_metrics)]

    response = 'placeholder'
    for i,(k,v) in enumerate(sorted_data, 1):
        flash_mess = f'Flash #{i}'
        print(flash_mess)
        print('-'*len(flash_mess))
        response = input(k+'\n').lower()
        if not response:
            break
        flash = [w.lower() for f in v for w in f['flash']]
        correct = response in flash
        if correct:
            print('\ncorrect!')
            if len(flash) > 1:
                others = [x for x in flash if x != response]
                print('\nCould also have responded with...')
                for o in others:
                    print(o+' ')
                print('\n')
            for card in data[k]:
                card['times_correct'] += 1
            total_correct += 1
        else:
            print('\nIncorrect! Would have accepted...')
            for f in flash:
                print(f+' ')
            print('\n')
        for card in data[k]:
            card['times_flashed'] += 1
            card['last_interaction'] = pendulum.now().to_iso8601_string()
            total_guessed += 1
        # Add print of sentence, notes etc...
    
    if total_guessed == 0:
        print('Quitter!\n')
        return
    print('###################################')
    print('############# Results #############')
    print('###################################')
    success_perc = round(total_correct*100/total_guessed, 3)
    print(f'Score: {total_correct}/{total_guessed}, {success_perc}%\n')

    # TODO: change to randomly select from pool of messages
    if success_perc < 15:
        print('Awful\n')
    elif success_perc < 30:
        print('Could have done better mate\n')
    elif success_perc < 60:
        print('Not bad keep it up\n')
    elif success_perc < 80:
        print('Nice score!\n')
    elif success_perc < 100:
        print('Killing it!\n')
    elif success_perc == 100:
        print('Impeccable!\n')

def extract_success_metric(list_of_flash_dicts):
    """
    From a list of flash dictionaries extract success rate
    """
    return np.mean([d['times_flashed']/d['times_correct'] if d['times_correct'] else 0 for d in list_of_flash_dicts])


def filter_by_tags(data, tags):
    """
    Return dictionary of <data> including only entries with a tag in <tags>

    data: dict
    tags: list
    """
    new_dict = {}
    for name, flash in data.items():
        try:
            tags_lists = [f['tags'] for f in flash]
        except Exception as e:
            print(e)
            import ipdb; ipdb.set_trace()
        data_tags = list(itertools.chain.from_iterable(tags_lists))
        if set(data_tags).intersection(tags):
            new_dict[name] = flash
    return new_dict


def weighted_sort(l, factor=2, reverse=True, return_indices=True):
    """
    Sort <l>. The value of each element in <l> contributes to the probability that this element will be 
    near the top of the list.
    
    Param
    =====
    l: list
        list of values to sort
    factor: int
        Higher factor means higher contribution to the probability, factor of 0 is random sort
    reverse: bool
        If True, higher list values mean lower probability of being at the top
        and vice versa
    return_indices: bool
        if False, return original list sorted, if True return indices 
    
    Return
    ======
    list of length == len(l)
    """
    weights_copy = copy.copy(l)
    n = len(weights_copy)

    if return_indices:
        all_indices = list(range(n))

    chosen = []
    for i in range(n):
        indices = list(range(len(weights_copy)))

        # correction for 0s
        weights_trans = [x**factor+0.0001 for x in weights_copy]
        weights_sum = sum(weights_trans)
        probs = [x/weights_sum for x in weights_trans]
        
        choice = np.random.choice(indices, size=1, replace=False, p=probs)[0]
        
        if return_indices:
            weights_copy.pop(choice)
            chosen.append(all_indices.pop(choice))
        else:
            chosen.append(weights_copy.pop(choice))

    if reverse:
        chosen.reverse()

    return chosen
