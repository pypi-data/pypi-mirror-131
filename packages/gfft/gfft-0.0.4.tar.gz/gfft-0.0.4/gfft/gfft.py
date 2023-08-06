#!/usr/bin/env python
###Module/Desc.


###Import Section
import os, sys, pickle
from tqdm import tqdm
from urllib.parse import unquote
from collections import Counter, namedtuple

###Constants/Globals


####Objects
GffEntry = namedtuple('GffEntry', (
    'seqid',
    'source',
    'gff_type',
    'start',
    'end',
    'score',
    'strand',
    'phase',
    'attributes'
    )
)


class Genome:
    def __init__(self, header):
        self.chromosomes = {}   #key is what chromosome we are on, value is the chromosome object 
        self._parse_header(header)
        
    @property
    def n_chromosomes(self):
        return len(self.chromosomes)
    
    @property
    def n_exons(self):
        exon_count = 0
        for chrom in self.chromosomes.values():
            exon_count += chrom.n_exons
        return exon_count
    
    @property
    def length(self):
        length = 0
        for chrom in self.chromosomes.values():
            length += chrom.length
        return length
    
    def _parse_header(self, header):
        for metadata in header:
            tag, val = metadata[2:].split(maxsplit=1)
            tag = tag.replace('-', '_')
            setattr(self, tag, val)
      
    
class BaseGFF:
    
    def __init__(
        self,
        seqid,
        source,
        gfftype,    #this is how we will classify our gff objects 
        start,
        end,
        score,
        strand,
        phase,
        attributes
                ):
        self.seqid = seqid
        self.source = source
        self.gfftype = gfftype
        self.start = int(start)
        self.end = int(end)
        self.score = score
        self.strand = strand
        self.phase = phase
        self.attributes = attributes
        self._init_feature()
    
    @property     
    def length(self):     # due to @property decorator the end user will see this as an attribute, though it is technically a method that caluclated this propety from other information. In this case, the information its calucaoting from are attrbiutes of the calls 
        return self.end - self.start + 1
    
    def _init_feature(self):  #this has a SINGLE underscore, not a double underscore and thus lacks a dunder. 
        pass
    
    def __str__(self):
        return '\t'.join([
            self.seqid,
            self.source,
            self.gfftype,
            str(self.start),
            str(self.end),
            self.score,
            self.strand,
            self.phase,
            str(self.attributes)
        ])
    
    def __repr__(self):
        return f'{type(self).__name__}({self.seqid}, {self.source}, {self.gfftype}, {self.start}, {self.end}, {self.score}, {self.strand}, {self.phase}, {self.attributes})'
    

class Chromosome(BaseGFF):
    def _init_feature(self):
        self.genes = {} 
        self.enhancers = {}
        name = self.attributes['chromosome']
        self.chromosome = int(name) if name.isdigit() else name
        
    @property
    def n_genes(self):
        return len(self.genes)
    
    @property
    def n_enhancer(self):
        return len(self.enhancer)
    
    
class Gene(BaseGFF): 
    def _init_feature(self):
        self.name = self.attributes['Name']
        self.lnc_RNAs = {}
        self.exons = {}
        self.cds = {}
        self.mRNAs = {}
        
    @property
    def n_lnc_RNA(self):
        return len(self.lnc_RNAs)
    
    @property
    def n_exons(self):
        return len(self.exons)
    
    @property
    def n_mRNA(self):
        return len(self.mRNA)
    
    @property
    def n_CDS(self):
        return len(self.CDS)

    
class Lnc_RNA(BaseGFF): 
    def _init_feature(self):
        self.name = self.attributes['Name']  #dictionary lookup, hence square brackets
        self.parent_gene = self.attributes['gene']  

    
class Enhancer(BaseGFF):
    def _init_feature(self):
        self.name = self.attributes['ID'] 
        
        
class Exon(BaseGFF):
    def _init_feature(self):
        self.ID = self.attributes['ID']
        self.gene = self.attributes['gene']
        self.exon_number = int(self.ID.split('-')[-1])
        
        
class mRNA(BaseGFF):
    def _init_feature(self):
        self.name = self.attributes['Name'] 
        self.gene = self.attributes['gene']

        
class CDS(BaseGFF):
    def _init_feature(self):
        self.name = self.attributes['Name'] if 'Name' in self.attributes else None
        self.gene = self.attributes['gene']

        
###Functions
def get_header(fileObject):
    """This function opend filer object and checks header for #, then makes a list comprised of the header column names
    """
    header = []
    gff_version = next(fileObject).strip() # Always the first line of a GFF file
    header.append(gff_version)
    
    for header_line in fileObject:
        if header_line.startswith('#!'):          # selectively capture the "metadata" of the header
            header.append(header_line.strip())
        else:                              # Once "##" is observed (start of chromosome), we are done
            return Genome(header)   
            
            
def split_attributes(attribute_string):
    attr_dict = {}
    for attribute in attribute_string.split(';'):
        key, vals = attribute.split('=')
        vals = vals.split(',')
        for i, val in enumerate(vals):
            vals[i] = unquote(val)
        if len(vals) == 1:
            vals = vals[0]
        attr_dict[key] = vals
    return attr_dict


def gen_gff(fileObject, delimiter):
    """This function reads a file, line by line, and creates a class 
    Args:
        fileObject (fileObject) : open file object
        delimeter (str) : what is the character that serves to delimit a column from another column (default: '\t')
    Output:
        (GffEntry): a namedtuple consisting of the variable names associated with the standard gff3 format    
    """
    for row in fileObject:
        if not row.startswith('#'):
            *first_8, attrs = row.strip().split(delimiter)
            yield GffEntry(*first_8, split_attributes(attrs)) 
          
        
def process_gff(filepath, delimiter = '\t', first_n = None):
    file_length = first_n if first_n else sum(1 for line in open(filepath))
    object_count = 0
    with open(filepath) as dataset:
        genome = get_header(dataset) # get header and puts into metadata, notee that it shovees stuff into a genome object 
        with tqdm(total=file_length) as prog_bar:
            for i, gff_entry in enumerate(gen_gff(dataset, delimiter = delimiter)): #shavees off gff one at a time makes our gfff object 
            #  if gff_entry.gfftype == 'exon': #DEBUG
            #       return gff_entry
                if gff_entry.gff_type == "mRNA":
                    mRNA_object = mRNA(*gff_entry)
                    genome.chromosomes[curr_chrom]\
                        .genes[mRNA_object.gene]\
                        .mRNAs[mRNA_object.name] = mRNA_object 
                elif gff_entry.gff_type == "CDS":
                     if gff_entry.attributes['gene'] in genome.chromosomes[curr_chrom].genes:
                        CDS_object = CDS(*gff_entry)
                        genome.chromosomes[curr_chrom]\
                            .genes[CDS_object.gene]\
                            .cds[CDS_object.name] = CDS_object 
                elif gff_entry.gff_type ==  "gene":
                    gene_object = Gene(*gff_entry)
                    genome.chromosomes[curr_chrom]\
                        .genes[gene_object.name] = gene_object 
                elif gff_entry.gff_type == "enhancer":
                    enhancer_object = Enhancer(*gff_entry)
                    genome.chromosomes[curr_chrom]\
                        .enhancers[gene_object.name] = enhancer_object
                elif gff_entry.gff_type ==  "lnc_RNA":
                    if gff_entry.attributes['gene'] in genome.chromosomes[curr_chrom].genes:
                        lnc_RNA_object = Lnc_RNA(*gff_entry)
                        genome.chromosomes[curr_chrom]\
                        .genes[lnc_RNA_object.parent_gene]\
                        .lnc_RNAs[lnc_RNA_object.name] = lnc_RNA_object 
                elif gff_entry.gff_type == "exon":
                    if gff_entry.attributes['gene'] in genome.chromosomes[curr_chrom].genes:
                        exon_object = Exon(*gff_entry)
                        genome.chromosomes[curr_chrom]\
                            .genes[exon_object.gene]\
                            .exons[exon_object.ID] = exon_object
                elif gff_entry.gff_type == "region":
                    if gff_entry.attributes.get("genome", None) == 'chromosome':
                        chromosome_object = Chromosome(*gff_entry)
                        curr_chrom = chromosome_object.chromosome
                        genome.chromosomes[curr_chrom] = chromosome_object
                else:
                    continue
                
                prog_bar.update(1)
                object_count += 1
                
                if  object_count == first_n:
                    break 
        return genome     


###Operational Code... "note that process_gff is the function that uses all the other functions"pything. 

###Runtime Behavior ..."how does the user run the application from the command line"

if __name__ == '__main__':
    args = sys.argv    #  <- list of all the args in orderthey were given, here 3 args
    infile = args[1]
    outfile = args[2]
    try: 
        first_n = int(args[3])
    except IndexError:
        first_n = None
        
    genome = process_gff(infile,  first_n = first_n)
    
    pickle.dump(genome, open(outfile, 'wb'))
    
    #TO DO.... pickle the genome 
    # what is a pickle object? Given that any objects we create in python application, when we turn it off the objects are gone since they are only used for the purpose of generating our OUTPUT from our INPUT. Pickle, however, allows us to store these lists, dicts, objects etc exist on the hard drive. 
    
#NOTE number_of_lines_to_process is what we mean when we say first_n
#The three args, in order ; 1.) inflile, the file being run 2.) outfile name 3.) number of entries (optional) 




