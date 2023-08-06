from ..ext.hist import hist_tail
import os
import json

def get_command(n_lines: list):
    # TODO: propagate that last line in n_lines is the # of lines used
    # maybe add a check for 1 num to use default (20)
    df = hist_tail(n_lines[-1] * 2)
    exec_line = f"{df.iloc[-1]['Command']}"
    for cmd in n_lines[:-1]:
        exec_line += ' && '
        exec_line += f"{df.iloc[cmd].Command}"
        
    return exec_line
    
def run_command(n_lines: list):
    exec_line = get_command(n_lines)
    print(f"Running {exec_line[:-4]}")
    os.system(exec_line[:-4])

    
def save_command(n_lines: list):
    raise NotImplementedError('This function is not deprecated. Please use `dt hist -s`')
    
def list_snippets(ls_level: int):
    snippets_path = os.path.join(os.path.expanduser('~'), 'dt_config.json')
    config = json.loads(open(snippets_path).read())
    print(f"Snippets: {config['snippets']}")