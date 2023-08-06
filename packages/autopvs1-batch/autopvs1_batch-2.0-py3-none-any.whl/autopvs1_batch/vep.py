import os
import re

from .utils import id_generator
from .vcf import read_vcf, write_vcf
from .bed import read_bed, write_bed


def get_vep_assembly(genome_version: str) -> str:
    if genome_version == 'hg19':
        return 'GRCh37'
    if genome_version == 'hg38':
        return 'GRCh38'
    raise ValueError("Genome version must be hg19/GRCh37 or hg38/GRCh38.")

def filter_vep(variant_id:str, vep_lines:list, vep_output:str):
    fo = open(vep_output, 'w')
    for line in vep_lines:
        if line.startswith('#') or line.split('\t')[0] == variant_id:
            fo.write(line)
    fo.close()

def run_snv_vep(vcf:str, vep_cache:str, genome_version: str) -> [list, str, dict]:
    vep_assembly= get_vep_assembly(genome_version)
    vep_input =  f'/tmp/vep_{id_generator()}.vcf'
    vep_output = f'/tmp/vep_{id_generator()}.tab'
    snvs = read_vcf(vcf)
    write_vcf(snvs, vep_input)
    vep_cmd = f'vep --offline --refseq --use_given_ref ' \
              f'--dir_cache {vep_cache} ' \
              f'--species "homo_sapiens" ' \
              f'--assembly {vep_assembly} ' \
              f'--fork 4 ' \
              f'--canonical ' \
              f'--flag_pick ' \
              f'--hgvs --hgvsg --symbol ' \
              f'--distance 500 ' \
              f'--exclude_predicted ' \
              f'--lookup_ref ' \
              f'--force ' \
              f'--no_stats ' \
              f'--numbers ' \
              f'--input_file {vep_input} ' \
              f'--output_file {vep_output} ' \
              f'--tab --fields "Uploaded_variation,SYMBOL,Feature,CANONICAL,PICK,Consequence,HGVSc,HGVSp,HGVSg,EXON,INTRON"'
    if os.system(vep_cmd) != 0:
        raise Exception(f'Error: run vep fail with: {vep_cmd}')
    lines = open(vep_output).readlines()
    os.remove(vep_input)
    os.remove(vep_output)
    return snvs, lines


def run_cnv_vep(bed:str, vep_cache:str, genome_version: str) -> [list, str, dict]:
    vep_assembly= get_vep_assembly(genome_version)
    vep_input =  f'/tmp/vep_{id_generator()}.bed'
    vep_output = f'/tmp/vep_{id_generator()}.tab'
    cnvs = read_bed(bed)
    write_bed(cnvs, vep_input)
    vep_cmd = f'vep --offline --refseq --use_given_ref ' \
              f'--dir_cache {vep_cache} ' \
              f'--species "homo_sapiens" ' \
              f'--assembly {vep_assembly} ' \
              f'--fork 1 ' \
              f'--hgvs --hgvsg --canonical --symbol ' \
              f'--distance 0 ' \
              f'--exclude_predicted ' \
              f'--flag_pick ' \
              f'--lookup_ref ' \
              f'--force ' \
              f'--no_stats ' \
              f'--numbers ' \
              f'--input_file {vep_input} ' \
              f'--output_file {vep_output} ' \
              f'--tab --fields "Uploaded_variation,SYMBOL,Feature,CANONICAL,PICK,EXON,INTRON,Consequence,CDS_position"'
    if os.system(vep_cmd) != 0:
        raise Exception(f'Error: run vep fail with: {vep_cmd}')
    lines = open(vep_output).readlines()
    os.remove(vep_input)
    os.remove(vep_output)
    return cnvs, lines


