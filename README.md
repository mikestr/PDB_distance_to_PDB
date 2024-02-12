# PDB_distance_to_PDB

To use this, you need a working installation of python3.

Run the script in the command line like this:

`pdb_at_dist_to_pdb_v2.py reference.pdb input.pdb`

This will produce a pdb file of input that has distance information stored in the b-factor column. 
The default is to show 10Å - distance, with a value only entered if the distance between atoms is less than 8.5.
eg:  if the atom in the reference (AtomA) is closest to AtomB at a distance of 3Å, then the value in the bfactor column for AtomA is (10-3) = 7

This is done so that the closest atoms are coloured most brightly by default in ChimeraX when colour is set to b-factor.
