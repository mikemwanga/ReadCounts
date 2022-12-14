FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:6839-main

RUN apt-get install -y curl unzip
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh --output miniconda.sh
ENV CONDA_DIR /opt/conda
RUN bash miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
RUN conda install -c bioconda fastp
RUN conda install -c bioconda star
# Its easy to build binaries from source that you can later reference as
# subprocesses within your workflow.
# RUN curl -L https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.4/bowtie2-2.4.4-linux-x86_64.zip/download -o bowtie2-2.4.4.zip &&\
#     unzip bowtie2-2.4.4.zip &&\
#     mv bowtie2-2.4.4-linux-x86_64 bowtie2

# Or use managed library distributions through the container OS's package
# manager.
# RUN apt-get update -y &&\
#     apt-get install -y autoconf samtools


# You can use local data to construct your workflow image.  Here we copy a
# pre-indexed reference to a path that our workflow can reference.
COPY data /root/reference
#ENV BOWTIE2_INDEXES="reference"

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root
