import re
from collections import namedtuple

CNV = namedtuple('SNV', ['chrom', 'start', 'end', 'type', 'id'])

def read_bed(bed:str) -> list:
    cnvs = list()
    fi = open(bed)
    for line in fi:
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        fields = line.split('\t')
        chrom, start, end, typo = fields[0:4]
        chrom = chrom.replace('chr', '')
        if chrom[0] == "M": chrom = "MT"
        cnvs.append(CNV(chrom=chrom, start=int(start), end=int(end), type=typo, id=f'{chrom}:{start}:{end}:{typo}'))
    fi.close()
    return cnvs

def write_bed(cnvs:list, out_bed:str):
    fo = open(out_bed, 'w')
    for cnv in cnvs:
        fo.write(f'{cnv.chrom}\t{cnv.start}\t{cnv.end}\t{cnv.type}\n')
    fo.close()