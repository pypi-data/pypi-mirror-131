# periodicgw

This is a Python package for **generating 2D periodic random groundwater flux fields with any user specified mean flow vector**. Periodic random hydraulic conductivity fields are generated that are locally multi-Gaussian with user-selectable semi-variograms and anisotropy structures. **Darcy flux fields are solved exactly using a finite volume approach** on these conductivity fields with periodic boundary conditions and an enforced mean flow angle. **Inter-cell fluxes are directly reported for compatibility with particle tracking algorithms based on the Pollock method.**

## Overview
This package generates random, periodic, locally Gaussian conductivity fields by use of the fast Fourier transform approach. It solves the steady-state groundwater flow equation on a random heterogeneous conductivity field, with periodic boundary conditions in both directions. Solution is finite volume, and formulated directly for the interfacial fluxes rather than for heads. 

Two classes and three functions are exposed, whose usage details are illustrated below.

**Classes:**
- `DomainData(nr, nc, dr, dc)` constructs an object representing an `nr` by `nc` rectangular structured grid whose cells have dimension `dr` by `dc`. Internally, the code works with coordinate axes _r_ ("row") and _c_ ("column"). _r_ is the 0-based row index for interacting with external codes, increasing _r_ corresponds to increasing _y_. _c_ is the 0-based column index for interacting with external codes, increasing _c_ corresponds to increasing _x_.

- `RandomKField(dd, model_ref, var, corr_len, f_lambda, azimuth)` constructs an object representing a lognormal K field defined on the `DomainData` grid `dd`, with user-defined structural parameters. `model_ref` represents the reference number of chosen covariance model (`1` indicates exponential covariance and `2` indicates Gaussian covariance). `var` is the log-variance of the field, and `corr_len` is its correlation length (in the direction of the principal axis of anisotropy). Geometric anisotropy is defined by `f_lambda`, the ratio of major axis correlation length to minor axis correlation length, and `azimuth`, the angle of the major axis of anisotropy above the _c_-axis (i.e., _x_-axis). 

**Functions:**
- `solve_q(K, angle=0)` returns a tuple `(qr, qc)`, each component of which is a Numpy array of the same shape as the `RandomKField` `K`. Element (_i_,_j_) of array `qr` represents the positive-directed outward-bound flux in the _r_-direction originating in cell (_i_,_j_) of field `K`. This is to say the flux from domain grid cell (_i_,_j_) to (_i_+1,_j_), assuming both cells are in the interior of the domain. Fluxes wrap around due to periodicity, so that if _R_ is the largest row index, element (_R_,_j_) of `qr` represents the flux from grid cell (_R_,_j_) to (0,_j_) of the domain. `qc` is similarly defined, but contains the positive-directed outward-bound flux in the _c_-direction for each domain grid cell. `qr` and `qc` are normalized so that the mean Darcy flux has unit norm. `angle` represents the mean flow angle (in radians) above the _c_-axis (i.e., _x_-axis). 

- `plot_lognormal_field(K)` generates a colormap plot of the base-10 logarithm of `RandomKField` object `K`. 

- `plot_quiver(K, qr, qc)` generates a quiver plot of interpolated cell-centre Darcy fluxes contained in the Numpy arrays `qr` and `qc` (discussed above). the `RandomKField` object `K` must be passed as a way of indirectly accessing the `DomainData` grid dimension parameters. 


## Usage 
The package is imported into your Python namespace by the command: `import periodicgw`

The example code below demonstrates how to generate a random, periodic, locally Gaussian conductivity field with user-selectable semi-variograms and anisotropy structures and solve the steady-state groundwater flow equation on a previously saved conductivity field. Note that the defined correlation length in both the major- and minor- direction should be larger than the grid cell size.

	from numpy import pi
	from pickle import dump, load
	from periodicgw import DomainData, RandomKField, solve_q, plot_lognormal_field, plot_quiver

	# Generate a random, periodic, log-normal conductivity field locally Gaussian semi-variogram
	dd = DomainData(nr=50, nc=100, dr=2, dc=2)
	K = RandomKField(dd, model_ref=2, var=.5, corr_len=dd.num_cols*dd.dc/20, f_lambda=.5, azimuth=0*pi/2)
	plot_lognormal_field(K)
	with open('k_field_test.pickle',"wb") as dump_file:
		dump(K, dump_file)

	# Read the previously saved conductivity field with exponential covariance
	with open("k_field_test.pickle", "rb") as read_file:
		saved_K = load(read_file)

	# Compute the periodic Darcy flow field resulting from enforcing mean flow in the +c (x-axis) direction          
	q_r, q_c = solve_q(saved_K, angle=0)
	plot_quiver(saved_K, q_r, q_c) 