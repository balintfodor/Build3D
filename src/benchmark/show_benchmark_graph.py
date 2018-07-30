from subprocess import Popen, PIPE
import sys
import pandas as pd
import platform
from bokeh.plotting import figure, output_file, show, gridplot
from bokeh.palettes import d3
import itertools
import os.path

PERF_CSV_FILENAME = 'perf.csv'


def git_branch():
    git_proc = Popen(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=PIPE)
    (br, err) = git_proc.communicate()
    exit_code = git_proc.wait()
    if exit_code != 0:
        print('can not determine current git branch')
        sys.exit(1)
    return br.decode('ascii').rstrip()


def contains_any_keyword(text, keywords_list):
    return any([k in text for k in keywords_list])


def remove_hash_tags(text):
    return ' '.join(filter(lambda x: x[0] != '#', text.split()))


# get filtering keywords
keywords = sys.argv[1:]
print('keywords: {}'.format(' '.join(keywords)))

if not os.path.isfile(PERF_CSV_FILENAME):
    print(('\'{}\' does not exist, can not create graph,\n'
           'run collect_benchmark_info.py to generate \'{}\'')
          .format(PERF_CSV_FILENAME, PERF_CSV_FILENAME))
    sys.exit(2)

branch = git_branch()
print('git branch = {}\nplatform = {}'.format(branch, platform.platform()))

dt = pd.read_csv(PERF_CSV_FILENAME, delimiter=';')

current_dt = dt[(dt['git_branch'] == branch) &
                (dt['platform'] == platform.platform())]

output_file('benchmark.html')
p = figure(title='benchmark on branch \'{}\' and platform \'{}\''
           .format(branch, platform.platform()),
           x_axis_label='timestamp',
           y_axis_label='ns/op')

colors = itertools.cycle(d3['Category20'][20])

t_index = {ts: i
           for i, ts in enumerate(sorted(current_dt['timestamp'].unique()))}

unq_names = current_dt['name'].unique()

if len(keywords) > 0:
    unq_names = [name for name in unq_names
                 if contains_any_keyword(name, keywords)]

unq_names = [remove_hash_tags(name) for name in unq_names]

# canonic names
current_dt['name'] = current_dt['name'].apply(remove_hash_tags)

for bm, c in zip(unq_names, colors):
    bm_dt = current_dt[current_dt['name'] == bm]
    x = [t_index[ts] for ts in bm_dt['timestamp'].values]
    y = bm_dt['runtime'].values
    p.line(x, y, legend=bm, color=c)
    p.circle(x, y, legend=bm, color=c, size=6)

fig = gridplot([[p]], sizing_mode='stretch_both', merge_tools=False)
show(fig)