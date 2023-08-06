import random
import string
import sys
import os
import configparser

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def rewrite_config(hg19_fa:str=None, hg38_fa:str=None, vep_cache:str=None) -> configparser.ConfigParser:
    for sys_path in sys.path:
        config_file = os.path.join(sys_path, 'autopvs1', 'config.ini')
        if not os.path.exists(config_file):
            continue
        config = configparser.ConfigParser()
        config.read(config_file)
        flag = False
        if hg19_fa and config.get('HG19', 'genome') != hg19_fa:
            config.set('HG19', 'genome', hg19_fa)
            flag = True
        if hg38_fa and config.get('HG38', 'genome') != hg38_fa:
            config.set('HG38', 'genome', hg38_fa)
            flag = True
        if vep_cache and config.get('DEFAULT', 'vep_cache') != vep_cache:
            config.set('DEFAULT', 'vep_cache', vep_cache)
            flag = True
        if flag:
            fo = open(config_file, 'w')
            config.write(fo)
            fo.close()
        return config


def check_vep(vep_cache:str=None):
    if vep_cache and not os.path.exists(vep_cache):
        raise Exception(f'ERROR: vep_cache not found: {vep_cache}')
    for cmdpath in os.environ['PATH'].split(':'):
        if os.path.isdir(cmdpath) and 'vep' in os.listdir(cmdpath):
            return
    raise Exception('ERROR: vep not found, please install it first')