from .parse_tree import ParseTree


command = input('?> ')
while command not in ('', 'exit', 'quit'):
    tokens = command.split(' ')
    key = tokens[0]
    expression = ' '.join(tokens[1:])
    t = ParseTree()
    t.read(expression)
    if key in {'eval', 'evaluate', 'calc', 'calculate'}:
        print(expression, '=', t.evaluate())
    elif key in {'show', 'display',  'vis', 'viz', 'visualise', 'visualize'}:
        print()
        print(str(t))
    else:
        raise ValueError(f'Unknown command {key} encountered')
    command = input('?> ')
print('Bye :)')