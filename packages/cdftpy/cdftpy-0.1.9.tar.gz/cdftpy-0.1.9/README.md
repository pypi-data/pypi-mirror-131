![Tests](https://github.com/mvaliev/cdftpy/actions/workflows/tests.yaml/badge.svg)

## CDFTPY: Python package for performing classical density functional theory calculations for molecular liquids 
#### Marat Valiev and Gennady Chuev
___
#### Quick Start:
___

Standard RISM calculation can be run as

   rism1d <input_file>

RSDFT calculation can be run as

   rsdft1d <input_file>

where <input_file> is the optional input file. An example of the latter 
for simulation of ion solvation in two-site water model is given below

     <solute>
     # site   sigma        eps(kj/mol)    charge(e)    x   y   z
     Cl       4.83         0.05349244     -1.0         0.0 0.0 0.0
     <simulation>
     solvent s2
     tol 1.0E-7
     max_iter 200
     
     #optional analysis
     <analysis>
     rdf_peaks
     <output>
     rdf

In the absense of the input file, the calculation will be run interactively
___
#### References:
___
G.N. Chuev, M. V. Fedotova and M. Valiev,
 Renormalized site density functional theory,
 J. Stat. Mech. (2021) 033205, https://doi.org/10.1088/1742-5468/abdeb3

G.N. Chuev, M. V. Fedotova and M. Valiev,
Chemical bond effects in classical site density 
functional theory of inhomogeneous molecular liquids. 
J. Chem Phys. 2020 Jan 31;152(4):041101,
https://doi.org/10.1063/1.5139619

M. Valiev and G.N. Chuev,
 Site density models of inhomogeneous classical molecular liquids,
 J. Stat. Mech. (2018) 093201,
https://doi.org/10.1088/1742-5468/aad6bf

 
 
