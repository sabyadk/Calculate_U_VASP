# Final code after you have the converged calculations of U to obtain the U value
#First lines of argument are no of atoms of each species

#python ../../src/regression.py natom_species1 natom_species2 --materials species_1 species_2 --alpha -0.1 0.05 0.05 0.1

python ../../src/regression.py 6 2 --materials Cr I --alpha -0.1 -0.05 0.05 0.1
