# ReadCounts
RNA-Seq is a sequencing technique that has been utilized in quantifying cellular transcriptome and 
enable a better understanding of various biological processess.

One key step in RNASeq data analysis involves generation of count data following mapping of 
next-generation sequence data to host reference genomes. With limited access to high-performance computing
environments and due to large sizes of reads and host files involved, this process has become challenging.

Working with [LathcBio](https://latch.bio/), I have automated the read-count step within the RNASeq workflow.

[ReadCount](https://console.latch.bio/workflows/82370/info) tool takes in host reference genome and its associated annotation file plus filtered raw reads and outputs 
count data that can be taken forward for analysis.


Try it by following this [Link](https://console.latch.bio/workflows/82370/info)