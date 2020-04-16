import pendulum

def query_entry(flashpack):
    """
    Query user to input flashpack information
    """
    print('Enter "n" to continue onto the next question\n')
    print('It is mandatory to have at least one response for questions marked *\n')
    
    front = ''
    while not front:
        front = input(f'Which word or phrase would you like to store in "{flashpack}"?*\n')
    
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


def query_list(message, min_length=-1, continue_char='n'):
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


def flash_from_data(data):
    """
    Randomly select a term from <data> and quiz on the flash
    Increment counters in data if chosen
    """
    pass