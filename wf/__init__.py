"""
Generate read counts from RNASeq dataset
"""

import subprocess
from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchFile, LatchDir

@small_task
def filter(read1: LatchFile, read2: LatchFile,refseq:LatchFile,gtf:LatchFile) -> LatchDir:

    #create files
    touch = ["touch","filtered_1.fastq.gz","filtered_2.fastq.gz"]
    subprocess.run(touch)
    # A reference to our output.
    outfile1 = Path("filtered_1.fastq.gz").resolve()
    outfile2 = Path("filtered_2.fastq.gz").resolve()
    
    filter = [
        "fastp",
        "-i",read1,
        "-I",read2,
        "-o",outfile1,
        "-O",outfile2]

    subprocess.run(filter)  

    #create folder
    dir = ["mkdir","filtered_DIR"]
    subprocess.run(dir)
    data_dir = Path("filtered_DIR").resolve()
   
    #mov files in there
    mv = ["mv", outfile1, outfile2, data_dir]
    subprocess.run(mv)

    map_dir = ["mkdir","genome_DIR"]
    subprocess.run(map_dir)
    genome_indices = Path("genome_DIR").resolve()

    #generate index for reference genome
    align = [
            "STAR","--runThreadN","6",
            "--runMode","genomeGenerate",
            "--genomeDir",genome_indices,
            "--genomeFastaFiles",refseq,
            "--sjdbGTFfile",gtf,
            "--sjdbOverhang","99"
        ]
    subprocess.run(align)

    #map reads to the reference

    map = [
        "STAR", 
        "--genomeDir",genome_indices,
        "--runThreadN","6",
        "--readFilesIn", data_dir,
        "--outSAMunmapped","Within", 
        "--outSAMattributes","Standard"

    ]
    subprocess.run(map)

    return LatchDir(path = str(genome_indices), remote_path = f"latch:///{genome_indices}/")
    
    #LatchDir(str(data_dir), "latch:///filtered_DIR")
           # LatchFile(str(outfile2), "latch:///filtered_2.fastq.gz")
           # ]

@workflow
def readcount(read1: LatchFile, read2: LatchFile,refseq:LatchFile, gtf:LatchFile) -> LatchDir:
    """Generate counts for RNASeq downstream analysis

    ReadCount
    ----
    # ReadCounts
    RNA-Seq is a sequencing technique that has been utilized in quantifying cellular transcriptome and 
    enable a better understanding of various biological processess.

    One key step in RNASeq data analysis involves generation of count data following mapping of 
    next-generation sequence data to host reference genomes. With limited access to high-performance computing
    environments and due to large sizes of reads and host files involved, this process has become challenging.

    Working with [LathcBio](https://latch.bio/), I have automated the read-count step within the RNASeq workflow.

    [ReadCount](https://github.com/mikemwanga/ReadCounts) tool takes in host reference genome and its associated annotation file plus filtered raw reads and outputs 
    count data that can be taken forward for analysis.


    __metadata__:
        display_name: ReadCount
        author:
            name:
            email:
            github:
        repository:
        license:
            id: MIT

    Args:

        read1:
          Paired-end read 1 file to be assembled.

          __metadata__:
            display_name: Read1

        read2:
          Paired-end read 2 file to be assembled.

          __metadata__:
            display_name: Read2
        refseq:
        	Reference genome sequence
        	
        	__metadata__
        	display_name: Ref_Sequence
        gtf:
            Reference annotation file
            display_name: Annotation_file
    """
    #sam = assembly_task(read1=read1, read2=read2)
    return filter(read1=read1, read2=read2, refseq =refseq,gtf=gtf)
