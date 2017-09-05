"""
Transform tsv file to json.
"""
import os
import json
import argparse


def tsv2json(filepath, outdir):
    print('Transform file %s' % filepath)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    with open(filepath) as fh:
        head = None
        data = []
        for line in fh:
            line = line.strip()
            if not line:
                continue
            # get head
            if head is None:
                head = line.strip('#').split('\t')
                continue
            # parse line
            d = {}
            cols = line.split('\t')
            for i in range(len(head)):
                v = cols[i].strip()
                if v == '' or v == 'NULL':
                    v = None
                d[head[i]] = v
            data.append(d)
    fname = os.path.basename(filepath)
    dot = fname.find('.')
    if dot > 0:
        fname = fname[:dot]
    outf = os.path.join(outdir, fname + '.json')
    with open(outf, 'w') as fh:
        json.dump(data, fh)


def transform_dir(directory, outdir):
    for rt, dirs, files in os.walk(directory):
        for fs in files:
            tsv2json(os.path.realpath(os.path.join(rt, fs)), outdir)


def transform(files, outdir):
    for f in files:
        if os.path.isdir(f):
            transform_dir(f, outdir)
        else:
            tsv2json(f, outdir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help='File or directory to transform.')
    parser.add_argument('-o', '--output', help='Output directory (default out)', default='out')
    args = parser.parse_args()
    transform(args.files, args.output)
