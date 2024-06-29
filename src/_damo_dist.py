# SPDX-License-Identifier: GPL-2.0

import os
import subprocess

'return error'
def plot_dist(data_file, output_file, xlabel, ylabel):
    terminal = output_file.split('.')[-1]
    if not terminal in ['pdf', 'jpeg', 'png', 'svg']:
        os.remove(data_file)
        return 'Unsupported plot output type.'

    gnuplot_cmd = """
    set term %s;
    set output '%s';
    set key off;
    set xlabel '%s';
    set ylabel '%s';
    plot '%s' with linespoints;""" % (terminal, output_file, xlabel, ylabel,
            data_file)
    subprocess.call(['gnuplot', '-e', gnuplot_cmd])
    os.remove(data_file)
    return None

def pr_dists(metric_name, dists, percentiles, pr_all, format_fn, raw_number,
             nr_cols_bar):
    '''
    Print distributed metric values for given percentiles or all
    '''
    print('# <percentile> <%s>' % metric_name)
    if len(dists) == 0:
        print('# no snapshot')
        return
    print('# avr:\t%s' % format_fn(sum(dists) / len(dists), raw_number))

    if pr_all:
        for idx, val in enumerate(dists):
            print('%s %s' % (idx, format_fn(val, raw_number)))
        return

    if nr_cols_bar > 0:
        max_val = 0
        for percentile in percentiles:
            val_idx = int(percentile / 100.0 * len(dists))
            if val_idx == len(dists):
                val_idx -= 1
            val = dists[val_idx]
            if max_val <= val:
                max_val = val
        if max_val > 0:
            val_per_col = max_val / nr_cols_bar
        else:
            val_per_col = 1

    for percentile in percentiles:
        idx = int(percentile / 100.0 * len(dists))
        if idx == len(dists):
            idx -= 1
        val = dists[idx]
        line = '%3d %15s' % (percentile, format_fn(val, raw_number))
        if nr_cols_bar > 0:
            cols = int(val / val_per_col)
            remaining_cols = nr_cols_bar - cols
            line += ' |%s%s|' % ('*' * cols, ' ' * remaining_cols)
        print(line)
