"""
Download deaf variation from http://deafnessvariationdatabase.org
"""

import requests
import json
import multiprocessing
import argparse
import os
import time


def download_genelist(filepath, verbose=False):
    url = 'http://deafnessvariationdatabase.org/api?&type=genelist&format=json'
    if verbose:
        print('Download genelist')
    res = requests.get(url)
    with open(filepath, 'w') as fh:
        json.dump(res.json(), fh)


def download_genefile(gene, outdir, retformat='tab', verbose=False):
    url = 'http://deafnessvariationdatabase.org/api?terms=%s&type=gene&format=%s' % (gene, retformat)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    if verbose:
        print('Request for %s' % url)
    start = time.time()
    res = requests.get(url)
    content = parse_content(res.text, retformat)
    if retformat == 'tab':
        outf = gene + '.tsv'
    elif retformat == 'json':
        outf = gene + '.json'
    elif retformat == 'xml':
        outf = gene + '.xml'
    else:
        outf = gene + '.txt'
    with open(os.path.join(outdir, outf), 'w') as fh:
        fh.write(content)
    end = time.time()
    if verbose:
        print('Request finished for %s, time %0.2f s' % (gene, end - start))


def parse_content(content, retformat):
    if retformat == 'tab' or retformat == 'csv':
        out = []
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            out.append(line)
        return '\n'.join(out)
    return content


def download_genes(genelist, outdir, refformat='tab', processes=3, verbose=False):
    if isinstance(genelist, str):
        with open(genelist) as fh:
            genelist = json.load(fh)
    pool = multiprocessing.Pool(processes=processes)
    for g in genelist:
        gene = g['gene']
        count = g['count']
        pool.apply_async(download_genefile, (gene, outdir, refformat, verbose))
    pool.close()
    pool.join()


def init_arguments(parser):
    """

    :param argparse.ArgumentParser parser:
    :return:
    """
    parser.add_argument('--genelist', help='Gene list file path (default genelist.json)', default='genelist.json')
    parser.add_argument('--output', help='Output dir (default data)', default='data')
    parser.add_argument('--format', help='Download file format (default tab)', default='tab')
    parser.add_argument('--processes', help='Number of processes (default 3)', default=3, type=int)
    parser.add_argument('-v', '--verbose', help='Show more information', action='store_true')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    init_arguments(parser)
    args = parser.parse_args()
    download_genelist(args.genelist, args.verbose)
    download_genes(args.genelist, args.output, args.format, args.processes, args.verbose)
