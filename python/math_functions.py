import numpy as np
import scipy.special as sp
from scipy.integrate import odeint
from scipy.special import fresnel
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Surfaces:
    """
    Contains broader classes of standard 3D mathematical surfaces mapped over a Cartesian grid. 
    These surfaces typically define z as a function of x and y (z = f(x, y))[cite: 1, 4].
    """

    @staticmethod
    def sinc(x_min=-10, x_max=10, y_min=-10, y_max=10, step=0.4):
        """
        Plots the Sinc function (z = sin(R)/R where R = sqrt(x^2 + y^2))[cite: 1, 4].
        This surface resembles a mathematical raindrop forming perfectly decaying concentric ripples[cite: 1, 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -10)[cite: 1, 4].
            x_max (float): Maximum x-coordinate (default 10)[cite: 1, 4].
            y_min (float): Minimum y-coordinate (default -10)[cite: 1, 4].
            y_max (float): Maximum y-coordinate (default 10)[cite: 1, 4].
            step (float): Grid resolution step size (default 0.4)[cite: 1, 4].
        
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Sinc function[cite: 1].

        Real-Life Examples:
            1. Signal Processing: Represents the ideal interpolation filter in the time and frequency domains[cite: 1, 4].
            2. Optics: Models the diffraction pattern (Airy disk) of a circular aperture[cite: 1].
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        R = np.hypot(X, Y) + 1e-4
        Z = np.sin(R) / R
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='cyan', edgecolor='none', alpha=0.9)
        ax.set_title('The Sinc Function')
        return fig

    @staticmethod
    def saddle(x_min=-5, x_max=5, y_min=-5, y_max=5, step=0.2):
        """
        Plots a Hyperbolic Paraboloid (z = x^2 - y^2), commonly known as a saddle point[cite: 1, 4].
        It curves up in one direction and down in the other[cite: 1, 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -5)[cite: 1, 4].
            x_max (float): Maximum x-coordinate (default 5)[cite: 1, 4].
            y_min (float): Minimum y-coordinate (default -5)[cite: 1, 4].
            y_max (float): Maximum y-coordinate (default 5)[cite: 1, 4].
            step (float): Grid resolution step size (default 0.2)[cite: 1, 4].
        
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Saddle point[cite: 1].

        Real-Life Examples:
            1. Machine Learning: Represents flat saddle points where optimizers can stall during gradient descent[cite: 1, 4].
            2. Architecture: Used in saddle-roof constructions (like the Calgary Saddledome) for structural stability[cite: 1].
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        Z = X**2 - Y**2
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='plasma', edgecolor='none')
        ax.set_title('Hyperbolic Paraboloid (Saddle)')
        return fig

    @staticmethod
    def monkey(x_min=-2, x_max=2, y_min=-2, y_max=2, step=0.08):
        """
        Plots a Monkey Saddle (z = x^3 - 3xy^2)[cite: 4].
        A saddle with three descents instead of two, providing enough room for a monkey's legs and tail[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -2)[cite: 4].
            x_max (float): Maximum x-coordinate (default 2)[cite: 4].
            y_min (float): Minimum y-coordinate (default -2)[cite: 4].
            y_max (float): Maximum y-coordinate (default 2)[cite: 4].
            step (float): Grid resolution step size (default 0.08)[cite: 4].
        
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Monkey Saddle[cite: 1].

        Real-Life Examples:
            1. Differential Geometry: Used to study surfaces with negative Gaussian curvature and complex stationary points.
            2. Engineering: Structural shells and blending surfaces often rely on multi-descent saddle topographies.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        Z = X**3 - 3 * X * Y**2
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='coolwarm', edgecolor='none')
        ax.set_title('Monkey Saddle')
        return fig

    @staticmethod
    def dropwave(x_min=-5.12, x_max=5.12, y_min=-5.12, y_max=5.12, step=0.15):
        """
        Plots the Drop-Wave Function (f = -(1 + cos(12*sqrt(x^2 + y^2))) / (0.5*(x^2 + y^2) + 2))[cite: 4].
        Resembles the splash of a water drop; it is highly multimodal and symmetrical, serving as a good stress test for optimizers[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -5.12)[cite: 4].
            x_max (float): Maximum x-coordinate (default 5.12)[cite: 4].
            y_min (float): Minimum y-coordinate (default -5.12)[cite: 4].
            y_max (float): Maximum y-coordinate (default 5.12)[cite: 4].
            step (float): Grid resolution step size (default 0.15)[cite: 4].
        
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Drop-Wave function[cite: 1].

        Real-Life Examples:
            1. Optimization: Benchmarking global optimization algorithms (e.g., genetic algorithms) due to its many local minima.
            2. Fluid Dynamics: Approximates the physical ripple pattern created by a droplet hitting a liquid surface.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        R2 = X**2 + Y**2
        Z = -(1 + np.cos(12 * np.sqrt(R2))) / (0.5 * R2 + 2)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='ocean', edgecolor='none')
        ax.set_title('Drop-Wave Function')
        return fig

    @staticmethod
    def eggcarton(x_min=-10, x_max=10, y_min=-10, y_max=10, step=0.3):
        """
        Plots the Egg Carton Surface (z = sin(x)*cos(y))[cite: 4].
        Forms a repeating lattice of peaks and pits, representing a 2D standing-wave interference pattern[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -10)[cite: 4].
            x_max (float): Maximum x-coordinate (default 10)[cite: 4].
            y_min (float): Minimum y-coordinate (default -10)[cite: 4].
            y_max (float): Maximum y-coordinate (default 10)[cite: 4].
            step (float): Grid resolution step size (default 0.3)[cite: 4].
        
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Egg Carton surface[cite: 1].

        Real-Life Examples:
            1. Acoustics: Visually models 2D standing-wave interference patterns[cite: 4].
            2. Packaging: The structural basis for shock-absorbing egg cartons and soundproofing foam profiles.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='terrain', edgecolor='none')
        ax.set_title('Egg Carton Surface')
        return fig


class Distributions:
    """
    Contains 2D continuous probability distributions and density functions extended into 3D.
    The z-axis represents the probability density function (PDF) f(x, y)[cite: 1, 4].
    """

    @staticmethod
    def gaussian(x_min=-6, x_max=6, y_min=-6, y_max=6, step=0.25):
        """
        Plots a Bivariate Gaussian distribution.
        The bell curve extended into 3D, a foundation of statistics that appears everywhere from quantum mechanics to populations[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -6)[cite: 4].
            x_max (float): Maximum x-coordinate (default 6)[cite: 4].
            y_min (float): Minimum y-coordinate (default -6)[cite: 4].
            y_max (float): Maximum y-coordinate (default 6)[cite: 4].
            step (float): Grid resolution step size (default 0.25)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Bivariate Gaussian.

        Real-Life Examples:
            1. Statistics: The foundation for tracking naturally occurring phenomena like population heights and test scores[cite: 4].
            2. Quantum Mechanics: Used to describe wave packets representing particle positions[cite: 4].
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-(X**2 + Y**2) / 8) / (8 * np.pi)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Bivariate Gaussian')
        return fig

    @staticmethod
    def corrnormal(x_min=-3.5, x_max=3.5, y_min=-3.5, y_max=3.5, step=0.1):
        """
        Plots a Correlated Normal distribution (ρ = 0.8)[cite: 4].
        Strong positive correlation squeezes the bell into a long ridge along the diagonal[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -3.5)[cite: 4].
            x_max (float): Maximum x-coordinate (default 3.5)[cite: 4].
            y_min (float): Minimum y-coordinate (default -3.5)[cite: 4].
            y_max (float): Maximum y-coordinate (default 3.5)[cite: 4].
            step (float): Grid resolution step size (default 0.1)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Correlated Normal.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-(X**2 - 1.6 * X * Y + Y**2) / 0.72) / (2 * np.pi * 0.6)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='plasma', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Correlated Normal (ρ = 0.8)')
        return fig

    @staticmethod
    def gmm(x_min=-5, x_max=5, y_min=-5, y_max=5, step=0.12):
        """
        Plots a Gaussian Mixture Model[cite: 4].
        Three weighted Gaussians: the standard model for clustered data and the engine behind soft clustering[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -5)[cite: 4].
            x_max (float): Maximum x-coordinate (default 5)[cite: 4].
            y_min (float): Minimum y-coordinate (default -5)[cite: 4].
            y_max (float): Maximum y-coordinate (default 5)[cite: 4].
            step (float): Grid resolution step size (default 0.12)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Gaussian Mixture.
        """
        def _gauss2(x_val, y_val, mx, my, s):
            return np.exp(-((x_val - mx)**2 + (y_val - my)**2) / (2 * s**2)) / (2 * np.pi * s**2)

        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        Z = 0.35 * _gauss2(X, Y, -2, -2, 0.8) + \
            0.4 * _gauss2(X, Y, 2, 1.5, 1) + \
            0.25 * _gauss2(X, Y, -1, 2.5, 0.7)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        # 'Portland' closest matplotlib equivalent can vary, using 'coolwarm'
        ax.plot_surface(X, Y, Z, cmap='coolwarm', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Gaussian Mixture')
        return fig

    @staticmethod
    def skewnormal(x_min=-4, x_max=4, y_min=-4, y_max=4, step=0.1):
        """
        Plots a Bivariate Skew-Normal distribution[cite: 4].
        A Gaussian tilted by its own CDF: one flank is steep, the other trails off in a long shoulder[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -4)[cite: 4].
            x_max (float): Maximum x-coordinate (default 4)[cite: 4].
            y_min (float): Minimum y-coordinate (default -4)[cite: 4].
            y_max (float): Maximum y-coordinate (default 4)[cite: 4].
            step (float): Grid resolution step size (default 0.1)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Bivariate Skew-Normal.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        # Phi(x) = 0.5 * (1 + erf(x / sqrt(2)))
        phi_term = 0.5 * (1 + sp.erf((3 * X + Y) / np.sqrt(2)))
        Z = np.exp(-(X**2 + Y**2) / 2) / np.pi * phi_term
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Bivariate Skew-Normal')
        return fig

    @staticmethod
    def student2d(x_min=-6, x_max=6, y_min=-6, y_max=6, step=0.15):
        """
        Plots a Bivariate Student's t distribution (ν = 3)[cite: 4].
        A sharper peak than the Gaussian with heavy tails, so extreme values are far more likely[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -6)[cite: 4].
            x_max (float): Maximum x-coordinate (default 6)[cite: 4].
            y_min (float): Minimum y-coordinate (default -6)[cite: 4].
            y_max (float): Maximum y-coordinate (default 6)[cite: 4].
            step (float): Grid resolution step size (default 0.15)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Bivariate Student's t.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        coef = np.exp(sp.gammaln(2.5) - sp.gammaln(1.5)) / (3 * np.pi)
        Z = coef * (1 + (X**2 + Y**2) / 3)**(-2.5)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='magma', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title("Bivariate Student's t (ν = 3)")
        return fig

    @staticmethod
    def cauchy2d(x_min=-6, x_max=6, y_min=-6, y_max=6, step=0.15):
        """
        Plots a Bivariate Cauchy distribution[cite: 4].
        So heavy-tailed that its mean and variance do not exist. Outliers are part of the shape[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -6)[cite: 4].
            x_max (float): Maximum x-coordinate (default 6)[cite: 4].
            y_min (float): Minimum y-coordinate (default -6)[cite: 4].
            y_max (float): Maximum y-coordinate (default 6)[cite: 4].
            step (float): Grid resolution step size (default 0.15)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Bivariate Cauchy.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        Z = (1 + X**2 + Y**2)**(-1.5) / (2 * np.pi)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        # Matplotlib doesn't have 'Electric', using 'hsv' or 'jet' as high-contrast
        ax.plot_surface(X, Y, Z, cmap='hsv', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Bivariate Cauchy')
        return fig

    @staticmethod
    def laplace2d(x_min=-6, x_max=6, y_min=-6, y_max=6, step=0.15):
        """
        Plots a Bivariate Laplace distribution[cite: 4].
        Two independent double exponentials form a pyramid with a sharp peak and diamond-shaped contours[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -6)[cite: 4].
            x_max (float): Maximum x-coordinate (default 6)[cite: 4].
            y_min (float): Minimum y-coordinate (default -6)[cite: 4].
            y_max (float): Maximum y-coordinate (default 6)[cite: 4].
            step (float): Grid resolution step size (default 0.15)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Bivariate Laplace.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-(np.abs(X) + np.abs(Y))) / 4
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='inferno', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Bivariate Laplace')
        return fig

    @staticmethod
    def logistic2d(x_min=-6, x_max=6, y_min=-6, y_max=6, step=0.2):
        """
        Plots a Bivariate Logistic (Gumbel) distribution[cite: 4].
        A skewed, bulky peak with exponential tails, from Gumbel's bivariate logistic family[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -6)[cite: 4].
            x_max (float): Maximum x-coordinate (default 6)[cite: 4].
            y_min (float): Minimum y-coordinate (default -6)[cite: 4].
            y_max (float): Maximum y-coordinate (default 6)[cite: 4].
            step (float): Grid resolution step size (default 0.2)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Bivariate Logistic.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        Z = 2 * np.exp(-X - Y) / (1 + np.exp(-X) + np.exp(-Y))**3
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='jet', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Bivariate Logistic (Gumbel)')
        return fig

    @staticmethod
    def lognormal2d(x_min=0.03, x_max=4, y_min=0.03, y_max=4, step=0.08):
        """
        Plots a Bivariate Log-Normal distribution[cite: 4].
        Multiplicative effects pile up on a log scale: a hump against the axes with a long right-hand tail[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default 0.03)[cite: 4].
            x_max (float): Maximum x-coordinate (default 4)[cite: 4].
            y_min (float): Minimum y-coordinate (default 0.03)[cite: 4].
            y_max (float): Maximum y-coordinate (default 4)[cite: 4].
            step (float): Grid resolution step size (default 0.08)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Bivariate Log-Normal.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-(np.log(X)**2 + np.log(Y)**2) / 0.72) / (2 * np.pi * 0.36 * X * Y)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='terrain', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Bivariate Log-Normal')
        return fig

    @staticmethod
    def normalgamma(m_min=-3, m_max=3, m_step=0.08, t_min=0, t_max=4, t_step=0.06):
        """
        Plots a Normal-Gamma distribution[cite: 4].
        A Bayesian prior over a mean μ and a precision τ. Notice how the spread in μ narrows as τ grows[cite: 4].

        Inputs:
            m_min (float): Minimum μ-coordinate (default -3)[cite: 4].
            m_max (float): Maximum μ-coordinate (default 3)[cite: 4].
            m_step (float): μ Grid resolution step size (default 0.08)[cite: 4].
            t_min (float): Minimum τ-coordinate (default 0)[cite: 4].
            t_max (float): Maximum τ-coordinate (default 4)[cite: 4].
            t_step (float): τ Grid resolution step size (default 0.06)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Normal-Gamma distribution.
        """
        m = np.arange(m_min, m_max, m_step)
        t = np.arange(t_min, t_max, t_step)
        M, T = np.meshgrid(m, t)
        Z = 0.3989 * T**1.5 * np.exp(-T - T * M**2 / 2)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(M, T, Z, cmap='plasma', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Normal-Gamma')
        return fig

    @staticmethod
    def dirichlet(x_min=0, x_max=1, y_min=0, y_max=1, step=0.02):
        """
        Plots a Dirichlet distribution (α = 3, 5, 4)[cite: 4].
        A distribution over probabilities that sum to 1. The base is the triangle of all possible three-way splits, shown here in (p₁, p₂)[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default 0)[cite: 4].
            x_max (float): Maximum x-coordinate (default 1)[cite: 4].
            y_min (float): Minimum y-coordinate (default 0)[cite: 4].
            y_max (float): Maximum y-coordinate (default 1)[cite: 4].
            step (float): Grid resolution step size (default 0.02)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Dirichlet distribution.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        P = 1 - X - Y
        
        Z = 138600 * X**2 * Y**4 * np.maximum(P, 0)**3
        Z[P < -1e-9] = np.nan
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Dirichlet (α = 3, 5, 4)')
        return fig

    @staticmethod
    def vonmises(x_min=-np.pi, x_max=np.pi, y_min=-np.pi, y_max=np.pi, step=0.1):
        """
        Plots a Bivariate von Mises distribution (torus)[cite: 4].
        A distribution over two angles, where the edges wrap around. It is used for protein backbone angles[cite: 4]. Shown unnormalized[cite: 4].

        Inputs:
            x_min (float): Minimum angle x (default -π)[cite: 4].
            x_max (float): Maximum angle x (default π)[cite: 4].
            y_min (float): Minimum angle y (default -π)[cite: 4].
            y_max (float): Maximum angle y (default π)[cite: 4].
            step (float): Grid resolution step size (default 0.1)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Bivariate von Mises.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(2 * np.cos(X) + 2 * np.cos(Y) + 1.5 * np.sin(X) * np.sin(Y))
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='coolwarm', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Bivariate von Mises (torus)')
        return fig

    @staticmethod
    def clayton(u_min=0.03, u_max=1, v_min=0.03, v_max=1, step=0.02):
        """
        Plots a Clayton Copula Density (θ = 2)[cite: 4].
        Models dependence with no marginals attached: strong lower-tail dependence, so variables crash together[cite: 4]. Capped at 20[cite: 4].

        Inputs:
            u_min (float): Minimum u-coordinate (default 0.03)[cite: 4].
            u_max (float): Maximum u-coordinate (default 1)[cite: 4].
            v_min (float): Minimum v-coordinate (default 0.03)[cite: 4].
            v_max (float): Maximum v-coordinate (default 1)[cite: 4].
            step (float): Grid resolution step size (default 0.02)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Clayton Copula.
        """
        u = np.arange(u_min, u_max, step)
        v = np.arange(v_min, v_max, step)
        U, V = np.meshgrid(u, v)
        Z = np.minimum(20, 3 * (U * V)**(-3) * (U**(-2) + V**(-2) - 1)**(-2.5))
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(U, V, Z, cmap='magma', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Clayton Copula Density (θ = 2)')
        return fig

    @staticmethod
    def banana(x_min=-5, x_max=5, x_step=0.1, y_min=-2, y_max=8, y_step=0.12):
        """
        Plots a Banana (Twisted Gaussian) distribution[cite: 4].
        A curved ridge that is a classic hard target for MCMC samplers, which struggle to follow its bend[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -5)[cite: 4].
            x_max (float): Maximum x-coordinate (default 5)[cite: 4].
            x_step (float): Grid resolution step size for x (default 0.1)[cite: 4].
            y_min (float): Minimum y-coordinate (default -2)[cite: 4].
            y_max (float): Maximum y-coordinate (default 8)[cite: 4].
            y_step (float): Grid resolution step size for y (default 0.12)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Banana distribution.
        """
        x = np.arange(x_min, x_max, x_step)
        y = np.arange(y_min, y_max, y_step)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-X**2 / 8 - 2 * (Y - X**2 / 4)**2) / (2 * np.pi)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='jet', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Banana (Twisted Gaussian)')
        return fig

    @staticmethod
    def funnel(x_min=-4, x_max=4, y_min=-4, y_max=4, step=0.08):
        """
        Plots Neal's Funnel distribution[cite: 4].
        The geometry of hierarchical models: wide and gentle at the top, a razor-thin neck at the bottom[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -4)[cite: 4].
            x_max (float): Maximum x-coordinate (default 4)[cite: 4].
            y_min (float): Minimum y-coordinate (default -4)[cite: 4].
            y_max (float): Maximum y-coordinate (default 4)[cite: 4].
            step (float): Grid resolution step size (default 0.08)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of Neal's Funnel.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-Y**2 / 18 - X**2 / (2 * np.exp(Y))) / (3 * 2 * np.pi * np.exp(Y / 2))
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='hsv', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title("Neal's Funnel")
        return fig

    @staticmethod
    def gammafam(x_min=0, x_max=12, x_step=0.15, k_min=1, k_max=9, k_step=0.1):
        """
        Plots the Gamma Family density over (x, shape k)[cite: 4].
        Shape k runs from 1 to 9. At k = 1 it is the exponential, and as k grows it slides right and turns bell-shaped[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default 0)[cite: 4].
            x_max (float): Maximum x-coordinate (default 12)[cite: 4].
            x_step (float): Grid resolution step size for x (default 0.15)[cite: 4].
            k_min (float): Minimum shape parameter k (default 1)[cite: 4].
            k_max (float): Maximum shape parameter k (default 9)[cite: 4].
            k_step (float): Grid resolution step size for k (default 0.1)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Gamma Family.
        """
        x = np.arange(x_min, x_max, x_step)
        k = np.arange(k_min, k_max, k_step)
        X, K = np.meshgrid(x, k)
        Z = np.exp((K - 1) * np.log(np.maximum(X, 1e-9)) - X - sp.gammaln(K))
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, K, Z, cmap='viridis', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Gamma Family (shape k)')
        return fig

    @staticmethod
    def betafam(x_min=0.01, x_max=0.99, x_step=0.01, a_min=1, a_max=8, a_step=0.1):
        """
        Plots the Beta Family density over (x, parameter α) with fixed β = 3[cite: 4].
        The distribution of probabilities themselves. Raising α pushes the mass from the left edge to the right[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default 0.01)[cite: 4].
            x_max (float): Maximum x-coordinate (default 0.99)[cite: 4].
            x_step (float): Grid resolution step size for x (default 0.01)[cite: 4].
            a_min (float): Minimum α parameter (default 1)[cite: 4].
            a_max (float): Maximum α parameter (default 8)[cite: 4].
            a_step (float): Grid resolution step size for α (default 0.1)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Beta Family.
        """
        x = np.arange(x_min, x_max, x_step)
        a = np.arange(a_min, a_max, a_step)
        X, A = np.meshgrid(x, a)
        Z = np.exp((A - 1) * np.log(X) + 2 * np.log(1 - X) - sp.gammaln(A) - sp.gammaln(3) + sp.gammaln(A + 3))
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, A, Z, cmap='plasma', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Beta Family (α, β = 3)')
        return fig

    @staticmethod
    def tfam(x_min=-5, x_max=5, x_step=0.1, v_min=0.5, v_max=30, v_step=0.5):
        """
        Plots the Student's t Family density over (x, degrees of freedom ν)[cite: 4].
        Degrees of freedom ν from 0.5 to 30. Watch the heavy tails thin out as the curve converges on the normal[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default -5)[cite: 4].
            x_max (float): Maximum x-coordinate (default 5)[cite: 4].
            x_step (float): Grid resolution step size for x (default 0.1)[cite: 4].
            v_min (float): Minimum ν parameter (default 0.5)[cite: 4].
            v_max (float): Maximum ν parameter (default 30)[cite: 4].
            v_step (float): Grid resolution step size for ν (default 0.5)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Student's t Family.
        """
        x = np.arange(x_min, x_max, x_step)
        v = np.arange(v_min, v_max, v_step)
        X, V = np.meshgrid(x, v)
        Z = np.exp(sp.gammaln((V + 1) / 2) - sp.gammaln(V / 2)) / np.sqrt(V * np.pi) * (1 + X**2 / V)**(-(V + 1) / 2)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, V, Z, cmap='terrain', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title("Student's t Family (ν)")
        return fig

    @staticmethod
    def chisqfam(x_min=0, x_max=30, x_step=0.4, k_min=2, k_max=14, k_step=0.15):
        """
        Plots the Chi-Squared Family density over (x, degrees of freedom k)[cite: 4].
        Sums of squared normals. More degrees of freedom k shift the mass right and flatten the peak[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default 0)[cite: 4].
            x_max (float): Maximum x-coordinate (default 30)[cite: 4].
            x_step (float): Grid resolution step size for x (default 0.4)[cite: 4].
            k_min (float): Minimum k parameter (default 2)[cite: 4].
            k_max (float): Maximum k parameter (default 14)[cite: 4].
            k_step (float): Grid resolution step size for k (default 0.15)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Chi-Squared Family.
        """
        x = np.arange(x_min, x_max, x_step)
        k = np.arange(k_min, k_max, k_step)
        X, K = np.meshgrid(x, k)
        Z = np.exp((K / 2 - 1) * np.log(np.maximum(X, 1e-9)) - X / 2 - K / 2 * np.log(2) - sp.gammaln(K / 2))
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, K, Z, cmap='coolwarm', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Chi-Squared Family (k)')
        return fig

    @staticmethod
    def weibullfam(x_min=0, x_max=3, x_step=0.04, k_min=1, k_max=6, k_step=0.1):
        """
        Plots the Weibull Family density over (x, shape k)[cite: 4].
        The distribution of lifetimes and failure times. Shape k below 2 means early failures, and above it wear-out[cite: 4].

        Inputs:
            x_min (float): Minimum x-coordinate (default 0)[cite: 4].
            x_max (float): Maximum x-coordinate (default 3)[cite: 4].
            x_step (float): Grid resolution step size for x (default 0.04)[cite: 4].
            k_min (float): Minimum k parameter (default 1)[cite: 4].
            k_max (float): Maximum k parameter (default 6)[cite: 4].
            k_step (float): Grid resolution step size for k (default 0.1)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Weibull Family.
        """
        x = np.arange(x_min, x_max, x_step)
        k = np.arange(k_min, k_max, k_step)
        X, K = np.meshgrid(x, k)
        Z = K * np.maximum(X, 1e-9)**(K - 1) * np.exp(-(X**K))
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, K, Z, cmap='magma', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Weibull Family (shape k)')
        return fig

    @staticmethod
    def poissonfam(k_min=0, k_max=20, k_step=0.25, l_min=0.5, l_max=15, l_step=0.2):
        """
        Plots the Poisson Family density over (count k, rate λ)[cite: 4].
        Counts of rare events. The true distribution lives on whole numbers, so this smooth surface is its continuous extension via Γ[cite: 4].

        Inputs:
            k_min (float): Minimum k-coordinate (default 0)[cite: 4].
            k_max (float): Maximum k-coordinate (default 20)[cite: 4].
            k_step (float): Grid resolution step size for k (default 0.25)[cite: 4].
            l_min (float): Minimum λ parameter (default 0.5)[cite: 4].
            l_max (float): Maximum λ parameter (default 15)[cite: 4].
            l_step (float): Grid resolution step size for λ (default 0.2)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Poisson Family.
        """
        k = np.arange(k_min, k_max, k_step)
        l = np.arange(l_min, l_max, l_step)
        K_grid, L_grid = np.meshgrid(k, l)
        Z = np.exp(K_grid * np.log(L_grid) - L_grid - sp.gammaln(K_grid + 1))
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(K_grid, L_grid, Z, cmap='jet', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Poisson Family (rate λ)')
        return fig


class OptimizationLandscapes:
    """
    Contains multimodal surfaces used primarily as stress tests for optimization algorithms.
    These features global minima hidden among numerous local minima or steep valleys[cite: 5].
    """

    @staticmethod
    def rastrigin(x_min=-5.12, x_max=5.12, y_min=-5.12, y_max=5.12, step=0.15):
        """
        Plots the Rastrigin Function.
        A highly multimodal function with countless local minima hiding a single global minimum at the center[cite: 5].

        Inputs:
            x_min (float): Minimum x-coordinate (default -5.12)[cite: 5].
            x_max (float): Maximum x-coordinate (default 5.12)[cite: 5].
            y_min (float): Minimum y-coordinate (default -5.12)[cite: 5].
            y_max (float): Maximum y-coordinate (default 5.12)[cite: 5].
            step (float): Grid resolution (default 0.15)[cite: 5].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Rastrigin landscape.

        Real-Life Examples:
            1. Algorithm Benchmarking: Used universally to evaluate the convergence speed and robustness of genetic algorithms and swarm intelligence[cite: 5].
            2. Material Science: Simulates energy landscapes of complex atomic crystalline structures[cite: 5].
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        Z = 20 + X**2 - 10 * np.cos(2 * np.pi * X) + Y**2 - 10 * np.cos(2 * np.pi * Y)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='terrain', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Rastrigin Function')
        return fig

    @staticmethod
    def rosenbrock(x_min=-2, x_max=2, x_step=0.1, y_min=-1, y_max=3, y_step=0.1):
        """
        Plots the Rosenbrock Valley function.
        The banana valley: finding the valley is easy, crawling along its flat floor to the minimum is not.

        Inputs:
            x_min (float): Minimum x-coordinate (default -2).
            x_max (float): Maximum x-coordinate (default 2).
            x_step (float): Grid resolution step size for x (default 0.1).
            y_min (float): Minimum y-coordinate (default -1).
            y_max (float): Maximum y-coordinate (default 3).
            y_step (float): Grid resolution step size for y (default 0.1).
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Rosenbrock landscape.
        """
        x = np.arange(x_min, x_max, x_step)
        y = np.arange(y_min, y_max, y_step)
        X, Y = np.meshgrid(x, y)
        Z = (1 - X)**2 + 100 * (Y - X**2)**2
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='magma', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Rosenbrock Valley')
        return fig

    @staticmethod
    def ackley(x_min=-8, x_max=8, y_min=-8, y_max=8, step=0.3):
        """
        Plots the Ackley Function.
        A flat outer region full of shallow ripples that plunges into one deep valley.

        Inputs:
            x_min (float): Minimum x-coordinate (default -8).
            x_max (float): Maximum x-coordinate (default 8).
            y_min (float): Minimum y-coordinate (default -8).
            y_max (float): Maximum y-coordinate (default 8).
            step (float): Grid resolution step size (default 0.3).
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Ackley landscape.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        Z = -20 * np.exp(-0.2 * np.sqrt(0.5 * (X**2 + Y**2))) - np.exp(0.5 * (np.cos(2 * np.pi * X) + np.cos(2 * np.pi * Y))) + np.e + 20
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='coolwarm', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Ackley Function')
        return fig

    @staticmethod
    def himmelblau(x_min=-5, x_max=5, y_min=-5, y_max=5, step=0.2):
        """
        Plots Himmelblau's Function.
        A polynomial landscape with four identical global minima where the surface touches zero.

        Inputs:
            x_min (float): Minimum x-coordinate (default -5).
            x_max (float): Maximum x-coordinate (default 5).
            y_min (float): Minimum y-coordinate (default -5).
            y_max (float): Maximum y-coordinate (default 5).
            step (float): Grid resolution step size (default 0.2).
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Himmelblau landscape.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        Z = (X**2 + Y - 11)**2 + (X + Y**2 - 7)**2
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='hsv', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title("Himmelblau's Function")
        return fig

    @staticmethod
    def beale(x_min=-4.5, x_max=4.5, y_min=-4.5, y_max=4.5, step=0.15):
        """
        Plots the Beale Function.
        Sharp walls with a very flat region near the minimum. Heights are capped so the valley stays visible.

        Inputs:
            x_min (float): Minimum x-coordinate (default -4.5).
            x_max (float): Maximum x-coordinate (default 4.5).
            y_min (float): Minimum y-coordinate (default -4.5).
            y_max (float): Maximum y-coordinate (default 4.5).
            step (float): Grid resolution step size (default 0.15).
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Beale landscape.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        
        Z = (1.5 - X + X * Y)**2 + (2.25 - X + X * Y**2)**2 + (2.625 - X + X * Y**3)**2
        # Capping the height so the valley remains visible
        Z = np.minimum(200, Z)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='jet', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Beale Function')
        return fig

    @staticmethod
    def crossintray(x_min=-10, x_max=10, y_min=-10, y_max=10, step=0.2):
        """
        Plots the Cross-in-Tray Function.
        A canopy-like surface with four identical global minima around its central cross.

        Inputs:
            x_min (float): Minimum x-coordinate (default -10).
            x_max (float): Maximum x-coordinate (default 10).
            y_min (float): Minimum y-coordinate (default -10).
            y_max (float): Maximum y-coordinate (default 10).
            step (float): Grid resolution step size (default 0.2).
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot of the Cross-in-Tray landscape.
        """
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        X, Y = np.meshgrid(x, y)
        
        Z = -1e-4 * (np.abs(np.sin(X) * np.sin(Y) * np.exp(np.abs(100 - np.hypot(X, Y) / np.pi))) + 1)**0.1
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        # Using Spectral to approximate the 'Picnic' colormap
        ax.plot_surface(X, Y, Z, cmap='Spectral', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Cross-in-Tray Function')
        return fig


class ParametricSurfaces:
    """
    Contains 3D manifolds and surfaces generated via parametric equations (u, v) rather than a simple z = f(x,y) grid.
    These allow for complex, self-intersecting, or non-orientable topologies[cite: 4, 5].
    """

    @staticmethod
    def torus(u_steps=60, v_steps=40):
        """
        Plots a Torus, the mathematical donut formed by revolving a circle around an axis in its own plane[cite: 4, 5].

        Inputs:
            u_steps (int): Resolution for the u parameter (default 60)[cite: 4, 5].
            v_steps (int): Resolution for the v parameter (default 40)[cite: 4, 5].
            
        Output:
            matplotlib.figure.Figure: A 3D parametric surface plot of a Torus.

        Real-Life Examples:
            1. Nuclear Physics: The shape of the magnetic confinement chamber in tokamak fusion reactors[cite: 5].
            2. Everyday Objects: Inner tubes, O-rings, and donuts[cite: 5].
        """
        u = np.linspace(0, 2 * np.pi, u_steps)
        v = np.linspace(0, 2 * np.pi, v_steps)
        U, V = np.meshgrid(u, v)
        
        X = (3 + np.cos(V)) * np.cos(U)
        Y = (3 + np.cos(V)) * np.sin(U)
        Z = np.sin(V)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('The Torus')
        return fig

    @staticmethod
    def mobius(u_steps=80, v_steps=20):
        """
        Plots a Möbius Strip. 
        A non-orientable surface with only one side and one edge; tracing its center line visits both "sides" before returning[cite: 4, 5].

        Inputs:
            u_steps (int): Resolution for the angular parameter u (default 80)[cite: 4, 5].
            v_steps (int): Resolution for the width parameter v (default 20)[cite: 4, 5].
            
        Output:
            matplotlib.figure.Figure: A 3D parametric surface plot of a Möbius Strip.

        Real-Life Examples:
            1. Mechanical Engineering: Continuous conveyor belts designed to wear evenly on "both" sides[cite: 5].
            2. Electronics: Möbius resistors that cancel out their own reactive impedance[cite: 5].
        """
        u = np.linspace(0, 2 * np.pi, u_steps)
        v = np.linspace(-1, 1, v_steps)
        U, V = np.meshgrid(u, v)
        
        X = (1 + (V / 2) * np.cos(U / 2)) * np.cos(U)
        Y = (1 + (V / 2) * np.cos(U / 2)) * np.sin(U)
        Z = (V / 2) * np.sin(U / 2)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='plasma', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Möbius Strip')
        return fig

    @staticmethod
    def helicoid(u_steps=40, v_steps=80):
        """
        Plots a Helicoid.
        A spiral staircase that locally minimizes area. Apart from the plane, it is the only ruled minimal surface[cite: 4].

        Inputs:
            u_steps (int): Resolution for the width parameter u (default 40)[cite: 4].
            v_steps (int): Resolution for the angular parameter v (default 80)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D parametric surface plot of a Helicoid.

        Real-Life Examples:
            1. Architecture: The optimal shape for spiral staircases to maximize headroom.
            2. Biology: The geometric structure of certain chiral molecules and tightly packed biological membranes.
        """
        u = np.linspace(-3, 3, u_steps)
        v = np.linspace(-2 * np.pi, 2 * np.pi, v_steps)
        U, V = np.meshgrid(u, v)
        
        X = U * np.cos(V)
        Y = U * np.sin(V)
        Z = 0.5 * V
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='magma', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Helicoid')
        return fig

    @staticmethod
    def catenoid(u_steps=60, v_steps=40):
        """
        Plots a Catenoid.
        Found by Euler in 1744: the shape of a soap film stretched between two rings, and the first non-trivial minimal surface[cite: 4].

        Inputs:
            u_steps (int): Resolution for the angular parameter u (default 60)[cite: 4].
            v_steps (int): Resolution for the height parameter v (default 40)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D parametric surface plot of a Catenoid.

        Real-Life Examples:
            1. Physics: Naturally forms when a soap film bridges two circular wire frames, minimizing surface tension.
            2. Engineering: Used in tension structures and cooling tower designs for structural efficiency.
        """
        u = np.linspace(0, 2 * np.pi, u_steps)
        v = np.linspace(-2, 2, v_steps)
        U, V = np.meshgrid(u, v)
        
        X = np.cosh(V) * np.cos(U)
        Y = np.cosh(V) * np.sin(U)
        Z = V
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='terrain', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Catenoid')
        return fig

    @staticmethod
    def enneper(u_steps=50, v_steps=50):
        """
        Plots the Enneper Surface.
        A self-intersecting minimal surface with elegant symmetry, a staple of differential geometry[cite: 4].

        Inputs:
            u_steps (int): Resolution for the u parameter (default 50)[cite: 4].
            v_steps (int): Resolution for the v parameter (default 50)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D parametric surface plot of the Enneper Surface.

        Real-Life Examples:
            1. Mathematics: Used extensively to study isotropic curves and Weierstrass-Enneper representations.
            2. Material Science: Models complex interfaces in block copolymers and lipid bilayers.
        """
        u = np.linspace(-2, 2, u_steps)
        v = np.linspace(-2, 2, v_steps)
        U, V = np.meshgrid(u, v)
        
        X = U * (1 - U**2 / 3 + V**2) / 3
        Y = -V * (1 - V**2 / 3 + U**2) / 3
        Z = (U**2 - V**2) / 3
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='inferno', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Enneper Surface')
        return fig

    @staticmethod
    def sphere(u_steps=40, v_steps=60):
        """
        Plots a Parametric Sphere.
        The simplest closed 3D manifold, drawn through spherical coordinates[cite: 4].

        Inputs:
            u_steps (int): Resolution for the polar angle u (default 40)[cite: 4].
            v_steps (int): Resolution for the azimuthal angle v (default 60)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D parametric surface plot of a Sphere.

        Real-Life Examples:
            1. Geography/Astronomy: Modeling planetary bodies and celestial navigation spheres.
            2. Computer Graphics: The foundational primitive for rendering environments, bounding volumes, and global illumination.
        """
        u = np.linspace(0, np.pi, u_steps)
        v = np.linspace(0, 2 * np.pi, v_steps)
        U, V = np.meshgrid(u, v)
        
        X = 2 * np.sin(U) * np.cos(V)
        Y = 2 * np.sin(U) * np.sin(V)
        Z = 2 * np.cos(U)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        # Matplotlib equivalent for 'Electric' is 'hsv'
        ax.plot_surface(X, Y, Z, cmap='hsv', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Parametric Sphere')
        return fig

    @staticmethod
    def dini(u_steps=80, v_steps=40):
        """
        Plots Dini's Surface.
        Constant negative curvature in a twisted, spiraling pseudosphere[cite: 4].

        Inputs:
            u_steps (int): Resolution for the u parameter (default 80)[cite: 4].
            v_steps (int): Resolution for the v parameter (default 40)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D parametric surface plot of Dini's Surface.
        """
        u = np.linspace(0, 4 * np.pi, u_steps)
        v = np.linspace(0.01, 2, v_steps)
        U, V = np.meshgrid(u, v)
        
        X = np.cos(U) * np.sin(V)
        Y = np.sin(U) * np.sin(V)
        Z = np.cos(V) + np.log(np.tan(V / 2)) + 0.2 * U
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title("Dini's Surface")
        return fig

    @staticmethod
    def roman(u_steps=60, v_steps=60):
        """
        Plots Steiner's Roman Surface.
        Steiner's 1852 map of the projective plane into 3D, with self-intersections and pinch points[cite: 4].

        Inputs:
            u_steps (int): Resolution for the u parameter (default 60)[cite: 4].
            v_steps (int): Resolution for the v parameter (default 60)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D parametric surface plot of the Roman Surface.
        """
        u = np.linspace(0, np.pi, u_steps)
        v = np.linspace(0, np.pi / 2, v_steps)
        U, V = np.meshgrid(u, v)
        
        X = 4 * np.cos(U) * np.cos(V) * np.sin(V)
        Y = 4 * np.sin(U) * np.cos(V) * np.sin(V)
        Z = 4 * np.cos(U) * np.sin(U) * np.cos(V)**2
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='plasma', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title("Steiner's Roman Surface")
        return fig

    @staticmethod
    def klein(u_steps=60, v_steps=60):
        """
        Plots the Figure-8 Klein Bottle.
        A non-orientable surface with no inside or outside, immersed in 3D as a figure-8[cite: 4].

        Inputs:
            u_steps (int): Resolution for the u parameter (default 60)[cite: 4].
            v_steps (int): Resolution for the v parameter (default 60)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D parametric surface plot of the Klein Bottle.
        """
        u = np.linspace(0, 2 * np.pi, u_steps)
        v = np.linspace(0, 2 * np.pi, v_steps)
        U, V = np.meshgrid(u, v)
        
        C = 2 + np.cos(U / 2) * np.sin(V) - np.sin(U / 2) * np.sin(2 * V)
        X = C * np.cos(U)
        Y = C * np.sin(U)
        Z = np.sin(U / 2) * np.sin(V) + np.cos(U / 2) * np.sin(2 * V)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='magma', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Figure-8 Klein Bottle')
        return fig

    @staticmethod
    def catalan(u_steps=60, v_steps=40):
        """
        Plots Catalan's Surface.
        A periodic minimal surface from 1855 that contains real cycloids[cite: 4].

        Inputs:
            u_steps (int): Resolution for the u parameter (default 60)[cite: 4].
            v_steps (int): Resolution for the v parameter (default 40)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D parametric surface plot of Catalan's Surface.
        """
        u = np.linspace(-np.pi, np.pi, u_steps)
        v = np.linspace(-2, 2, v_steps)
        U, V = np.meshgrid(u, v)
        
        X = U - np.sin(U) * np.cosh(V)
        Y = 1 - np.cos(U) * np.cosh(V)
        Z = 4 * np.sin(U / 2) * np.sinh(V / 2)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='terrain', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title("Catalan's Surface")
        return fig

    @staticmethod
    def seashell(u_steps=50, v_steps=120):
        """
        Plots a Seashell.
        An exponentially growing spiral tube, following the same logarithmic growth law that real mollusks follow[cite: 4].

        Inputs:
            u_steps (int): Resolution for the u parameter (default 50)[cite: 4].
            v_steps (int): Resolution for the v parameter (default 120)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D parametric surface plot of a Seashell.
        """
        u = np.linspace(0, 2 * np.pi, u_steps)
        v = np.linspace(0, 6 * np.pi, v_steps)
        U, V = np.meshgrid(u, v)
        
        E = np.exp(V / (6 * np.pi))
        C = np.cos(U / 2)**2
        
        X = 2 * (1 - E) * np.cos(V) * C
        Y = 2 * (E - 1) * np.sin(V) * C
        Z = 1 - np.exp(V / (3 * np.pi)) - np.sin(U) + E * np.sin(U)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='plasma', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Seashell')
        return fig


class Attractors:
    """
    Contains chaotic dynamical systems and strange attractors generated by integrating 
    ordinary differential equations over time[cite: 4, 6].
    """

    @staticmethod
    def lorenz(steps=8000, dt=0.008, init_state=(0.1, 0, 0)):
        """
        Plots the Lorenz Attractor.
        The blueprint of chaos, born from a model of atmospheric convection and home of the butterfly effect[cite: 4, 6].

        Inputs:
            steps (int): Total integration steps (default 8000)[cite: 4, 6].
            dt (float): Time delta per step (default 0.008)[cite: 4, 6].
            init_state (tuple): Initial (x, y, z) coordinates (default (0.1, 0, 0))[cite: 4, 6].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter/line plot mapping the chaotic trajectory.

        Real-Life Examples:
            1. Meteorology: Demonstrates why long-term weather prediction is impossible due to extreme sensitivity to initial conditions[cite: 6].
            2. Cryptography: Used to generate pseudo-random number sequences for secure communications[cite: 6].
        """
        def deriv(state, t):
            x, y, z = state
            return [10 * (y - x), x * (28 - z) - y, x * y - (8 / 3) * z]

        t = np.arange(0, steps * dt, dt)
        states = odeint(deriv, init_state, t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(states[:,0], states[:,1], states[:,2], 
                   c=states[:,2], cmap='inferno', s=0.5)
        ax.set_title('Lorenz Attractor')
        return fig

    @staticmethod
    def rossler(steps=10000, dt=0.04, init_state=(1, 1, 1)):
        """
        Plots the Rössler Attractor.
        Otto Rössler's 1976 design: as simple as possible while still being chaotic[cite: 4].

        Inputs:
            steps (int): Total integration steps (default 10000)[cite: 4].
            dt (float): Time delta per step (default 0.04)[cite: 4].
            init_state (tuple): Initial (x, y, z) coordinates (default (1, 1, 1))[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot of the Rössler Attractor.
        """
        def deriv(state, t):
            x, y, z = state
            return [-y - z, x + 0.2 * y, 0.2 + z * (x - 5.7)]

        t = np.arange(0, steps * dt, dt)
        states = odeint(deriv, init_state, t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(states[:,0], states[:,1], states[:,2], 
                   c=states[:,2], cmap='terrain', s=0.5)
        ax.set_title('Rössler Attractor')
        return fig

    @staticmethod
    def chen(steps=8000, dt=0.005, init_state=(5, 10, 10)):
        """
        Plots the Chen Attractor.
        Found in 1999, dynamically richer than the Lorenz system despite a similar structure[cite: 4].

        Inputs:
            steps (int): Total integration steps (default 8000)[cite: 4].
            dt (float): Time delta per step (default 0.005)[cite: 4].
            init_state (tuple): Initial (x, y, z) coordinates (default (5, 10, 10))[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot of the Chen Attractor.
        """
        def deriv(state, t):
            x, y, z = state
            return [35 * (y - x), -7 * x - x * z + 28 * y, x * y - 3 * z]

        t = np.arange(0, steps * dt, dt)
        states = odeint(deriv, init_state, t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(states[:,0], states[:,1], states[:,2], 
                   c=states[:,2], cmap='hsv', s=0.5)
        ax.set_title('Chen Attractor')
        return fig

    @staticmethod
    def thomas(steps=15000, dt=0.05, init_state=(1, 1.1, 1)):
        """
        Plots Thomas' Cyclically Symmetric Attractor.
        Cyclic symmetry in three dimensions: instead of two wings it weaves a labyrinthine lattice[cite: 4].

        Inputs:
            steps (int): Total integration steps (default 15000)[cite: 4].
            dt (float): Time delta per step (default 0.05)[cite: 4].
            init_state (tuple): Initial (x, y, z) coordinates (default (1, 1.1, 1))[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot of the Thomas Attractor.
        """
        def deriv(state, t):
            x, y, z = state
            return [np.sin(y) - 0.208186 * x, 
                    np.sin(z) - 0.208186 * y, 
                    np.sin(x) - 0.208186 * z]

        t = np.arange(0, steps * dt, dt)
        states = odeint(deriv, init_state, t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(states[:,0], states[:,1], states[:,2], 
                   c=states[:,2], cmap='Spectral', s=0.5)
        ax.set_title("Thomas' Cyclically Symmetric Attractor")
        return fig

    @staticmethod
    def halvorsen(steps=15000, dt=0.01, init_state=(1, 0, 0)):
        """
        Plots the Halvorsen Attractor.
        Cyclically symmetric trajectories that spin out from the origin and fold back into a flower[cite: 4].

        Inputs:
            steps (int): Total integration steps (default 15000)[cite: 4].
            dt (float): Time delta per step (default 0.01)[cite: 4].
            init_state (tuple): Initial (x, y, z) coordinates (default (1, 0, 0))[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot of the Halvorsen Attractor.
        """
        def deriv(state, t):
            x, y, z = state
            return [-1.89 * x - 4 * y - 4 * z - y**2, 
                    -1.89 * y - 4 * z - 4 * x - z**2, 
                    -1.89 * z - 4 * x - 4 * y - x**2]

        t = np.arange(0, steps * dt, dt)
        states = odeint(deriv, init_state, t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(states[:,0], states[:,1], states[:,2], 
                   c=states[:,2], cmap='magma', s=0.5)
        ax.set_title('Halvorsen Attractor')
        return fig

    @staticmethod
    def aizawa(steps=12000, dt=0.015, init_state=(0.1, 0, 0)):
        """
        Plots the Aizawa Attractor.
        A dense sphere of orbits with a tube bored through its axis[cite: 4].

        Inputs:
            steps (int): Total integration steps (default 12000)[cite: 4].
            dt (float): Time delta per step (default 0.015)[cite: 4].
            init_state (tuple): Initial (x, y, z) coordinates (default (0.1, 0, 0))[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot of the Aizawa Attractor.
        """
        def deriv(state, t):
            x, y, z = state
            return [(z - 0.7) * x - 3.5 * y, 
                    3.5 * x + (z - 0.7) * y, 
                    0.6 + 0.95 * z - z**3 / 3 - (x**2 + y**2) * (1 + 0.25 * z) + 0.1 * z * x**3]

        t = np.arange(0, steps * dt, dt)
        states = odeint(deriv, init_state, t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(states[:,0], states[:,1], states[:,2], 
                   c=states[:,2], cmap='inferno', s=0.5)
        ax.set_title('Aizawa Attractor')
        return fig

    @staticmethod
    def rabinovich(steps=10000, dt=0.01, init_state=(-1, 0, 0.5)):
        """
        Plots the Rabinovich-Fabrikant Attractor.
        Models modulation instability in waves and yields delicate structures that shift with its parameters[cite: 4].

        Inputs:
            steps (int): Total integration steps (default 10000)[cite: 4].
            dt (float): Time delta per step (default 0.01)[cite: 4].
            init_state (tuple): Initial (x, y, z) coordinates (default (-1, 0, 0.5))[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot of the Rabinovich-Fabrikant Attractor.
        """
        def deriv(state, t):
            x, y, z = state
            return [y * (z - 1 + x**2) + 0.1 * x, 
                    x * (3 * z + 1 - x**2) + 0.1 * y, 
                    -2 * z * (0.2875 + x * y)]

        t = np.arange(0, steps * dt, dt)
        states = odeint(deriv, init_state, t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(states[:,0], states[:,1], states[:,2], 
                   c=states[:,2], cmap='viridis', s=0.5)
        ax.set_title('Rabinovich-Fabrikant')
        return fig

    @staticmethod
    def lorenz84(steps=15000, dt=0.01, init_state=(1, 1, 1)):
        """
        Plots the Lorenz-84 Attractor.
        Lorenz's later, simpler model of westerly winds interacting with large-scale eddies[cite: 4].

        Inputs:
            steps (int): Total integration steps (default 15000)[cite: 4].
            dt (float): Time delta per step (default 0.01)[cite: 4].
            init_state (tuple): Initial (x, y, z) coordinates (default (1, 1, 1))[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot of the Lorenz-84 Attractor.
        """
        def deriv(state, t):
            x, y, z = state
            return [-0.25 * x - y**2 - z**2 + 2, 
                    -y + x * y - 4 * x * z + 1, 
                    -z + 4 * x * y + x * z]

        t = np.arange(0, steps * dt, dt)
        states = odeint(deriv, init_state, t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(states[:,0], states[:,1], states[:,2], 
                   c=states[:,2], cmap='plasma', s=0.5)
        ax.set_title('Lorenz-84 Attractor')
        return fig

    @staticmethod
    def sprottA(steps=12000, dt=0.02, init_state=(0, 5, 0)):
        """
        Plots Sprott System A.
        Found by J.C. Sprott in an automated search: one of the simplest equation sets that still produces chaos[cite: 4].

        Inputs:
            steps (int): Total integration steps (default 12000)[cite: 4].
            dt (float): Time delta per step (default 0.02)[cite: 4].
            init_state (tuple): Initial (x, y, z) coordinates (default (0, 5, 0))[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot of Sprott System A.
        """
        def deriv(state, t):
            x, y, z = state
            return [y, -x + y * z, 1 - y**2]

        t = np.arange(0, steps * dt, dt)
        states = odeint(deriv, init_state, t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(states[:,0], states[:,1], states[:,2], 
                   c=states[:,2], cmap='cool', s=0.5)
        ax.set_title('Sprott System A')
        return fig

    @staticmethod
    def nosehoover(steps=15000, dt=0.015, init_state=(1, 0, 0)):
        """
        Plots the Nosé-Hoover Attractor.
        Built to hold temperature constant in molecular dynamics, with a symmetric hollow core[cite: 4].

        Inputs:
            steps (int): Total integration steps (default 15000)[cite: 4].
            dt (float): Time delta per step (default 0.015)[cite: 4].
            init_state (tuple): Initial (x, y, z) coordinates (default (1, 0, 0))[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot of the Nosé-Hoover Attractor.
        """
        def deriv(state, t):
            x, y, z = state
            return [y, -x + y * z, 1.5 - y**2]

        t = np.arange(0, steps * dt, dt)
        states = odeint(deriv, init_state, t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(states[:,0], states[:,1], states[:,2], 
                   c=states[:,2], cmap='jet', s=0.5)
        ax.set_title('Nosé-Hoover Attractor')
        return fig

    @staticmethod
    def burkeshaw(steps=12000, dt=0.01, init_state=(1, 0, 0)):
        """
        Plots the Burke-Shaw Attractor.
        A Lorenz variant that folds into a clean, symmetric butterfly[cite: 4].

        Inputs:
            steps (int): Total integration steps (default 12000)[cite: 4].
            dt (float): Time delta per step (default 0.01)[cite: 4].
            init_state (tuple): Initial (x, y, z) coordinates (default (1, 0, 0))[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot of the Burke-Shaw Attractor.
        """
        def deriv(state, t):
            x, y, z = state
            return [-10 * (x + y), -y - 10 * x * z, 10 * x * y + 4.272]

        t = np.arange(0, steps * dt, dt)
        states = odeint(deriv, init_state, t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(states[:,0], states[:,1], states[:,2], 
                   c=states[:,2], cmap='hsv', s=0.5)
        ax.set_title('Burke-Shaw Attractor')
        return fig

    @staticmethod
    def dadras(steps=15000, dt=0.005, init_state=(1, 1, 1)):
        """
        Plots the Dadras Attractor.
        A chaotic system that stretches into a wide multi-lobed ribbon[cite: 4].

        Inputs:
            steps (int): Total integration steps (default 15000)[cite: 4].
            dt (float): Time delta per step (default 0.005)[cite: 4].
            init_state (tuple): Initial (x, y, z) coordinates (default (1, 1, 1))[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot of the Dadras Attractor.
        """
        def deriv(state, t):
            x, y, z = state
            return [y - 3 * x + 2.7 * y * z, 
                    1.7 * y - x * z + z, 
                    2 * x * y - 9 * z]

        t = np.arange(0, steps * dt, dt)
        states = odeint(deriv, init_state, t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(states[:,0], states[:,1], states[:,2], 
                   c=states[:,2], cmap='rainbow', s=0.5)
        ax.set_title('Dadras Attractor')
        return fig

    @staticmethod
    def fourwing(steps=12000, dt=0.05, init_state=(1, 1, 1)):
        """
        Plots the Four-Wing Attractor.
        Trajectories alternate between four lobes, a more intricate cousin of the two-winged Lorenz butterfly[cite: 4].

        Inputs:
            steps (int): Total integration steps (default 12000)[cite: 4].
            dt (float): Time delta per step (default 0.05)[cite: 4].
            init_state (tuple): Initial (x, y, z) coordinates (default (1, 1, 1))[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot of the Four-Wing Attractor.
        """
        def deriv(state, t):
            x, y, z = state
            return [0.2 * x + y * z, 
                    0.01 * x - 0.4 * y - x * z, 
                    -z - x * y]

        t = np.arange(0, steps * dt, dt)
        states = odeint(deriv, init_state, t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(states[:,0], states[:,1], states[:,2], 
                   c=states[:,2], cmap='coolwarm', s=0.5)
        ax.set_title('Four-Wing Attractor')
        return fig


class CurvesAndKnots:
    """
    Contains 3D closed curves and topological knots defined via a single parametric variable (t)[cite: 4, 5].
    """

    @staticmethod
    def trefoil(t_max=2.05 * np.pi, dt=0.02):
        """
        Plots a Trefoil Knot.
        The simplest nontrivial knot, which cannot be untied without cutting; the starting point of knot theory[cite: 4, 5].

        Inputs:
            t_max (float): Maximum parameter value (default ~2.05π)[cite: 4, 5].
            dt (float): Parameter step size (default 0.02)[cite: 4, 5].
            
        Output:
            matplotlib.figure.Figure: A 3D line plot of the knot.

        Real-Life Examples:
            1. Biology: Models the topological constraints and supercoiling of circular DNA molecules[cite: 5].
            2. Art and Architecture: A prominent motif in Celtic knotwork and modern structural design[cite: 5].
        """
        t = np.arange(0, t_max, dt)
        x = np.sin(t) + 2 * np.sin(2 * t)
        y = np.cos(t) - 2 * np.cos(2 * t)
        z = -np.sin(3 * t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c=z, cmap='cyan', s=10)
        ax.set_aspect("equal")
        ax.set_title('Trefoil Knot')
        return fig

    @staticmethod
    def torusknot(t_max=2.01 * np.pi, dt=0.01):
        """
        Plots a Torus Knot (3,5).
        A curve that winds 3 times around a torus the long way and 5 times the short way before closing[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default ~2.01π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D line plot of the Torus Knot.
        """
        t = np.arange(0, t_max, dt)
        r = 2 + np.cos(5 * t)
        x = r * np.cos(3 * t)
        y = r * np.sin(3 * t)
        z = -np.sin(5 * t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        # Using hsv as the closest matplotlib equivalent to 'Rainbow'
        ax.scatter(x, y, z, c=z, cmap='hsv', s=8)
        ax.set_aspect("equal")
        ax.set_title('Torus Knot (3,5)')
        return fig

    @staticmethod
    def lissajous3d(t_max=2.05 * np.pi, dt=0.01):
        """
        Plots a 3D Lissajous Curve.
        Three coupled harmonic oscillations tracing a closed, woven path[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default ~2.05π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D line plot of the 3D Lissajous Curve.
        """
        t = np.arange(0, t_max, dt)
        x = np.sin(3 * t + np.pi / 2)
        y = np.sin(4 * t)
        z = np.sin(5 * t)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c=z, cmap='hsv', s=6)
        ax.set_aspect("equal")
        ax.set_title('3D Lissajous Curve')
        return fig

    @staticmethod
    def viviani(t_max=4.02 * np.pi, dt=0.02):
        """
        Plots Viviani's Curve.
        The figure-8 where a sphere meets a cylinder passing through its center[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default ~4.02π)[cite: 4].
            dt (float): Parameter step size (default 0.02)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D line plot of Viviani's Curve.
        """
        t = np.arange(0, t_max, dt)
        x = 1 + np.cos(t)
        y = np.sin(t)
        z = 2 * np.sin(t / 2)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        # Using coolwarm as a substitute for 'Portland'
        ax.scatter(x, y, z, c=z, cmap='coolwarm', s=8)
        ax.set_aspect("equal")
        ax.set_title("Viviani's Curve")
        return fig

    @staticmethod
    def sphspiral(u_max=np.pi, du=0.004):
        """
        Plots a Spherical Spiral.
        A path that winds from pole to pole, crossing every line of longitude at a steady rate[cite: 4].

        Inputs:
            u_max (float): Maximum parameter value (default π)[cite: 4].
            du (float): Parameter step size (default 0.004)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D line plot of the Spherical Spiral.
        """
        u = np.arange(0, u_max, du)
        x = np.sin(u) * np.cos(12 * u)
        y = np.sin(u) * np.sin(12 * u)
        z = np.cos(u)
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c=z, cmap='viridis', s=6)
        ax.set_aspect("equal")
        ax.set_title('Spherical Spiral')
        return fig

    @staticmethod
    def conespiral(t_max=5, dt=0.01):
        """
        Plots a Conical Spiral.
        A helix whose radius grows with height, wrapping the surface of a cone[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 5)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D line plot of the Conical Spiral.
        """
        t = np.arange(0, t_max, dt)
        x = t * np.cos(6 * t)
        y = t * np.sin(6 * t)
        z = t
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c=z, cmap='plasma', s=6)
        ax.set_aspect("equal")
        ax.set_title('Conical Spiral')
        return fig


class EngineeringCurves:
    """
    Contains 2D kinematic and engineering curves (plotted flat on the XY plane).
    These encompass cycloids, spirals, gears, and linkages often used in mechanical design[cite: 4, 5].
    """

    @staticmethod
    def _plot_curve(x, y, title, cmap):
        """Helper method to plot 2D curves flattened in 3D space with uniform styling[cite: 4, 5]."""
        z = np.zeros_like(x)
        color_arr = np.arange(len(x))
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c=color_arr, cmap=cmap, s=6)
        ax.set_aspect("equal")
        ax.set_title(title)
        return fig

    @staticmethod
    def _epi(t, R, r, d):
        """Helper to generate epicycloid/epitrochoid parametric coordinates[cite: 4]."""
        x = (R + r) * np.cos(t) - d * np.cos((R + r) / r * t)
        y = (R + r) * np.sin(t) - d * np.sin((R + r) / r * t)
        return x, y

    @staticmethod
    def _hypo(t, R, r, d):
        """Helper to generate hypocycloid/hypotrochoid parametric coordinates[cite: 4]."""
        x = (R - r) * np.cos(t) + d * np.cos((R - r) / r * t)
        y = (R - r) * np.sin(t) - d * np.sin((R - r) / r * t)
        return x, y

    @staticmethod
    def cycloid(t_max=6 * np.pi, dt=0.02, r=1):
        """
        Plots a Cycloid.
        The path traced by a point on the rim of a rolling wheel. Its arches form the profile for cycloidal gears[cite: 4, 5].

        Inputs:
            t_max (float): Maximum angle/parameter (default 6π)[cite: 4, 5].
            dt (float): Parameter step size (default 0.02)[cite: 4, 5].
            r (float): Radius of the rolling circle (default 1)[cite: 5].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane[cite: 5].

        Real-Life Examples:
            1. Mechanical Engineering: The basis for cycloidal drives and specific gear tooth profiles requiring zero-friction contact[cite: 4, 5].
            2. Physics: Closely related to the tautochrone curve used in perfectly isochronous pendulum clocks designed by Huygens[cite: 4, 5].
        """
        t = np.arange(0, t_max, dt)
        x = r * (t - np.sin(t))
        y = r * (1 - np.cos(t))
        return EngineeringCurves._plot_curve(x, y, 'Cycloid', 'plasma')

    @staticmethod
    def brachistochrone(t_max=2 * np.pi, dt=0.01, r=1):
        """
        Plots a Brachistochrone (Tautochrone) curve[cite: 4].
        An upside-down cycloid: the frictionless slide that gets a bead from A to B fastest, and in equal time from anywhere on the curve[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            r (float): Radius of the rolling circle (default 1).
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.

        Real-Life Examples:
            1. Physics: Solves the curve of fastest descent problem proposed by Johann Bernoulli.
            2. Entertainment: Applied in roller coaster design to maximize acceleration through dips.
        """
        t = np.arange(0, t_max, dt)
        x = r * (t - np.sin(t))
        y = r * (np.cos(t) - 1)
        return EngineeringCurves._plot_curve(x, y, 'Brachistochrone (Tautochrone)', 'viridis')

    @staticmethod
    def trochoidin(t_max=6 * np.pi, dt=0.02, r=1, d=0.6):
        """
        Plots an Inferior Trochoid (curtate)[cite: 4].
        A point inside the wheel, such as one on a spoke. The path is a wavy line with no cusps or loops[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 6π)[cite: 4].
            dt (float): Parameter step size (default 0.02)[cite: 4].
            r (float): Rolling circle radius (default 1)[cite: 4].
            d (float): Pen distance from center (default 0.6)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Mechanics: The trajectory of an internal point on a rolling wheel or locomotive drive shaft.
            2. Animation: Simulating smooth, undulating movement paths without sharp turns.
        """
        t = np.arange(0, t_max, dt)
        x = r * t - d * np.sin(t)
        y = r - d * np.cos(t)
        # Using coolwarm for 'Portland' mapping
        return EngineeringCurves._plot_curve(x, y, 'Inferior Trochoid (curtate)', 'coolwarm')

    @staticmethod
    def trochoidsup(t_max=6 * np.pi, dt=0.02, r=1, d=1.6):
        """
        Plots a Superior Trochoid (prolate)[cite: 4].
        A point beyond the rim, like a train wheel's flange. At the bottom it moves backward, so the path forms loops[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 6π)[cite: 4].
            dt (float): Parameter step size (default 0.02)[cite: 4].
            r (float): Rolling circle radius (default 1)[cite: 4].
            d (float): Pen distance from center (default 1.6)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Railway Engineering: Describes the retrograde motion of a train wheel's outer flange below the track[cite: 4].
            2. Kinematics: Traced by specific linkages designed to create dwell periods and loops.
        """
        t = np.arange(0, t_max, dt)
        x = r * t - d * np.sin(t)
        y = r - d * np.cos(t)
        # Using hsv as a vibrant alternative for 'Electric'
        return EngineeringCurves._plot_curve(x, y, 'Superior Trochoid (prolate)', 'hsv')

    @staticmethod
    def cardioid(t_max=2 * np.pi, dt=0.01):
        """
        Plots a Cardioid.
        An epicycloid with one cusp. It describes the pickup pattern of a cardioid microphone[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Audio Engineering: The unidirectional polar response of a cardioid microphone[cite: 4].
            2. Optics: Forms the central bright caustic reflection in a teacup[cite: 4].
        """
        t = np.arange(0, t_max, dt)
        x, y = EngineeringCurves._epi(t, 1, 1, 1)
        return EngineeringCurves._plot_curve(x, y, 'Cardioid', 'magma')

    @staticmethod
    def nephroid(t_max=2 * np.pi, dt=0.01):
        """
        Plots a Nephroid.
        An epicycloid with two cusps. It is the caustic that sunlight draws inside a coffee cup[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Optics: The common bright caustic pattern formed by reflected light inside cylindrical mirrors[cite: 4].
            2. Gear Design: Used occasionally in specialized multi-lobe gear profiling.
        """
        t = np.arange(0, t_max, dt)
        x, y = EngineeringCurves._epi(t, 2, 1, 1)
        return EngineeringCurves._plot_curve(x, y, 'Nephroid', 'inferno')

    @staticmethod
    def epi3(t_max=2 * np.pi, dt=0.01):
        """
        Plots an Epicycloid with 3 cusps[cite: 4].
        A circle rolling outside a fixed circle three times its size, the flank shape of cycloidal gear teeth[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Mechanical Engineering: The primary curved flank shape behind highly efficient cycloidal drives[cite: 4].
            2. Horology: Used extensively in mechanical clockwork to minimize friction between gears.
        """
        t = np.arange(0, t_max, dt)
        x, y = EngineeringCurves._epi(t, 3, 1, 1)
        return EngineeringCurves._plot_curve(x, y, 'Epicycloid (3 cusps)', 'hsv')

    @staticmethod
    def ranunculoid(t_max=2 * np.pi, dt=0.01):
        """
        Plots a Ranunculoid (5 cusps)[cite: 4].
        Rolling outside a circle five times larger gives five pointed petals[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Generative Design: Serves as a mathematical template for decorative, star-like motifs[cite: 4].
            2. Geometry: A prominent member of the epicycloid family studied for its harmonic properties.
        """
        t = np.arange(0, t_max, dt)
        x, y = EngineeringCurves._epi(t, 5, 1, 1)
        return EngineeringCurves._plot_curve(x, y, 'Ranunculoid (5 cusps)', 'Spectral')

    @staticmethod
    def epitroin(t_max=2 * np.pi, dt=0.01):
        """
        Plots an Inferior Epitrochoid[cite: 4].
        The pen sits inside the rolling circle, so the cusps soften into rounded lobes[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Recreational Math: Basic rosettes generated by drawing toys like the Spirograph[cite: 4].
            2. Machinery: Profiles for rotary engines and internal planetary gear housing.
        """
        t = np.arange(0, t_max, dt)
        x, y = EngineeringCurves._epi(t, 3, 1, 0.5)
        return EngineeringCurves._plot_curve(x, y, 'Inferior Epitrochoid', 'plasma')

    @staticmethod
    def epitrosup(t_max=2 * np.pi, dt=0.01):
        """
        Plots a Superior Epitrochoid[cite: 4].
        The pen sits beyond the rolling circle's edge, which ties a small loop into every lobe[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Toys and Art: One of the classic looped patterns generated by the Spirograph[cite: 4].
            2. Cams: Used to design complex multi-lobe cams that require distinct dwell phases.
        """
        t = np.arange(0, t_max, dt)
        x, y = EngineeringCurves._epi(t, 3, 1, 2)
        return EngineeringCurves._plot_curve(x, y, 'Superior Epitrochoid', 'viridis')

    @staticmethod
    def wankel(t_max=2 * np.pi, dt=0.01):
        """
        Plots a Wankel Housing (epitrochoid)[cite: 4].
        The two-lobed epitrochoid inside a rotary engine, traced so the triangular rotor always touches its wall[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Automotive Engineering: Defines the combustion chamber housing for Wankel rotary engines[cite: 4].
            2. Compressors: Also forms the internal geometry of certain liquid-ring and gas compressors.
        """
        t = np.arange(0, t_max, dt)
        x = np.cos(t) + 0.18 * np.cos(3 * t)
        y = np.sin(t) + 0.18 * np.sin(3 * t)
        return EngineeringCurves._plot_curve(x, y, 'Wankel Housing (epitrochoid)', 'jet')

    @staticmethod
    def deltoid(t_max=2 * np.pi, dt=0.01):
        """
        Plots a Deltoid (Steiner curve)[cite: 4].
        A circle rolling inside one three times its size makes a curved triangle with three cusps[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Manufacturing: Used as a profile in specialized continuous-rotor pumps (Moineau pumps)[cite: 4].
            2. Textiles: Forms the cross-section shape of certain synthetic trilobal fibers.
        """
        t = np.arange(0, t_max, dt)
        x, y = EngineeringCurves._hypo(t, 3, 1, 1)
        return EngineeringCurves._plot_curve(x, y, 'Deltoid (Steiner curve)', 'terrain')

    @staticmethod
    def astroid(t_max=2 * np.pi, dt=0.01):
        """
        Plots an Astroid[cite: 4].
        The four-cusped star. It is the envelope of a sliding ladder, and the shape of the Cartesian "pencil of lines" trammel[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Kinematics: The envelope traced when a ladder slides down a wall (a Trammel of Archimedes)[cite: 4].
            2. Magnetism: Models the switching asteroid diagram in applied magnetic fields (Stoner-Wohlfarth).
        """
        t = np.arange(0, t_max, dt)
        x, y = EngineeringCurves._hypo(t, 4, 1, 1)
        return EngineeringCurves._plot_curve(x, y, 'Astroid', 'coolwarm')

    @staticmethod
    def hypo52(t_max=4 * np.pi, dt=0.01):
        """
        Plots a Hypocycloid (R/r = 5/2)[cite: 4].
        A non-integer ratio takes two turns to close and traces a five-pointed star[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 4π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Art and Architecture: A mathematical method for laying out perfect pentagrams and five-pointed motifs[cite: 4].
            2. Security Printing: Component of the complex guilloche patterns found on banknotes.
        """
        t = np.arange(0, t_max, dt)
        x, y = EngineeringCurves._hypo(t, 5, 2, 2)
        return EngineeringCurves._plot_curve(x, y, 'Hypocycloid (R/r = 5/2)', 'magma')

    @staticmethod
    def hypotroin(t_max=6 * np.pi, dt=0.02):
        """
        Plots an Inferior Hypotrochoid[cite: 4].
        A Spirograph pattern with the pen inside the rolling circle: a rounded rosette with no loops[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 6π)[cite: 4].
            dt (float): Parameter step size (default 0.02)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Generative Art: One of the hallmark internal patterns generated by the Spirograph toy[cite: 4].
            2. Anti-Counterfeiting: Fine-line rosettes on certificates and passports.
        """
        t = np.arange(0, t_max, dt)
        x, y = EngineeringCurves._hypo(t, 5, 3, 2)
        return EngineeringCurves._plot_curve(x, y, 'Inferior Hypotrochoid', 'hsv')

    @staticmethod
    def hypotrosup(t_max=6 * np.pi, dt=0.02):
        """
        Plots a Superior Hypotrochoid[cite: 4].
        The classic Spirograph curve: the pen sits beyond the rolling circle's rim, so each lobe gets a loop[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 6π)[cite: 4].
            dt (float): Parameter step size (default 0.02)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Art/Toys: The quintessential pattern produced by placing a pen in the outer hole of a Spirograph gear[cite: 4].
            2. Machinery: Orbiting paths traced in specific planetary gearbox arrangements.
        """
        t = np.arange(0, t_max, dt)
        x, y = EngineeringCurves._hypo(t, 5, 3, 5)
        return EngineeringCurves._plot_curve(x, y, 'Superior Hypotrochoid', 'plasma')

    @staticmethod
    def archspiral(t_max=8 * np.pi, dt=0.02):
        """
        Plots an Archimedean Spiral (r = a*theta)[cite: 4].
        Equal spacing between turns, as in scroll compressors, record grooves and constant-lift cams[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 8π)[cite: 4].
            dt (float): Parameter step size (default 0.02)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Audio/HVAC: The groove spacing on vinyl records and the internal shape of a scroll compressor[cite: 4].
            2. Mechanics: Constant-lift cam profiles and the unwinding of flat coil springs.
        """
        t = np.arange(0, t_max, dt)
        x = 0.4 * t * np.cos(t)
        y = 0.4 * t * np.sin(t)
        return EngineeringCurves._plot_curve(x, y, 'Archimedean Spiral', 'viridis')

    @staticmethod
    def logspiral(t_min=-4 * np.pi, t_max=2 * np.pi, dt=0.02):
        """
        Plots a Logarithmic Spiral (r = a*e^{b*theta})[cite: 4].
        Equiangular: it crosses every radius at the same angle. Nautilus shells and pump volutes follow it[cite: 4].

        Inputs:
            t_min (float): Minimum parameter value (default -4π)[cite: 4].
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.02)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Nature/Biology: The growth pattern of Nautilus shells, hurricane bands, and galaxy arms[cite: 4].
            2. Fluid Dynamics: The ideal expanding profile for a centrifugal pump's volute casing[cite: 4].
        """
        t = np.arange(t_min, t_max, dt)
        r = np.exp(0.2 * t)
        x = r * np.cos(t)
        y = r * np.sin(t)
        return EngineeringCurves._plot_curve(x, y, 'Logarithmic Spiral', 'inferno')

    @staticmethod
    def fermat(t_min=-4, t_max=4, dt=0.005):
        """
        Plots Fermat's Spiral (r^2 = a^2 * theta)[cite: 4].
        A parabolic spiral whose two branches interlock through the origin. Sunflower seed heads grow along it[cite: 4].

        Inputs:
            t_min (float): Minimum parameter value (default -4)[cite: 4].
            t_max (float): Maximum parameter value (default 4)[cite: 4].
            dt (float): Parameter step size (default 0.005)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Botany: The fundamental phyllotactic arrangement of seeds in a sunflower head[cite: 4].
            2. Renewable Energy: Used to perfectly pack and position heliostat mirrors in solar thermal plants.
        """
        t = np.arange(t_min, t_max, dt)
        x = t * np.cos(t**2)
        y = t * np.sin(t**2)
        return EngineeringCurves._plot_curve(x, y, "Fermat's Spiral", 'coolwarm')

    @staticmethod
    def clothoid(t_min=-4, t_max=4, dt=0.01):
        """
        Plots an Euler Spiral (Clothoid)[cite: 4].
        Curvature grows steadily with distance. Highways and railways use it so steering eases in rather than jerking[cite: 4].

        Inputs:
            t_min (float): Minimum parameter value (default -4)[cite: 4].
            t_max (float): Maximum parameter value (default 4)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Civil Engineering: Highway transition curves and off-ramps linking straights to circles[cite: 4].
            2. Entertainment: Ensures safe, continuous transitions in extreme roller coaster loops[cite: 4].
        """
        t = np.arange(t_min, t_max, dt)
        # Using scipy's fresnel integration (S, C = fresnel(t)) which precisely calculates the clothoid coordinates.
        S, C = fresnel(t)
        return EngineeringCurves._plot_curve(C, S, 'Euler Spiral (Clothoid)', 'jet')

    @staticmethod
    def involute(t_max=8, dt=0.01):
        """
        Plots an Involute of a Circle[cite: 4].
        The path of a taut string unwinding from a circle, and the standard tooth profile for most gears[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 8)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Gear Engineering: The nearly universal curved flank profile for spur and helical gear teeth[cite: 4].
            2. HVAC: The internal stationary and orbiting spirals of a scroll compressor.
        """
        t = np.arange(0, t_max, dt)
        x = np.cos(t) + t * np.sin(t)
        y = np.sin(t) - t * np.cos(t)
        return EngineeringCurves._plot_curve(x, y, 'Involute of a Circle', 'hsv')

    @staticmethod
    def fourbar(t_max=2 * np.pi, dt=0.01):
        """
        Plots a Four-Bar Coupler Curve[cite: 4].
        A point on the coupler of a crank-rocker linkage (links 1, 3, 3, 3). Linkage designers use such curves to guide motion[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Mechanics: The swept path of a windshield wiper or pumpjack head mechanism[cite: 4].
            2. Manufacturing: Used to coordinate multi-stage pick-and-place automation systems.
        """
        t = np.arange(0, t_max, dt)
        ax_c, ay_c = np.cos(t), np.sin(t)
        dx, dy = 3 - ax_c, -ay_c
        L = np.hypot(dx, dy)
        a = L / 2
        h = np.sqrt(9 - a**2)
        ux, uy = dx / L, dy / L
        vx = (a * ux - h * uy) / 3
        vy = (a * uy + h * ux) / 3
        c, s = np.cos(0.5), np.sin(0.5)
        x = ax_c + 3.5 * (vx * c - vy * s)
        y = ay_c + 3.5 * (vx * s + vy * c)
        return EngineeringCurves._plot_curve(x, y, 'Four-Bar Coupler Curve', 'plasma')

    @staticmethod
    def slidercrank(t_max=4 * np.pi, dt=0.02):
        """
        Plots Slider-Crank Piston Motion[cite: 4].
        Piston position against crank angle for l/r = 3.5. The connecting rod makes it differ from a pure sine wave[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 4π)[cite: 4].
            dt (float): Parameter step size (default 0.02)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Automotive: Represents the true kinematic displacement of an internal combustion engine's piston[cite: 4].
            2. Hydraulics: The linear motion driving a reciprocating piston water pump[cite: 4].
        """
        t = np.arange(0, t_max, dt)
        x = t
        y = np.cos(t) + np.sqrt(12.25 - np.sin(t)**2)
        return EngineeringCurves._plot_curve(x, y, 'Slider-Crank Piston Motion', 'viridis')

    @staticmethod
    def limacon(t_max=2 * np.pi, dt=0.01):
        """
        Plots a Limaçon (r = b + a*cos(theta))[cite: 4].
        With a > b it grows an inner loop. It shows up in cam profiles and as the path of a crank-driven point[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Machinery: Profiling standard rotating cams to convert rotary motion into complex linear dwells[cite: 4].
            2. Optics: Forms part of the caustic light reflections off a cylindrical mirror.
        """
        t = np.arange(0, t_max, dt)
        r = 1 + 2 * np.cos(t)
        x = r * np.cos(t)
        y = r * np.sin(t)
        return EngineeringCurves._plot_curve(x, y, 'Limaçon', 'magma')

    @staticmethod
    def catenary(t_min=-3, t_max=3, dt=0.02):
        """
        Plots a Catenary (y = a*cosh(x/a))[cite: 4].
        How a free-hanging chain sags. Flipped upside down, it is the ideal shape for a masonry arch[cite: 4].

        Inputs:
            t_min (float): Minimum parameter value (default -3)[cite: 4].
            t_max (float): Maximum parameter value (default 3)[cite: 4].
            dt (float): Parameter step size (default 0.02)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Architecture: The structurally optimal shape (an inverted catenary) for masonry arches and vaults, notably the Gateway Arch[cite: 4].
            2. Civil Engineering: The natural sagging profile of high-voltage power lines and suspension bridge cables[cite: 4].
        """
        t = np.arange(t_min, t_max, dt)
        x = t
        y = np.cosh(t)
        return EngineeringCurves._plot_curve(x, y, 'Catenary', 'terrain')

    @staticmethod
    def tractrix(t_min=-6, t_max=6, dt=0.02):
        """
        Plots a Tractrix[cite: 4].
        The path of an object dragged by a rope along a straight line. It is also the profile of a Schiele pivot bearing[cite: 4].

        Inputs:
            t_min (float): Minimum parameter value (default -6)[cite: 4].
            t_max (float): Maximum parameter value (default 6)[cite: 4].
            dt (float): Parameter step size (default 0.02)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Mechanics: The profile for a Schiele pivot bearing that distributes wear perfectly evenly across its surface[cite: 4].
            2. Acoustics: The optimal expanding shape for a horn loudspeaker (a tractricial horn)[cite: 4].
        """
        t = np.arange(t_min, t_max, dt)
        x = t - np.tanh(t)
        y = 1 / np.cosh(t)
        return EngineeringCurves._plot_curve(x, y, 'Tractrix', 'coolwarm')

    @staticmethod
    def damped(t_max=20, dt=0.02):
        """
        Plots a Damped Oscillation[cite: 4].
        A spring-mass system losing energy: the sine wave shrinks under an exponential envelope[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 20)[cite: 4].
            dt (float): Parameter step size (default 0.02)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Automotive: The ideal settling response of a vehicle's shock absorber traversing a bump[cite: 4].
            2. Acoustics: Visualizing the natural decay rate (reverberation time) of sound in a room[cite: 4].
        """
        t = np.arange(0, t_max, dt)
        x = t
        y = np.exp(-0.2 * t) * np.sin(4 * t)
        return EngineeringCurves._plot_curve(x, y, 'Damped Oscillation', 'inferno')

    @staticmethod
    def beats(t_max=4 * np.pi, dt=0.01):
        """
        Plots a Beat Pattern[cite: 4].
        Two close frequencies interfere and the amplitude swells and fades, the signal behind out-of-tune strings and vibration beating[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 4π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Acoustics/Music: The pulsing "wah-wah" interference sound heard when two slightly out-of-tune guitar strings are played[cite: 4].
            2. Machinery: Used in vibration analysis to detect twin rotors spinning at slightly different speeds[cite: 4].
        """
        t = np.arange(0, t_max, dt)
        x = t
        y = np.sin(10 * t) + np.sin(11 * t)
        return EngineeringCurves._plot_curve(x, y, 'Beat Pattern', 'hsv')

    @staticmethod
    def lissajous2d(t_max=2 * np.pi, dt=0.005):
        """
        Plots a Lissajous Figure (5:4)[cite: 4].
        What an oscilloscope shows when two signals of related frequency drive its axes. The knot count reveals the ratio[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.005)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Electronics: Displayed on X-Y oscilloscopes to visualize the exact phase and frequency ratio between two AC signals[cite: 4].
            2. Laser Light Shows: The mathematical basis for galvanometer-scanned laser projections[cite: 4].
        """
        t = np.arange(0, t_max, dt)
        x = np.sin(5 * t + np.pi / 2)
        y = np.sin(4 * t)
        return EngineeringCurves._plot_curve(x, y, 'Lissajous Figure (5:4)', 'jet')

    @staticmethod
    def superellipse(t_max=2 * np.pi, dt=0.01):
        """
        Plots a Superellipse (n = 4)[cite: 4].
        Between a circle and a rounded square. Designers use it for table tops, plazas and app icons[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Urban Design/Architecture: Piet Hein famously utilized this exact shape for a traffic roundabout in Stockholm (Sergels Torg)[cite: 4].
            2. Software UI: The mathematical curve used to round corners on many mobile device app icons (like iOS)[cite: 4].
        """
        t = np.arange(0, t_max, dt)
        x = np.sign(np.cos(t)) * np.abs(np.cos(t))**0.5
        y = np.sign(np.sin(t)) * np.abs(np.sin(t))**0.5
        return EngineeringCurves._plot_curve(x, y, 'Superellipse (n = 4)', 'viridis')

    @staticmethod
    def lemniscate(t_max=2 * np.pi, dt=0.01):
        """
        Plots the Lemniscate of Bernoulli[cite: 4].
        The figure-8 where the product of the distances to two foci stays constant. Railway transition curves borrow its shape[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 2π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Civil Engineering: Its central geometry is often used as a template for railway transition curves[cite: 4].
            2. Typography: The origin of the standard infinity symbol (∞)[cite: 4].
        """
        t = np.arange(0, t_max, dt)
        denom = 1 + np.sin(t)**2
        x = 2 * np.cos(t) / denom
        y = 2 * np.sin(t) * np.cos(t) / denom
        return EngineeringCurves._plot_curve(x, y, 'Lemniscate of Bernoulli', 'plasma')

    @staticmethod
    def witch(t_min=-8, t_max=8, dt=0.02):
        """
        Plots the Witch of Agnesi[cite: 4].
        A bell-shaped curve named by a mistranslation. It resembles resonance peaks and diffraction profiles[cite: 4].

        Inputs:
            t_min (float): Minimum parameter value (default -8)[cite: 4].
            t_max (float): Maximum parameter value (default 8)[cite: 4].
            dt (float): Parameter step size (default 0.02)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Physics: The standard mathematical model for spectral line broadening and resonance curves (Lorentzian function)[cite: 4].
            2. Statistics: Exactly matches the probability density curve of the Cauchy distribution.
        """
        t = np.arange(t_min, t_max, dt)
        x = t
        y = 8 / (t**2 + 4)
        return EngineeringCurves._plot_curve(x, y, 'Witch of Agnesi', 'terrain')

    @staticmethod
    def cissoid(t_min=-4, t_max=4, dt=0.01):
        """
        Plots the Cissoid of Diocles[cite: 4].
        Invented to double the cube. Its cusp and asymptote make a shape much like a pointed leaf with open arms[cite: 4].

        Inputs:
            t_min (float): Minimum parameter value (default -4)[cite: 4].
            t_max (float): Maximum parameter value (default 4)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. History of Mathematics: Famously devised to solve the classical geometric problem of duplicating the cube[cite: 4].
            2. Kinematics: Forms the cusp locus of certain mechanical linkages.
        """
        t = np.arange(t_min, t_max, dt)
        denom = 1 + t**2
        x = 2 * t**2 / denom
        y = 2 * t**3 / denom
        return EngineeringCurves._plot_curve(x, y, 'Cissoid of Diocles', 'magma')

    @staticmethod
    def rose52(t_max=4 * np.pi, dt=0.01):
        """
        Plots a Rose Curve (k = 5/2)[cite: 4].
        A petal curve. With an odd numerator over 2 it needs four turns to close, and the petals overlap[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 4π)[cite: 4].
            dt (float): Parameter step size (default 0.01)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Art and Architecture: A natural, harmonic geometry used to map stained glass rose windows and architectural motifs[cite: 4].
            2. Acoustics: Visualizes certain multi-nodal standing wave vibration patterns on a circular membrane.
        """
        t = np.arange(0, t_max, dt)
        x = np.cos(2.5 * t) * np.cos(t)
        y = np.cos(2.5 * t) * np.sin(t)
        return EngineeringCurves._plot_curve(x, y, 'Rose Curve (k = 5/2)', 'hsv')

    @staticmethod
    def butterfly(t_max=12 * np.pi, dt=0.02):
        """
        Plots the Butterfly Curve[cite: 4].
        Temple Fay's 1989 polar curve, drawn here over 12π so its wings fill in[cite: 4].

        Inputs:
            t_max (float): Maximum parameter value (default 12π)[cite: 4].
            dt (float): Parameter step size (default 0.02)[cite: 4].
            
        Output:
            matplotlib.figure.Figure: A 3D scatter plot rendered flat on the XY plane.
            
        Real-Life Examples:
            1. Mathematical Art: A highly popular polar equation representing the aesthetic possibilities of generative design algorithms[cite: 4].
            2. Procedural Animation: Provides an organic, complex, closed looping path for computer graphics sprites.
        """
        t = np.arange(0, t_max, dt)
        r = np.exp(np.cos(t)) - 2 * np.cos(4 * t) - np.sin(t / 12)**5
        x = r * np.sin(t)
        y = r * np.cos(t)
        return EngineeringCurves._plot_curve(x, y, 'Butterfly Curve', 'inferno')


class InvolutesEvolutes:
    """
    Contains involutes and evolutes of planar curves mapped into 3D. 
    Each visualization pairs a primary curve with its involute (traced by unwinding a taut string) 
    or its evolute (the envelope of its normals)[cite: 4, 6].
    """

    @staticmethod
    def _plot_bundle(curves, title, cmap):
        """Helper to plot a bundle of curves with independent coloring[cite: 4, 6]."""
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        colors = plt.cm.get_cmap(cmap)(np.linspace(0, 1, len(curves)))
        
        for i, curve in enumerate(curves):
            x, y = curve[:, 0], curve[:, 1]
            z = np.zeros_like(x)
            ax.plot(x, y, z, color=colors[i], linewidth=2)
            
        ax.set_aspect("equal")
        ax.set_title(title)
        return fig

    @staticmethod
    def invfamily(k_count=8, r=1, t_max=4.5, dt=0.05):
        """
        Plots the Involute Family of a Circle.
        Eight involutes of one base circle, each a rotated copy of the others. This is the pinwheel that gear teeth are cut from[cite: 4, 6].

        Inputs:
            k_count (int): Number of involutes (default 8)[cite: 4, 6].
            r (float): Radius of the base circle (default 1)[cite: 4, 6].
            t_max (float): Maximum unwinding parameter (default 4.5)[cite: 4, 6].
            dt (float): Parameter step size (default 0.05)[cite: 4, 6].
            
        Output:
            matplotlib.figure.Figure: A 3D line plot showing the base circle and its involutes.

        Real-Life Examples:
            1. Mechanical Engineering: The foundational geometry for designing meshing involute gear teeth[cite: 4].
            2. Compressors: Provides the identical paired scroll profiles used in scroll compressors.
        """
        t_circ = np.arange(0, 2 * np.pi, dt)
        base_circle = np.column_stack([r * np.cos(t_circ), r * np.sin(t_circ)])
        curves = [base_circle]
        
        t = np.arange(0, t_max, dt)
        for k in range(k_count):
            a = k * np.pi / (k_count / 2)
            x = r * np.cos(t + a) + r * t * np.sin(t + a)
            y = r * np.sin(t + a) - r * t * np.cos(t + a)
            curves.append(np.column_stack([x, y]))
            
        return InvolutesEvolutes._plot_bundle(curves, 'Involute Family of a Circle', 'hsv')

    @staticmethod
    def spurgear():
        """
        Plots an Involute Spur Gear (14 teeth).
        Each tooth flank is an involute of the base circle, so the gears roll with a constant velocity ratio. The inner rings mark the pitch and base circles[cite: 4, 6].

        Output:
            matplotlib.figure.Figure: A 3D line plot displaying the gear profile.

        Real-Life Examples:
            1. Power Transmission: The standard tooth profile allowing smooth, constant-velocity power transfer between gears[cite: 4].
            2. Clocks/Watches: Used where precise timing and minimal friction are critical.
        """
        N = 14
        rp = N / 2
        rb = rp * np.cos(np.pi / 9)
        ra = rp + 1
        rr = rp - 1.25
        hb = np.pi / (2 * N) + np.tan(np.pi / 9) - np.pi / 9
        tm = np.sqrt((ra / rb)**2 - 1)
        
        def inv(t): return t - np.arctan(t)
        
        out_x, out_y = [], []
        for k in range(N):
            c = 2 * np.pi * k / N
            def add(r, a): 
                out_x.append(r * np.cos(c + a))
                out_y.append(r * np.sin(c + a))
                
            def flank(s):
                for i in range(17):
                    t = tm * (i if s < 0 else 16 - i) / 16
                    add(rb * np.sqrt(1 + t * t), s * (hb - inv(t)))
                    
            add(rr, -hb)
            flank(-1)
            flank(1)
            add(rr, hb)
            for i in range(1, 5):
                add(rr, hb + (2 * np.pi / N - 2 * hb) * i / 5)
                
        out_x.append(out_x[0])
        out_y.append(out_y[0])
        gear_outline = np.column_stack([out_x, out_y])
        
        t = np.arange(0, 2 * np.pi + 0.05, 0.05)
        pitch_circle = np.column_stack([7 * np.cos(t), 7 * np.sin(t)])
        base_circle = np.column_stack([7 * np.cos(np.pi / 9) * np.cos(t), 7 * np.cos(np.pi / 9) * np.sin(t)])
        
        return InvolutesEvolutes._plot_bundle([gear_outline, pitch_circle, base_circle], 'Involute Spur Gear (14 teeth)', 'plasma')

    @staticmethod
    def _involute(curve_func, t0, t1, dt, tc):
        """Computes the involute of a parameterized curve numerically[cite: 4, 6]."""
        t_vals = np.arange(t0, t1 + dt, dt)
        points = np.array([curve_func(t) for t in t_vals])
        
        # Calculate arc length
        dp = np.diff(points, axis=0)
        ds = np.hypot(dp[:, 0], dp[:, 1])
        s = np.concatenate(([0], np.cumsum(ds)))
        
        # Find arc length at tc
        idx_tc = int(np.round((tc - t0) / dt))
        idx_tc = np.clip(idx_tc, 0, len(s) - 1)
        L0 = s[idx_tc]
        
        inv_points = []
        for i in range(len(points)):
            p = points[i]
            if i < len(points) - 1:
                tangent = points[i + 1] - points[i]
            else:
                tangent = points[i] - points[i - 1]
                
            l = np.hypot(tangent[0], tangent[1])
            if l > 1e-9:
                inv_points.append([p[0] - (s[i] - L0) * tangent[0] / l, 
                                 p[1] - (s[i] - L0) * tangent[1] / l])
            else:
                inv_points.append(p)
                
        return np.array(inv_points)

    @staticmethod
    def invellipse():
        """
        Plots Involutes of an Ellipse.
        String unwound from an ellipse spirals outward. Starting at the two ends of the axes gives two different involutes[cite: 4, 6].

        Output:
            matplotlib.figure.Figure: A 3D plot of an ellipse and two of its involutes.
            
        Real-Life Examples:
            1. Mechanics: Cam profiling where the base follower is an ellipse[cite: 6].
            2. Optics: Related to wave fronts emitted from an elliptical source.
        """
        def ell(t): return [2 * np.cos(t), np.sin(t)]
        
        t_vals = np.arange(0, 2 * np.pi, 0.05)
        base = np.array([ell(t) for t in t_vals])
        inv1 = InvolutesEvolutes._involute(ell, 0, 4 * np.pi, 0.02, 0)
        inv2 = InvolutesEvolutes._involute(ell, 0, 4 * np.pi, 0.02, np.pi)
        
        # Using coolwarm as 'Portland' substitute
        return InvolutesEvolutes._plot_bundle([base, inv1, inv2], 'Involutes of an Ellipse', 'coolwarm')

    @staticmethod
    def invparabola():
        """
        Plots the Involute of a Parabola.
        Unwinding from the vertex gives a curve with a cusp at the start, which bends back toward the parabola's axis[cite: 4, 6].

        Output:
            matplotlib.figure.Figure: A 3D plot of a parabola and its involute.
            
        Real-Life Examples:
            1. Geometry: Demonstrates how a curve lacking a closed perimeter generates an infinitely extending involute[cite: 6].
            2. Antenna Design: The unwinding path from a parabolic reflector.
        """
        def par(t): return [t, t**2]
        
        t_vals = np.arange(-1.5, 1.5, 0.05)
        base = np.array([par(t) for t in t_vals])
        inv = InvolutesEvolutes._involute(par, -1.5, 1.5, 0.01, 0)
        
        return InvolutesEvolutes._plot_bundle([base, inv], 'Involute of a Parabola', 'plasma')

    @staticmethod
    def invcycloid():
        """
        Plots the Involute of a Cycloid.
        Unwinding a cycloid arch gives another cycloid of the same size. Huygens used this for his isochronous pendulum clock[cite: 4, 6].

        Output:
            matplotlib.figure.Figure: A 3D plot of a cycloid and its involute.
            
        Real-Life Examples:
            1. Physics: The geometric basis for Huygens' isochronous pendulum, where the bob swings with a period independent of amplitude[cite: 4, 6].
            2. Horology: Clock escapements designed for perfect timekeeping regardless of mainspring tension[cite: 6].
        """
        def cyc(t): return [t + np.sin(t), np.cos(t) - 1]
        
        t_vals = np.arange(0, 2 * np.pi, 0.03)
        base = np.array([cyc(t) for t in t_vals])
        inv = InvolutesEvolutes._involute(cyc, 0, 2 * np.pi, 0.01, 0)
        
        return InvolutesEvolutes._plot_bundle([base, inv], 'Involute of a Cycloid', 'viridis')

    @staticmethod
    def invcatenary():
        """
        Plots the Involute of a Catenary (Tractrix).
        Unwind a hanging chain from its lowest point and the free end draws a tractrix[cite: 4, 6].

        Output:
            matplotlib.figure.Figure: A 3D plot of a catenary and its tractrix involute.
            
        Real-Life Examples:
            1. Architecture/Engineering: Links the shape of a hanging chain directly to the optimal friction-bearing pivot curve[cite: 4, 6].
            2. Mathematics: A classic demonstration of how different named curves are intimately connected via calculus[cite: 6].
        """
        def cat(t): return [t, np.cosh(t)]
        
        t_vals = np.arange(-3, 3, 0.05)
        base = np.array([cat(t) for t in t_vals])
        inv = InvolutesEvolutes._involute(cat, -3, 3, 0.01, 0)
        
        return InvolutesEvolutes._plot_bundle([base, inv], 'Involute of a Catenary (Tractrix)', 'terrain')

    @staticmethod
    def invhelicoid(u_steps=40, v_steps=60):
        """
        Plots an Involute Helicoid (helical gear flank).
        Sweep an involute up the axis while turning it and you get the tooth flank of a helical gear[cite: 4, 6].

        Inputs:
            u_steps (int): Resolution for the involute parameter (default 40)[cite: 4, 6].
            v_steps (int): Resolution for the axial sweep parameter (default 60)[cite: 4, 6].
            
        Output:
            matplotlib.figure.Figure: A 3D surface plot.
            
        Real-Life Examples:
            1. Automotive: The continuous, sweeping contact surface of quiet, high-load helical gears in transmissions[cite: 4, 6].
            2. Pumps: The internal rotor geometry for screw pumps and twin-screw compressors.
        """
        u = np.linspace(0, 1.3, u_steps)
        v = np.linspace(0, 6, v_steps)
        U, V = np.meshgrid(u, v)
        
        bx = np.cos(U) + U * np.sin(U)
        by = np.sin(U) - U * np.cos(U)
        a = 0.45 * V
        
        X = bx * np.cos(a) - by * np.sin(a)
        Y = bx * np.sin(a) + by * np.cos(a)
        Z = V
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='plasma', edgecolor='none')
        ax.set_aspect("equal")
        ax.set_title('Involute Helicoid (helical gear flank)')
        return fig

    @staticmethod
    def ellipseoffsets():
        """
        Plots Parallel Curves of an Ellipse.
        Offsetting an ellipse by distance d. Inward offsets past the radius of curvature grow cusps, tracing out the evolute[cite: 4, 6].

        Output:
            matplotlib.figure.Figure: A 3D plot of an ellipse and its parallel offsets.
            
        Real-Life Examples:
            1. CNC Machining: Toolpath generation where a cutting tool follows the offset curve of a desired elliptical profile[cite: 6].
            2. Road Design: The parallel lanes bounding an elliptical track or plaza.
        """
        curves = []
        t = np.arange(0, 2 * np.pi, 0.02)
        
        for d in [-0.8, -0.5, -0.25, 0, 0.4, 0.8, 1.2]:
            N = np.hypot(np.cos(t), 2 * np.sin(t))
            x = 2 * np.cos(t) + d * np.cos(t) / N
            y = np.sin(t) + d * 2 * np.sin(t) / N
            curves.append(np.column_stack([x, y]))
            
        return InvolutesEvolutes._plot_bundle(curves, 'Parallel Curves of an Ellipse', 'hsv')

    @staticmethod
    def _evolute_pair(base_func, ev_func, a, b, title, cmap):
        """Helper to plot a base curve, its evolute, and the connecting normals[cite: 4, 6]."""
        t_vals = np.arange(a, b, 0.02)
        base = np.array([base_func(t) for t in t_vals])
        evolute = np.array([ev_func(t) for t in t_vals])
        
        curves = [base, evolute]
        
        # Add normal lines
        t_normals = np.linspace(a, b, 16)
        for t in t_normals:
            p_base = base_func(t)
            p_ev = ev_func(t)
            curves.append(np.array([p_base, p_ev]))
            
        return InvolutesEvolutes._plot_bundle(curves, title, cmap)

    @staticmethod
    def evparabola():
        """
        Plots a Parabola and its Evolute.
        The evolute of a parabola is Neile's semicubical parabola, with a cusp at the focus-side of the vertex[cite: 4, 6].

        Output:
            matplotlib.figure.Figure: 3D plot of a parabola, its evolute, and normal lines.
        """
        def base(t): return [t, t**2]
        def ev(t): return [-4 * t**3, 3 * t**2 + 0.5]
        return InvolutesEvolutes._evolute_pair(base, ev, -1, 1, 'Parabola and its Evolute', 'coolwarm')

    @staticmethod
    def evellipse():
        """
        Plots an Ellipse and its Evolute.
        The centres of curvature of an ellipse form a stretched astroid with four cusps[cite: 4, 6].

        Output:
            matplotlib.figure.Figure: 3D plot of an ellipse, its astroid evolute, and normal lines.
        """
        def base(t): return [2 * np.cos(t), np.sin(t)]
        def ev(t): return [1.5 * np.cos(t)**3, -3 * np.sin(t)**3]
        return InvolutesEvolutes._evolute_pair(base, ev, 0, 2 * np.pi, 'Ellipse and its Evolute', 'hsv')

    @staticmethod
    def evcycloid():
        """
        Plots a Cycloid and its Evolute.
        The evolute of a cycloid is an identical cycloid shifted down and sideways[cite: 4, 6].

        Output:
            matplotlib.figure.Figure: 3D plot of a cycloid, its identical evolute, and normal lines.
        """
        def base(t): return [t - np.sin(t), 1 - np.cos(t)]
        def ev(t): return [t + np.sin(t), np.cos(t) - 1]
        return InvolutesEvolutes._evolute_pair(base, ev, 0, 2 * np.pi, 'Cycloid and its Evolute', 'viridis')

    @staticmethod
    def evcatenary():
        """
        Plots a Catenary and its Evolute.
        The centres of curvature of a hanging chain trace a curve that rises steeply on both sides[cite: 4, 6].

        Output:
            matplotlib.figure.Figure: 3D plot of a catenary, its evolute, and normal lines.
        """
        def base(t): return [t, np.cosh(t)]
        def ev(t): return [t - np.sinh(t) * np.cosh(t), 2 * np.cosh(t)]
        return InvolutesEvolutes._evolute_pair(base, ev, -1.6, 1.6, 'Catenary and its Evolute', 'terrain')

    @staticmethod
    def evastroid():
        """
        Plots an Astroid and its Evolute.
        The evolute of an astroid is another astroid, twice as large and turned 45 degrees[cite: 4, 6].

        Output:
            matplotlib.figure.Figure: 3D plot of an astroid, its enlarged evolute, and normal lines.
        """
        def base(t): return [np.cos(t)**3, np.sin(t)**3]
        def ev(t): return [np.cos(t)**3 + 3 * np.cos(t) * np.sin(t)**2, 
                          np.sin(t)**3 + 3 * np.sin(t) * np.cos(t)**2]
        return InvolutesEvolutes._evolute_pair(base, ev, 0, 2 * np.pi, 'Astroid and its Evolute', 'plasma')


if __name__ == "__main__":
    cycloidObj = EngineeringCurves()
    fig = cycloidObj.cycloid()

    plt.show()