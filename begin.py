%load_ext autoreload

%autoreload 2

example = {
    'ingenuo':[{
        'flash': ['naive'],
        'date': '2020-04-16',
        'time': '18:23:59',
        'tags': ['adjective', 'masculine'],
        'times_flashed': 0,
        'times_correct': 0,
        'notes': ['No soy ingenuo'],
        'siblings': []
    }],
    'raya':[{
        'flash': ['line', 'stripe'],
        'date': '2020-04-16',
        'time': '18:29:24',
        'tags': ['noun', 'feminine'],
        'times_flashed': 0,
        'times_correct': 0,
        'notes': ['Un vestido con rayas', 'Conecta los puntos con rayas'],
        'siblings': []
    },
    {
        'flash': ['line of drugs'],
        'date': '2020-04-16',
        'time': '18:29:24',
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
