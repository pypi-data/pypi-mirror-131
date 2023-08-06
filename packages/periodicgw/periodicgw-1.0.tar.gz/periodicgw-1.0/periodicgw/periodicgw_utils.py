'''
periodic_gw_utils.py

API
>Classes
    DomainData -- contains number and size of cells, axes
    RandomKField -- generates and stores stats of lognormal K field
    SparseBag -- convenience class for generatig CSR sparse matrices

>Functions
    solve_q(RandomKField K, float angle)
        generates q_r and q_c: matrices of r-axis and c-axis Darcy fluxes for each
        cell, given the flux angle (above the c-axis) at cell 0,0
    plot_lognormal_field(RandomKField K)
        Generates a pseudocolor plot  of a lognormal K field  
    plot_quiver(RandomKField K, array qr, array qc)
        Generates a quiver plot of interpolated caeel-centre velocities

SUMMARY
Solves the steady-stake groundwater flow equation on a random heterogeneous conductivity
field, with periodic boundary conditions in both directions. Solution is finite volume,
and formulated directly for the interfacial fluxes rather than for heads. 

Refactors 2D_periodic_q_solve.py as classes/functions, without using global variables, 
adds a high-level function to generate a velocity field with arbitrary flow angle. Uses
sparse matrix solvers; 1M element domains are no problem.

COORDINATE SYSTEMS
We use a rectangular structured grid with the coordinates r ("row") and c ("column"),
where these increment the same way as coordinates in a matrix:

|  M(0,0)  M(0,1) ... M(0,c) ... |
|  M(1,0)  M(1,1) ...            |
|  ...                M(r,c) ... |

r is the 0-based row index 
    for interacting with external codes, increasing r corresponds to increasing y
c is the 0-based column index 
    for interacting with external codes, increasing c corresponds to increasing x

Each cell has the same dimeisnions, dd.dr in the r-direction, and dd.dc in the c-direction.

SOLUTION METHOD
Under fully periodic BCs, each cell may be uniquely associated with two interfacial fluxes:
the outward-directed fluxes in the +r and +c directions. We DEFINE
    q_r(r,c) as the outward interfacial flux in the +r direction originating at cell (r,c)
    q_c(r,c) as the outward interfacial flux in the +c direction originating at cell (r,c)

Solving for the fluxes directly means that if there are N cells, there are 2*N unknowns, 
so 2*N linearly independent equations are required for solution.

For each cell, we can write two equations
1) Mass balance: inflows must equal outflows for every cell, so
    dd.dc*q_r(r-1,c) - dd.dc*q_r(r,c) + dd.dr*q_c(r,c-1) - dd.dr*q_c(r,c) = 0
2) Head consistency: The head change h(r+1,c+1) - h(r,c) is path-independent:
    (h(r+1,c+1) - h(r+1,c))  + (h(r+1,c) - h(r,c))  = (h(r+1,c+1) - h(r,c+1))  + (h(r,c+1) - h(r,c))
    OR
    dd.dc*q_c(r+1,c)/k_c(r+1,c) + dd.dr*q_r(r,c)/k_r(r,c) = dd.dr*q_r(r,c+1)/k_r(r,c+1) + dd.dc*q_c(r,c)/k_c(r,c)

We wish to solve a matrix equation A q = b, where q is the 2N-vector of fluxes q_r and q_c.
However, the naive 2N x 2N matrix encoding the 2 equations for each of the N cells shown
above has rank 2N - 2; we need to specify two fluxes explicitly (otherwise the trivial, 
zero-flux sol'n is possible).

We remove the mass-balance and head-consistency equations for cell (0,0), instead writing:
    q_r(0,0) = q_r0
    q_c(0,0) = q_c0
for some constants q_r0 and q_c0
'''

from numpy import arange, cos, mean, pi, power, reshape, roll, sin, sqrt, zeros, ones, shape, int32, linspace, random, meshgrid, flipud, exp, real, log10
import matplotlib.pyplot as mpl
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
from scipy.fft import fft2, ifft2

class DomainData:
    def __init__(self, nr=40, nc=25, dr=1.25, dc=1):
        self.num_cols = nc
        self.num_rows = nr

        self.a_dim = 2*nr*nc

        self.dc = dc
        self.dr = dr

        self.v_c = dc*(0.5 + arange(nc))
        self.v_r = dr*(0.5 + arange(nr))

class RandomKField:
    def __init__( self, dd, model_ref, var, corr_len, f_lambda, azimuth):
        self.dd = dd
        self.Lr = dd.num_rows*dd.dr  # Lr = The domain length in the r-axis
        self.Lc = dd.num_cols*dd.dc  # Lc = The domain length in the c-axis
        self.num_rows = dd.num_rows
        self.num_cols = dd.num_cols
        self.step_size_r = dd.dr
        self.step_size_c = dd.dc
        self.model_ref = str(model_ref)   # model_ref: the reference number of the covariance model: exponential=1 or Gaussian =2
        self.var = var                    # var: the log-variance of the field
        self.corr_len = corr_len          # corr_len: correlation length in main direction
        self.f_lambda = f_lambda          # f_lambda: anisotropic factor: the ratio of the minor range to the major range of anisotropy.
        self.azimuth = azimuth            # azimuth: the azimuth angle of the major axis of anisotropy above the c-axis (x-axis), measured in degrees counterclockwise from the c-axis (x-axis))
        self.Field()
   
    # Define discrete Fourier transform tools
    @staticmethod
    def x2k(x): # transform x (space domain) to k (Fourier domian), f(x), f'(k)
        N = shape(x)[0] 
        dx = x[1]-x[0]
        dk = 2*pi/(N*dx)
        inull = int32(N/2)
        k = dk*(linspace(1,N,N)-inull)
        return k
       
    def k2x(k): # transform k (Fourier domian) to x (space domain)
        N = shape(k)[0]
        dk = k[1]-k[0]
        dx = 2*pi/(N*dk)
        x = dx*(linspace(1,N,N)-1)
        return x
    
    # Forward Fourier transform of a function
    def deff2(x, y, f):
        Nx = shape(x)[0]
        Ny = shape(y)[0]
        k=RandomKField.x2k(x)
        m=RandomKField.x2k(y)
        Periodx= Nx*(x[1]-x[0])
        Periody= Ny*(y[1]-y[0])
        inull= int32(Nx/2)
        jnull= int32(Ny/2)
        ft= (Periodx/Nx)*(Periody/Ny)*roll(fft2(f),(inull-1,jnull-1))
        return ft
    
    # Generation of the Fourier transform of a complex 2-D Gaussian random field
    def grf2(k, m, C):
        Nx = shape(k)[0]
        Ny = shape(m)[0]
        dk = k[1]-k[0]
        dm = m[1]-m[0]
        Periodx= 2*pi/dk
        Periody= 2*pi/dm 
        A=random.randn(Ny,Nx)
        B=random.randn(Ny,Nx)
        phi= sqrt(Periodx*Periody*C/2)*(A+B*1.j)
        return phi

    # Inverse Fourier transform of a function
    def deiff2(k, m, ft):
        Nx = shape(k)[0]
        Ny = shape(m)[0]
        x=RandomKField.k2x(k)
        y=RandomKField.k2x(m)
        Periodx= Nx*(x[1]-x[0])
        Periody= Ny*(y[1]-y[0])
        inull= int32(Nx/2)
        jnull= int32(Ny/2)
        f = (Nx/Periodx)*(Ny/Periody)*ifft2(roll(ft,(-inull+1,-jnull+1)))
        return [k, m, f]  
    
    def Field(self):
        # Discretization of the spatial domain        
        c_axis = arange(0.5*self.step_size_c, self.Lc, self.step_size_c)
        r_axis = arange(0.5*self.step_size_r, self.Lr, self.step_size_r)
        self.cols, self.rows = meshgrid(c_axis, r_axis)
        self.rows = flipud(self.rows)
        
        nc = shape(self.cols)[1]
        nr = shape(self.cols)[0]

        # Shift the spatial grid to make it symmetrical
        c_shift = arange(0.5*self.step_size_c, self.Lc, self.step_size_c)-self.Lc/2
        r_shift = arange(0.5*self.step_size_r, self.Lr, self.step_size_r)-self.Lr/2
        
        len_phi = self.corr_len                 # Correlation length in main-direction (Phi)
        len_theta = self.corr_len*self.f_lambda # Correlation length in minor-direction (Theta)
        angle = self.azimuth                    # The azimuth angle of the direction of maximum continuity
        
        # Calculate the covariance function (exponental or Gaussian covariance) on the spatial grid
        Cmtx= ones((nr,nc))   # Calculate the spatial covariance function
        if self.model_ref == '1': # exponential covariance
            for i in range(0,nr):
                for j in range(0,nc):
                        Cmtx[i,j] = self.var*exp(-sqrt((cos(angle)*c_shift[j] - sin(angle)*r_shift[i])**2/len_phi**2+\
                                                    (sin(angle)*c_shift[j] + cos(angle)*r_shift[i])**2/len_theta**2))
                            
        if self.model_ref == '2': # Gaussian covariance
            for i in range(0,nr):
                for j in range(0,nc):
                        Cmtx[i,j] = self.var*exp(-(cos(angle)*c_shift[j] - sin(angle)*r_shift[i])**2/len_phi**2-\
                                                    (sin(angle)*c_shift[j] + cos(angle)*r_shift[i])**2/len_theta**2)
        
        # Fourier transform of the generated covariance fucntion
        FT_C = RandomKField.deff2(c_shift, r_shift, Cmtx) 
        
        # Generate Fourier transform of a complex 2-D Gaussian random field with covariance function 2*Cmtx
        k = RandomKField.x2k(c_shift)
        m = RandomKField.x2k(r_shift)
        FT_complex_phi = RandomKField.grf2(k, m, 2*FT_C)
        
        # Generate a real-valued 2-D Gaussian random field with covariance function Cmtx
        [xx,yy,phi] = RandomKField.deiff2(k, m, FT_complex_phi)
        log10_K= real(phi)
        
        # Generate a conductivity K field
        idx_r = shape(log10_K)[0]
        idx_c = shape(log10_K)[1]
        self.K = zeros((idx_r, idx_c))
        for i in range(0,idx_r):
            for j in range(0,idx_c):
               self.K[i,j]= power(10,log10_K[i,j])

    # Return the harmonic mean hydraulic conductivity for flow from one cell to its neighbour
    def k_bar(self, r, c, dir):
        if dir == 'r':
            return 2/(1/self.K[r%self.num_rows, c%self.num_cols] +\
                 1/self.K[(r+1)%self.num_rows, c%self.num_cols])

        else:
            return 2/(1/self.K[r%self.num_rows, c%self.num_cols] +\
                 1/self.K[r%self.num_rows, (c+1)%self.num_cols])
        


class SparseBag:
    def __init__(self, size):
        self.size = size
        self.row_coords = zeros(size)
        self.col_coords = zeros(size)
        self.data = zeros(size)
        self.ptr = 0

    def stow(self, r, c, d):
        if self.ptr >= self.size:
            raise Exception("Bag is full.")
        self.row_coords[self.ptr] = r
        self.col_coords[self.ptr] = c
        self.data[self.ptr] = d
        self.ptr += 1

def solve_q(K, angle):
    b = zeros(K.dd.a_dim)
    bag = SparseBag(K.dd.a_dim*5 - 8) 

    #CONVERSION FUNCTIONS FROM (r,c) COORDINATES TO MATRIX INDICES
    def idx_q(r, c, dir):
        '''returns the index in the q-vector corresponding to OUTWARD flux in direction 'dir' originating at node (r,c) '''
        r %= K.dd.num_rows
        c %= K.dd.num_cols
        offset = 0 if dir == 'r' else K.dd.num_cols*K.dd.num_rows
        return offset + r*K.dd.num_cols + c

    def row_idx_A(r, c, mode):
        '''returns row of A matrix for the equation based at node (i,j):
            mode = 'mb' -> the mass balance equation
            mode = 'dh' -> the two different head pathways
        '''
        return idx_q(r, c, 'r') if mode == 'mb' else idx_q(r, c, 'c')

    for r in range(K.dd.num_rows):
        for c in range(K.dd.num_cols):
            
            r_A = row_idx_A(r, c, 'mb')
            if r == 0 and c == 0:
                #special case: encode average velocity in 'r' direction instead of mass 
                # balance at cell (0,0)
                for rr in range(K.dd.num_rows):
                    for cc in range(K.dd.num_cols):
                        bag.stow(r_A, idx_q(rr, cc, 'r'), 2/K.dd.a_dim)
                b[r_A] = sin(angle)
            else:
                #encode mass balance equation at cell (r,c)
                bag.stow(r_A, idx_q(r-1 , c   , 'r'), K.dd.dc)
                bag.stow(r_A, idx_q(r   , c   , 'r'), -K.dd.dc)
                bag.stow(r_A, idx_q(r   , c-1 , 'c'), K.dd.dr)
                bag.stow(r_A, idx_q(r   , c   , 'c'), -K.dd.dr)

            #encode head delta equation
            r_A = row_idx_A(r, c, 'dh')
            if r == 0 and c == 0:
                #special case: encode average velocity in 'c' direction
                for rr in range(K.dd.num_rows):
                    for cc in range(K.dd.num_cols):
                        bag.stow(r_A, idx_q(rr, cc, 'c'), 2/K.dd.a_dim)
                b[r_A] = cos(angle)
            else:
                bag.stow(r_A, idx_q(r   , c   , 'c'),  K.dd.dc/K.k_bar(r   , c   , 'c'))
                bag.stow(r_A, idx_q(r   , c+1 , 'r'),  K.dd.dr/K.k_bar(r   , c+1 , 'r'))
                bag.stow(r_A, idx_q(r   , c   , 'r'), -K.dd.dr/K.k_bar(r   , c   , 'r'))
                bag.stow(r_A, idx_q(r+1 , c   , 'c'), -K.dd.dc/K.k_bar(r+1 , c   , 'c'))

    A = csr_matrix((bag.data,(bag.row_coords,bag.col_coords)), shape=(K.dd.a_dim,K.dd.a_dim))
    q = spsolve(A,b)

    q_r = reshape(q[:int(len(q)/2)],(K.dd.num_rows,K.dd.num_cols))
    q_c = reshape(q[int(len(q)/2):],(K.dd.num_rows,K.dd.num_cols))

    mag = sqrt(mean(q_r)**2 + mean(q_c)**2)
    return q_r/mag, q_c/mag

def plot_lognormal_field(K):
    fig, ax = mpl.subplots()
    f = ax.pcolormesh(K.cols, K.rows, log10(K.K), shading='gouraud', cmap='jet')
    fig.colorbar(f, ax=ax, shrink=0.5)
    mpl.xlim((0, K.Lc))
    mpl.ylim((0, K.Lr))
    ax.set_aspect('equal')
    ax.set_title("Log hydraulic conductivity field")
    ax.set_xlabel("x (column)")
    ax.set_ylabel("y (row)")
    mpl.show()

def plot_quiver(K, q_r, q_c):
    q_r_centre = 0.5*(q_r + roll(q_r, 1, axis=0))
    q_c_centre = 0.5*(q_c + roll(q_c, 1, axis=1))

    _, ax = mpl.subplots()
    
    ax.quiver(K.dd.v_c, K.dd.v_r, q_c_centre, q_r_centre)
    ax.set_aspect('equal')
    ax.set_title("Darcy flux field")
    ax.set_xlabel("x (column)")
    ax.set_ylabel("y (row)")
    mpl.show()

if __name__ == '__main__':
    dd = DomainData(nr=50, nc=100, dr=2, dc=2)
    K = RandomKField(dd, model_ref=2, var=.5, corr_len=(dd.num_cols*dd.dc/20),f_lambda=0.5, azimuth=0*pi/2)
    plot_lognormal_field(K)
    q_r, q_c = solve_q(K, 0)
    plot_quiver(K, q_r, q_c)
