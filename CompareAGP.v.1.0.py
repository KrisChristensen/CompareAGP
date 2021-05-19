##########################################################
### Import Necessary Modules

import argparse                       #provides options at the command line
import sys                       #take command line arguments and uses it in the script
import gzip                       #allows gzipped files to be read
import re                       #allows regular expressions to be used
import textwrap                       #allows the use of textwrapping for long sequences

##########################################################
### Command-line Arguments
parser = argparse.ArgumentParser(description="A script to compare agp files.  Outputs all the contigs/scaffolds from the first file and any matching from the second.")
parser.add_argument("-file1", help = "A standard AGP file with matching contigs/scaffolds", default=sys.stdin, required=True)
parser.add_argument("-file2", help = "A standard AGP file with matching contigs/scaffolds", default=sys.stdin, required=True)
args = parser.parse_args()


#########################################################

###Setup dictionaries to store info
class Variables():
    agp = {}
    agp[1] = {}
    agp[2] = {}
    order = {}
    order[1] = {}
    order[2] = {}

class OpenFile():
    def __init__ (self, f, typ):
        """Opens a file (gzipped) accepted"""
        if re.search(".gz$", f):
            self.filename = gzip.open(f, 'rb')
        else:
            self.filename = open(f, 'r') 
        if typ == "file1":
            ReadFile(self.filename, 1)
        else:
            ReadFile(self.filename, 2)

class ReadFile():
    def __init__ (self,f,n):
        """Reads agp files and stores data in Variables hash"""
        for self.line in f:
            if not re.search("^#", self.line):
                self.line = self.line.rstrip('\n')
                self.chr, self.pos1, self.pos2, self.order, self.spacing, self.contig, self.cPos1, self.cPos2, self.orientation  = self.line.split()
                if self.spacing == "W":
                    Variables.agp[n][self.contig] = "{}\t{}\t{}".format(self.chr, self.order, self.orientation)
                    #print ("{}\t{}\t{}".format(self.chr, self.order, self.orientation))
                    if self.chr in Variables.order[n]:
                        Variables.order[n][self.chr][int(self.order)] = self.contig
                    else:
                        Variables.order[n][self.chr] = {}
                        Variables.order[n][self.chr][int(self.order)] = self.contig
        f.close()

class Output():
    def __init__ (self):
        """Outputs the comparison between the two agp files"""
        for self.chr in Variables.order[1]:
            for self.order in sorted(Variables.order[1][self.chr].keys()):
                self.contig = Variables.order[1][self.chr][self.order]
                self.chr1, self.order1, self.orientation1 = Variables.agp[1][self.contig].split()
                if self.contig in Variables.agp[2]:
                    self.chr2, self.order2, self.orientation2 = Variables.agp[2][self.contig].split()
                    print ("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.chr1, self.order1, self.orientation1, self.chr2, self.order2, self.orientation2, self.contig))
                else:
                    print ("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.chr1, self.order1, self.orientation1, "", "", "", self.contig))

if __name__ == '__main__':
    Variables()
    open_file = OpenFile(args.file1, "file1")
    open_file = OpenFile(args.file2, "file2")
    Output()
