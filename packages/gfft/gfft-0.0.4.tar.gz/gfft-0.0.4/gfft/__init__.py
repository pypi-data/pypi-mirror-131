import sys, pickle
from gfft.gfft import process_gff
    
def main():
    args = sys.argv    #  <- list of all the args in orderthey were given, here 3 args
    infile = args[1]
    outfile = args[2]
    try: 
        first_n = int(args[3])
    except IndexError:
        first_n = None
        
    genome = process_gff(infile,  first_n = first_n)
    
    pickle.dump(genome, open(outfile, 'wb'))
    
