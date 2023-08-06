#! /usr/bin/env python3
import argparse
import configparser
import os.path

from autopvs1_batch import rewrite_config, check_vep, run_snv_vep, run_cnv_vep

def prepare(hg19_fa:str, hg38_fa:str, vep_cache:str)->configparser.ConfigParser:
    config = rewrite_config(hg19_fa=hg19_fa, hg38_fa=hg38_fa, vep_cache=vep_cache)
    check_vep(config.get('DEFAULT', 'vep_cache'))
    return config

def autopvs1_snv(vcf:str, vep_cache:str, genome_version:str, outfile:str):
    snvs, vep_lines = run_snv_vep(vcf, vep_cache , args.genome_version)
    from autopvs1_batch.pvs1 import AutoPVS1
    fo = open(outfile, 'w')
    for snv in snvs:
        auto = AutoPVS1(snv=snv, vep_lines=vep_lines, genome_version=genome_version)
        if auto.islof:
            line = f'{snv.id}\t{auto.pvs1.criterion}\t{auto.pvs1.strength_raw}\t{auto.pvs1.strength}'
            fo.write(f'{line}\n')
    fo.close()

def autopvs1_cnv(bed:str, vep_cache:str, genome_version:str, outfile:str):
    cnvs, vep_lines = run_cnv_vep(bed, vep_cache , args.genome_version)
    from autopvs1_batch.pvs1 import AutoPVS1CNV
    fo = open(outfile, 'w')
    for cnv in cnvs:
        auto = AutoPVS1CNV(cnv=cnv, vep_lines=vep_lines, genome_version=genome_version)
        if auto.cnvtype:
            line = f'{cnv.id}\t{auto.pvs1.criterion}\t{auto.pvs1.strength_raw}\t{auto.pvs1.strength}'
            fo.write(f'{line}\n')
    fo.close()

def main(args):
    config = prepare(hg19_fa=args.hg19_fa, hg38_fa=args.hg38_fa, vep_cache=args.vep_cache)
    ext = os.path.splitext(args.input.lower())[-1]
    vep_cache = config.get('DEFAULT', 'vep_cache')
    if ext == '.vcf':
        autopvs1_snv(vcf=args.input, vep_cache=vep_cache, genome_version=args.genome_version, outfile=args.output)
    elif ext == '.bed':
        autopvs1_cnv(bed=args.input, vep_cache=vep_cache, genome_version=args.genome_version, outfile=args.output)
    else:
        raise Exception('ERROR: make sure your input is VCF for SNV or BED for CNV')
if __name__ == '__main__':
    parser = argparse.ArgumentParser('BAM View')
    parser.add_argument('--input', '-i', help='input file, VCF for SNV, BED for CNV')
    parser.add_argument('--output', '-o', help='output file')
    parser.add_argument('--hg19_fa', '-r', help='hg19 reference fasta file')
    parser.add_argument('--hg38_fa', '-R', help='hg38 reference fasta file')
    parser.add_argument('--vep_cache', '-d', help='vep cache directory')
    parser.add_argument('--genome_version', '-g', default='hg19', choices=('hg19', 'hg38'), help='genome version')
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(args)

