# CompareAGP
A script to compare agp files.  Outputs all the contigs/scaffolds from the first file and any matching from the second.

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#requirements">Requirements</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- requirements -->
## Requirements

This script has been tested with Python 2.7 and 3 and should work with either (except with compressed files).
The script requires two AGP files.  The AGP files can be compressed with gzip (only works with Python 2.7 for now).  This script also requires an AGP file.

<!-- usage -->
## Usage

Find Pairwise:
python CompareAGP.v.1.0.py -file1 file1.agp -file2 file2.agp > Comparison.txt

To see the usage and get futher information: python CompareAGP.v.1.0.py -h


<!-- license -->
## License 

Distributed under the MIT License.
