from mace_optimize_md import *
from ase.io import read

# the steps to run the code are as follows:
# 1- get structure format in ASE format
# 2- class initialization
# Note: The above two steps are a "must" at all times. However, the steps below are optional in no particular order
# 3- optimization
# 4- md NVE 
# 5- md NVT Langevin
# 6- md NVT Andersen
# 7- md NVT Berendsen
# 8- md inhomogeneous NPT Berendsen
# 9- md NPT Berendsen
# 10- md NPT combined Noose-Hoover and Parrinello-Rahman dynamics with upper-triangular cell
# 11- bulk modulus calculations

# 1- get structure format in ASE format
# Note: pymatgen and jarvis structure format do not work
atoms=read('Si_pri_POSCAR_95')

# 2- class initialization
md_run=mace_optimize_md_runs(atoms, 
				calculator='mace', # now you can even select "chgnet" calculator if you want
				dyn=None, 
				timestep=1, # units are forced to be in fs. default timestep=0.01 if left as "None", logger
				logger=None, 
				print_format = False, # "False" means you dont want to print anything, set it to "None" if you want to print something
				logfile="mace_md.log", # you can set it to None if you just want to optimize structures
				device='cpu', # you can use 'cuda' if you want to run on GPU
				default_dtype="float64", # you can use "float32" for faster but less accurate results
				bulk_modulus=None, # default bulk modulus is "None" (input must be in GPa). If you run NPT and bulk modulus is None then it will be calculated
				) 


# Note: initialize another class mace_optimizer_md_runs if you dont want the same run
# for example if you want to run NVT Langevin separately from NVT Andersen then you should initialize the class "mace_optimizer_md_runs" again
# with a different variable name from the above "md_run", 
# so the class variables with their runs will become something like "md_run1.run_nvt_langevin(...)" and "md_run2.run_nvt_andersen(...)"
# where "md_run1" and "md_run2" are different class initializations

# Mind: if you want to optimize then run NVE, NVT, NPT, or all, YOU MUST USE THE SAME CLASS VARIABLE


# 3- optimization
atoms, PE, forces=md_run.optimize_structure(optimizer="LBFGS", 
						trajectory="opt.traj", # use None to not output trajectory  
						logfile="opt.log", 
						steps=100, 
						fmax=0.1, 
						optimize_lattice=True, 
						filter = "FrechetCellFilter", # you can also use "UnitCellFilter"  
						interval=1,
						output_relaxed_structure=False,
						relaxed_filename='POSCAR_opt',
						)


# 4- md NVE
md_run.run_nve_velocity_verlet(filename="ase_nve", 
				interval=1, 
				steps=5, 
				initial_temperature_K=5,
				output_trajectory = True,
				)


# 5- md NVT Langevin
md_run.run_nvt_langevin(filename="ase_nvt_langevin", 
			interval=1, 
			temperature_K=100, 
			steps=10, 
			friction=1e-4, 
			initial_temperature_K=5,
			output_trajectory = True,
			)

# 6- md NVT Andersen 
md_run.run_nvt_andersen(filename="ase_nvt_andersen", 
			interval=1, 
			temperature_K=100, 
			steps=10, 
			andersen_prob=1e-1, 
			initial_temperature_K=None,
			output_trajectory = True,
			)


# 7- NVT Berendsen
md_run.run_nvt_berendsen(
			filename="ase_nvt_berendsen",
			interval=1,
			initial_temperature_K=1,
			temperature_K=300,
			steps=10,
			taut=None,
			)


"""
Inhomogeneous_NPTBerendsen thermo/barostat
This is a more flexible scheme that fixes three angles of the unit
cell but allows three lattice parameter to change independently.
see: https://gitlab.com/ase/ase/-/blob/master/ase/md/nptberendsen.py
"""

# 8- inhomogeneous NPT Berendsen	
md_run.run_Inhomogeneous_npt_berendsen(
			filename="ase_Inhomogeneous_npt_berendsen",
			interval=1,
			initial_temperature_K=None,
			temperature_K=300,
			steps=10,
			taut= None, #49.11347394232032,
			taup= None, #98.22694788464064,
			pressure=1.01325e-4,
			#pressure=1.01325, 
			compressibility_au=None,
			)


"""
This is a similar scheme to the Inhomogeneous_NPTBerendsen.
This is a less flexible scheme that fixes the shape of the
cell - three angles are fixed and the ratios between the three
lattice constants.
see: https://gitlab.com/ase/ase/-/blob/master/ase/md/nptberendsen.py
"""

# 9- NPT Berendsen
md_run.run_npt_berendsen(
			filename="ase_npt_berendsen",
			interval=1,
			initial_temperature_K=None,
			temperature_K=300,
			steps=10,
			taut= None, #49.11347394232032,
			taup= None, #98.22694788464064,
			pressure=1.01325e-4,
			#pressure=1.01325, 
			compressibility_au=None,
			)


# 10- NPT combined Noose-Hoover and Parrinello-Rahman dynamics with upper-triangular cell
md_run.run_npt_nose_hoover(
			filename="ase_npt_nose_hoover",
			interval=1,
			initial_temperature_K=None,
			temperature_K=300,
			steps=10,
			pressure=1.01325e-4,
			taut=None,
			taup=None,
			)


# 11- bulk modulus calculations

atoms=read('Si_conv_POSCAR_opt')
mace_MP=mace_mp(model="large", dispersion=False, default_dtype='float64', device='cpu')
#mace_MP=CHGNetCalculator()

base_EOS=mace_EOS(atoms, convert_to_primitive=True, calculator=mace_MP, optimize_input_atoms=True, device='cpu', default_dtype='float64', 
		optimizer=BFGSLineSearch, filter="FrechetCellFilter", output_relaxed_structure=False, trajectory=None, logfile=None, fmax=0.01)
base_EOS.fit(max_strain_val= 0.1, num_samples=11, optimize_strained_atoms=True, output_trajectory=False, logfile = 'opt_strained.log', output_optimized_strained_atoms=False)
print(base_EOS.get_bulk_modulus(unit="GPa"))
