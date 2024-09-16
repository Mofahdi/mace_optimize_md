# MACE_optimize_md
code to run optimize materials and run molecular dynamics (md) simulations using CHGNet and MACE (i.e., machine learning potentials (MLP)) tools

## Usage
**Note:** you have to put both files "*mace_optimize_md_classes.py*" and "*mace_optimize_md_run.py*" in the same path since "*mace_optimize_md_run.py*" inherits classes from "*mace_optimize_md_classes.py*". The code will output the above files in the same path where you put "*mace_optimize_md_classes.py*" and "*mace_optimize_md_run.py*".


## the steps to run the code are as follows:
1- get structure format in ASE format \
2- class initialization \
**Note**: The above two steps are a **"must"** at all times. However, the steps below are optional in no particular order \
3- optimization \
4- md NVE  \
5- md NVT Langevin \
6- md NVT Andersen \
7- md NVT Berendsen \
8- md inhomogeneous NPT Berendsen \
9- md NPT Berendsen \
10- md NPT combined Noose-Hoover and Parrinello-Rahman dynamics with upper-triangular cell \
11- bulk modulus calculations (bulk modulus calculations are done automatically if bulk modulus is not provided in NPT simulations) \



## Required Packages
the code is tested on the following packages and versions:
<code>torch=2.0.1</code>
<code>ase=3.23.0</code>
<code>pymatgen=2023.11.12</code>
<code>e3nn=0.4.4</code>
<code>mace-torch=0.3.6</code>
<code>chgnet=0.3.5</code>
<code>jarvis-tools=2024.4.30</code>
</br>The code can probably work with different versions of the above packages

## Credit
* Please consider reading my published work in Google Scholar using this [link](https://scholar.google.com/citations?user=5tkWy4AAAAAJ&hl=en&oi=ao) thank you :)
* also please let me know if more features are needed to be added and/or improved 
