from pathlib import Path
from autopvs1 import AutoPVS1 as AutoPVS1Default, AutoPVS1CNV as AutoPVS1CNVDefault
from .vcf import SNV
from .bed import CNV
from .vep import filter_vep

class AutoPVS1(AutoPVS1Default):
    def __init__(self, snv:SNV, vep_lines: list, genome_version:str, user_trans=None):
        self.snv = snv
        self.vep_lines = vep_lines
        super().__init__(f'{snv.chrom}-{snv.pos}-{snv.ref}-{snv.alt}', genome_version, user_trans)

    def vep_run(self):
        Path(self.vep_input).touch(exist_ok=True)
        filter_vep(variant_id=self.snv.id, vep_lines=self.vep_lines, vep_output=self.vep_output)


class AutoPVS1CNV(AutoPVS1CNVDefault):
    def __init__(self, cnv:CNV, vep_lines: list, genome_version:str, user_trans=None):
        self.cnv = cnv
        self.vep_lines = vep_lines
        super().__init__(f'{cnv.chrom}-{cnv.start}-{cnv.end}-{cnv.type}', genome_version, user_trans)

    def vep_run(self):
        Path(self.vep_input).touch(exist_ok=True)
        filter_vep(variant_id=self.cnv.id, vep_lines=self.vep_lines, vep_output=self.vep_output)