# autoPVS1 batch

该包集成[autoPVS1](https://github.com/JiguangPeng/autopvs1) ，实现以VCF/BED文件为输入对多个变异批量VEP注释及autoPVS1注释。
拟解决的问题：
1. autoPVS1集成VEP注释命令行，一次只能注释一个变异，若需要对大量变异进行分析，则需要多次运行vep注释命令行。
2. 本工具首先使用vep对保存大量变异的VCF/BED文件进行注释，并重写了AutoPVS1.vep_run逻辑（由运行vep注释单个变异改为根据vep结果过滤出指定变异的注释信息）
   1. VCF：对应SNV变异
   2. BED：对应CNV变异
   
## 参数说明

- -i/--input: 输入文件, VCF for SNV, BED for CNV
- -o/--outfile: 输出autoPVS1结果
- -r/--hg19_fa: hg19 参考序列fasta文件路径
- -R/--hg38_fa: hg38 参考序列fasta文件路径
- -d/--vep_cahce: vep cache目录，即vep数据库目录路径
- -g/--genome_version: 当前变异对应的基因组版本，可选项：hg19, hg38

## 安装运行
```shell
zhuy@ubuntu:/projects/example$ pip install autopvs1-batch
zhuy@ubuntu:/projects/example$ autopvs1-batch.py -i test.vcf -o test.autopvs1_anno.txt -r /path/to/hg19.fa -R /path/to/hg38.fa -d ~/.vep -g hg19 
```

### 结果说明
1. 变异
2. PVS1 criterion
3. PVS1 strength_raw
4. PVS1 strength

```text
1:5935162:5935162:A:T           SS9    Strength.Moderate      Strength.Moderate
3:142281601:142281604:GAGT:-    NF1    Strength.VeryStrong    Strength.Unset
```

### 限制
1. 本工具仅在python>=3.8环境下进行测试过。
2. 本工具引入autoPVS1项目代码并本着不对该项目代码进行任何改动的原则，由于autoPVS1源码内部机制读取config.ini相对路径写死了，因此本工具运行时需要修改`site-packages/autopvs1/config.ini`文件内容，要求执行用户对该文件局具有写权限。
   1. root用户环境下运行此工具
   2. 或在用户所属pyenv，conda等对config.ini有写权限的环境下运行此工具