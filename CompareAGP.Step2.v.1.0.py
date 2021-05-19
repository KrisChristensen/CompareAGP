##########################################################
### Import Necessary Modules

import argparse                       #provides options at the command line
import sys                       #take command line arguments and uses it in the script
import gzip                       #allows gzipped files to be read
import re                       #allows regular expressions to be used
import textwrap                       #allows the use of textwrapping for long sequences

##########################################################
### Command-line Arguments
parser = argparse.ArgumentParser(description="A script to add cM positions to comparison output by CompareAGP.v.1.0.py.")
parser.add_argument("-comparison", help = "The comparison file output by CompareAGP.v.1.0.py", default=sys.stdin, required=True)
parser.add_argument("-log", help = "The log files generated from chromonomer", default=sys.stdin, required=True, nargs="+")
args = parser.parse_args()


#########################################################

###Setup dictionaries to store info
class Variables():
    cM = {}

class OpenFile():
    def __init__ (self, f, typ):
        """Opens a file (gzipped) accepted"""
        if re.search(".gz$", f):
            self.filename = gzip.open(f, 'rb')
        else:
            self.filename = open(f, 'r') 
        if typ == "log":
            ReadLog(self.filename)
        else:
            ReadCom(self.filename)

class ReadLog():
    def __init__ (self,f):
        """Reads log file produced by chromonomer and returns a variable for each contig and the corresponding cM position"""
        self.previousCM = 0
        for self.line in f:
            if not re.search("unmodified:$", self.line):
                self.line = self.line.rstrip('\n')
                if re.search("contig", self.line) or re.search("scaffold", self.line):
                    self.contig = self.line.split()[0]
                    if self.contig in Variables.cM:
                        Variables.cM[self.contig] = "{}|{}".format(Variables.cM[self.contig], self.previousCM)
                    else:
                        Variables.cM[self.contig] = self.previousCM
                    #print ("{}\t{}".format(self.contig, self.previousCM))
                elif re.search("^\d", self.line):
                    self.previousCM = self.line
                    #print ("{}".format(self.line))
        f.close()

class ReadCom():
    def __init__ (self,f):
        """Reads in the output of the CompareAGP.v1.0.py script and outputs the corresponding cM positions"""
        for self.line in f:
            self.line = self.line.rstrip('\n')
            self.contig = self.line.split()[-1]
            if self.contig in Variables.cM:
                print ("{}\t{}".format(self.line, Variables.cM[self.contig]))
            else:
                print ("{}\t{}".format(self.line, ""))
        f.close()

if __name__ == '__main__':
    Variables()
    for logs in args.log:
        open_file = OpenFile(logs, "log")
    open_file = OpenFile(args.comparison, "com")
