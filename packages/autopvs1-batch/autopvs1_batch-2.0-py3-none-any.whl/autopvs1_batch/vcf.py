import re
from collections import namedtuple

SNV = namedtuple('SNV', ['chrom', 'pos', 'id', 'ref', 'alt'])

def vcf_id_generator(chrom:str, pos:int, ref:str, alt:str)->str:
    start = pos
    if len(ref) > 1 or len(alt) > 1 and ref != alt:
        if ref.startswith(alt) or ref.endswith(alt):
            if ref.startswith(alt): start = start + len(alt)
            ref = ref.replace(alt, '', 1)
            alt = ''
        elif alt.startswith(ref) or alt.endswith(ref):
            start = start + len(ref) - 1 if alt.startswith(ref) else start - len(alt) + len(ref)
            alt = alt.replace(ref, '', 1)
            ref = ''
        else:
            ref_rev, alt_rev, substr, stop, index = ref[::-1], alt[::-1], '', False, 0
            while index < len(ref) and index < len(alt):
                if ref_rev[index] != alt_rev[index]: stop = True
                if ref_rev[index] == alt_rev[index] and not stop: substr = ref_rev[index] + substr
                index += 1
            ref = re.sub(r'%s$' % substr, '', ref)
            alt = re.sub(r'%s$' % substr, '', alt)
            substr, stop, index = '', False, 0
            while index < len(ref) and index < len(alt):
                if ref[index] != alt[index]: stop = True
                if ref[index] == alt[index] and not stop: substr += ref[index]
                index += 1
            ref = re.sub(r'^%s' % substr, '', ref)
            alt = re.sub(r'^%s' % substr, '', alt)
            start += len(substr) - 1 if len(substr) and not ref else len(substr)
    end = start + len(ref) - 1 if ref else start
    return f'{chrom}:{start}:{end}:{ref if ref else "-"}:{alt if alt else "-"}'

def read_vcf(vcf:str) -> list:
    snvs = list()
    fi = open(vcf)
    for line in fi:
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        fields = line.split('\t')
        chrom, pos, snv_id, ref, alt = fields[0:5]
        chrom = chrom.replace('chr', '')
        if chrom[0] == "M": chrom = "MT"
        if snv_id == '.':
            snv_id = vcf_id_generator(chrom, int(pos), ref, alt)
        snvs.append(SNV(chrom=chrom, pos=int(pos), ref=ref, alt=alt, id=snv_id))
    fi.close()
    return snvs

def write_vcf(snvs:list, out_vcf:str):
    fo = open(out_vcf, 'w')
    for snv in snvs:
        fo.write(f'{snv.chrom}\t{snv.pos}\t{snv.id}\t{snv.ref}\t{snv.alt}\t.\tPASS\t.\n')
    fo.close()