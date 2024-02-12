#!/usr/bin/env python
# this script produces a pdb with bfactors altered to reflect distance to another pdb.
# Mike Strauss Aug 2013
# modified, June 2023 - output bfactor reverse to distance (10-dist)
#
"""
run either as script by changing file names in here, or

usage: pdb_at_dist_to_pdb_v2.py ref.pdb in_file.pdb
"""

from math import sqrt
import sys, os

#################



def clean(x): return x!=''

def distance(p1,p2):
    d=sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)
    return d

def get_pdb(document) :
	doct=open(document,'r')
	doc=doct.readlines()
	doct.close()
	out=[]

	for line in doc:
		line0=line.rstrip("\n")
		line1=line0.split(' ')
		line2=filter(clean,line1)
		out.append(line2)
	return out

def pdb_to_list(file_in):
    if type(file_in) == type(sys.stdin):
      readfile = file_in
    else:
      readfile = open(file_in,'r')
    lines = readfile.readlines()
    print(len(lines))
    i = 0
    pdf_list=[]
    for line in lines:
        if len(line) >= 55:
            line = line[:-1]
            label = line[0:6]
            atnum = int(line[6:12])
            atname = line[12:16]
            atalt = line[16:17]
            resname = line[17:21]
            chain = line[21]
            resnum = int(line[22:26])
            resext = line[27]
            coord = [float(line[30:38]), float(line[38:46]), float(line[46:54])]
            occ = float(line[54:60])
            b = float(line[60:66])
            lin_entry=[label,atnum,atname,atalt,resname,chain,resnum,resext,coord,occ,b]
            pdf_list.append(lin_entry)
    return pdf_list


def list_to_pdb(in_list,file_out):
    if type(file_out) == type(sys.stdout):
      out = file_out
    else:
      out = open(file_out,'w')
    blank=''
    for ea in in_list:
        [label,atnum,atname,atalt,resname,chain,resnum,resext,coord,occ,b]=ea
        out.write('%-6s%5i %-4s%1s%-4s%1s%4i%1s   %8.3f%8.3f%8.3f%6.2f%6.2f%10s%2s\n' %
        (label,atnum,atname,atalt,resname,chain, resnum,resext,
        coord[0],coord[1],coord[2],occ,b,blank,atname))
    out.close()

#Original
def dist_to_pdb(dist_list, ref_list, radius2=8.5):
	it1=0
	dt1=len(dist_list)
	pdb_out_list=[]
	distances=[]
	for eb in dist_list:
		is_incl=0
		distances=[]
		for cs in ref_list:
			dist=distance(cs[8],eb[8])
			distances.append(dist)
		mindist=min(distances)
		if mindist<=radius2:
			eb[10]=10-mindist  # adjusted to reverse numbers: big numbers small dist
		else:
			eb[10]=10-radius2
		pdb_out_list.append(eb)

		#if is_incl==0:
		#	eb[10]=radius2
		#	pdb_out_list.append(eb)
		#else:
		#	pdb_out_list.append(eb)
		s9=(it1+1.)/dt1; sys.stdout.write(' %3d percent completed.  %s\r' % (int(100*s9),(str("|<"+"="*int(15*s9)+">"+" "*(15-int(15*s9))+"|")))); sys.stdout.flush()
		it1+=1


	return pdb_out_list


def bfact_by_dist(dist_pdb, ref_pdb, out_pdb, r2=8.5 ):
    dlist=pdb_to_list(dist_pdb)
    rlist=pdb_to_list(ref_pdb)
    olist=dist_to_pdb(dlist,rlist,radius2=r2)
    print("writing "+out_pdb+" to file")
    list_to_pdb(olist, out_pdb)

    ######################################

# define max distance to neighbouring residues to consider
rad2=8.5
in_fils=[]
if len(sys.argv) > 1:
    r1 = sys.argv[1]
    print(r1)
    in_fils.append(sys.argv[2])
    print(in_fils)
else:
    print("please specify the names of 2 pdb files")

for ea in in_fils:
    i1=ea
      o1=os.path.basename(i1).rstrip(".pdb")+"_within"+str(rad2)+".pdb"
    bfact_by_dist(i1,r1,o1,rad2)
 
