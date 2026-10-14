/* ---------- Helpers ---------- */
const T = String.raw;
const CY = [[0, '#0b1d3a'], [.5, '#1fb5c9'], [1, '#e9fffb']];

const generateGrid = (xMin, xMax, xs, yMin, yMax, ys, f) => {
  const x = [], y = [], z = [];
  for (let i = xMin; i <= xMax + 1e-9; i += xs) x.push(i);
  for (let j = yMin; j <= yMax + 1e-9; j += ys) y.push(j);
  for (const yy of y) z.push(x.map(xx => f(xx, yy)));
  return { x, y, z };
};

const generateParametric = (u0, u1, un, v0, v1, vn, f) => {
  const x = [], y = [], z = [];
  for (let i = 0; i <= un; i++) {
    const u = u0 + i * (u1 - u0) / un, rx = [], ry = [], rz = [];
    for (let j = 0; j <= vn; j++) {
      const p = f(u, v0 + j * (v1 - v0) / vn);
      rx.push(p.x); ry.push(p.y); rz.push(p.z);
    }
    x.push(rx); y.push(ry); z.push(rz);
  }
  return { x, y, z };
};

const generateAttractor = (steps, dt, init, f) => {
  const x = [], y = [], z = [];
  let [a, b, c] = init;
  for (let i = 0; i < steps; i++) {
    const [dx, dy, dz] = f(a, b, c);
    a += dx * dt; b += dy * dt; c += dz * dt;
    x.push(a); y.push(b); z.push(c);
  }
  return { x, y, z };
};

const polyline = (t0, t1, dt, f) => {
  const x = [], y = [], z = [];
  for (let t = t0; t <= t1; t += dt) { const p = f(t); x.push(p[0]); y.push(p[1]); z.push(p[2]); }
  return { x, y, z };
};

/* ---------- Model registry ---------- */
const M = {};
const reg = (k, group, name, eq, desc, gen) => { M[k] = { group, name, equation: '$$' + eq + '$$', description: desc, generate: gen }; };
const surf = (k, g, n, eq, d, cs, f) => reg(k, g, n, eq, d, () => ({ data: [{ ...f(), type: 'surface', colorscale: cs, showscale: false }] }));
const curve = (k, g, n, eq, d, cs, w, f) => reg(k, g, n, eq, d, () => { const p = f(); return { data: [{ ...p, type: 'scatter3d', mode: 'lines', line: { color: p.z, colorscale: cs, width: w } }] }; });
const att = (k, n, eq, d, cs, steps, dt, init, fn) => curve(k, 'Attractors', n, eq, d, cs, 2.5, () => generateAttractor(steps, dt, init, fn));
const G = (a, b, s, f) => () => generateGrid(a, b, s, a, b, s, f);
const P = (u0, u1, un, v0, v1, vn, f) => () => generateParametric(u0, u1, un, v0, v1, vn, f);

/* Surfaces */
surf('sinc', 'Surfaces', 'The Sinc Function', T`z=\frac{\sin R}{R},\; R=\sqrt{x^2+y^2}`,
  'A mathematical raindrop: perfectly decaying concentric ripples, and the ideal interpolation filter in signal processing.', CY,
  G(-10, 10, .4, (x, y) => { const r = Math.hypot(x, y) + 1e-4; return Math.sin(r) / r; }));
surf('saddle', 'Surfaces', 'Hyperbolic Paraboloid', T`z=x^2-y^2`,
  'The saddle point: curving up in one direction and down in the other. Optimizers can stall here during gradient descent.', 'Plasma',
  G(-5, 5, .2, (x, y) => x * x - y * y));
surf('monkey', 'Surfaces', 'Monkey Saddle', T`z=x^3-3xy^2`,
  'A saddle with three descents instead of two, enough room for a monkey\'s legs and tail.', 'Portland',
  G(-2, 2, .08, (x, y) => x ** 3 - 3 * x * y * y));
surf('dropwave', 'Surfaces', 'Drop-Wave Function', T`f=-\frac{1+\cos(12\sqrt{x^2+y^2})}{0.5(x^2+y^2)+2}`,
  'The splash of a water drop: multimodal, symmetrical and a good stress test for optimizers.', CY,
  G(-5.12, 5.12, .15, (x, y) => { const r2 = x * x + y * y; return -(1 + Math.cos(12 * Math.sqrt(r2))) / (.5 * r2 + 2); }));
surf('eggcarton', 'Surfaces', 'Egg Carton Surface', T`z=\sin x\cos y`,
  'A repeating lattice of peaks and pits: a 2D standing-wave interference pattern.', 'Portland',
  G(-10, 10, .3, (x, y) => Math.sin(x) * Math.cos(y)));

/* Distributions */
const D = 'Distributions';
const GR = (xa, xb, xs, ya, yb, ys, f) => () => generateGrid(xa, xb, xs, ya, yb, ys, f);
const lnG = z => {
  if (z < .5) return Math.log(Math.PI / Math.abs(Math.sin(Math.PI * z))) - lnG(1 - z);
  const c = [.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059, 12.507343278686905, -.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
  z -= 1; let a = c[0]; const t = z + 7.5;
  for (let i = 1; i < 9; i++) a += c[i] / (z + i);
  return .5 * Math.log(2 * Math.PI) + (z + .5) * Math.log(t) - t + Math.log(a);
};
const erf = x => {
  const s = Math.sign(x), t = 1 / (1 + .3275911 * Math.abs(x));
  return s * (1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - .284496736) * t + .254829592) * t * Math.exp(-x * x));
};
const Phi = x => .5 * (1 + erf(x / Math.SQRT2));
const gauss2 = (x, y, mx, my, s) => Math.exp(-((x - mx) ** 2 + (y - my) ** 2) / (2 * s * s)) / (2 * Math.PI * s * s);

surf('gaussian', D, 'Bivariate Gaussian', T`f(x,y)=\frac{1}{2\pi\sigma^2}e^{-\frac{x^2+y^2}{2\sigma^2}}`,
  'The bell curve extended into 3D, a foundation of statistics that appears everywhere from quantum mechanics to populations.', 'Viridis',
  G(-6, 6, .25, (x, y) => Math.exp(-(x * x + y * y) / 8) / (8 * Math.PI)));
surf('corrnormal', D, 'Correlated Normal (ρ = 0.8)', T`f=\frac{1}{2\pi\sqrt{1-\rho^2}}\exp\!\left(-\frac{x^2-2\rho xy+y^2}{2(1-\rho^2)}\right)`,
  'Strong positive correlation squeezes the bell into a long ridge along the diagonal.', 'Plasma',
  G(-3.5, 3.5, .1, (x, y) => Math.exp(-(x * x - 1.6 * x * y + y * y) / .72) / (2 * Math.PI * .6)));
surf('gmm', D, 'Gaussian Mixture', T`f(\mathbf x)=\sum_{k=1}^{3}\pi_k\,\mathcal N(\mathbf x\mid\boldsymbol\mu_k,\sigma_k^2 I)`,
  'Three weighted Gaussians: the standard model for clustered data and the engine behind soft clustering.', 'Portland',
  G(-5, 5, .12, (x, y) => .35 * gauss2(x, y, -2, -2, .8) + .4 * gauss2(x, y, 2, 1.5, 1) + .25 * gauss2(x, y, -1, 2.5, .7)));
surf('skewnormal', D, 'Bivariate Skew-Normal', T`f(x,y)=2\,\phi(x)\phi(y)\,\Phi(\alpha_1x+\alpha_2y)`,
  'A Gaussian tilted by its own CDF: one flank is steep, the other trails off in a long shoulder.', 'Viridis',
  G(-4, 4, .1, (x, y) => Math.exp(-(x * x + y * y) / 2) / Math.PI * Phi(3 * x + y)));
surf('student2d', D, "Bivariate Student's t (ν = 3)", T`f=\frac{\Gamma(\frac{\nu+2}{2})}{\Gamma(\frac\nu2)\,\nu\pi}\left(1+\frac{x^2+y^2}{\nu}\right)^{-\frac{\nu+2}{2}}`,
  'A sharper peak than the Gaussian with heavy tails, so extreme values are far more likely.', 'Magma',
  G(-6, 6, .15, (x, y) => Math.exp(lnG(2.5) - lnG(1.5)) / (3 * Math.PI) * (1 + (x * x + y * y) / 3) ** -2.5));
surf('cauchy2d', D, 'Bivariate Cauchy', T`f=\frac{1}{2\pi}\left(1+x^2+y^2\right)^{-3/2}`,
  'So heavy-tailed that its mean and variance do not exist. Outliers are part of the shape.', 'Electric',
  G(-6, 6, .15, (x, y) => (1 + x * x + y * y) ** -1.5 / (2 * Math.PI)));
surf('laplace2d', D, 'Bivariate Laplace', T`f=\tfrac14\,e^{-(|x|+|y|)}`,
  'Two independent double exponentials form a pyramid with a sharp peak and diamond-shaped contours.', 'Inferno',
  G(-6, 6, .15, (x, y) => Math.exp(-(Math.abs(x) + Math.abs(y))) / 4));
surf('logistic2d', D, 'Bivariate Logistic (Gumbel)', T`f=\frac{2\,e^{-x-y}}{\left(1+e^{-x}+e^{-y}\right)^{3}}`,
  'A skewed, bulky peak with exponential tails, from Gumbel\'s bivariate logistic family.', 'Jet',
  G(-6, 6, .2, (x, y) => 2 * Math.exp(-x - y) / (1 + Math.exp(-x) + Math.exp(-y)) ** 3));
surf('lognormal2d', D, 'Bivariate Log-Normal', T`f=\frac{1}{2\pi\sigma^2xy}\exp\!\left(-\frac{\ln^2x+\ln^2y}{2\sigma^2}\right)`,
  'Multiplicative effects pile up on a log scale: a hump against the axes with a long right-hand tail.', 'Earth',
  GR(.03, 4, .08, .03, 4, .08, (x, y) => Math.exp(-(Math.log(x) ** 2 + Math.log(y) ** 2) / .72) / (2 * Math.PI * .36 * x * y)));
surf('normalgamma', D, 'Normal-Gamma', T`f(\mu,\tau)=\frac{b^a\sqrt\lambda}{\Gamma(a)\sqrt{2\pi}}\,\tau^{a-\frac12}e^{-b\tau}e^{-\frac{\lambda\tau(\mu-\mu_0)^2}{2}}`,
  'A Bayesian prior over a mean μ and a precision τ. Notice how the spread in μ narrows as τ grows.', 'Plasma',
  GR(-3, 3, .08, 0, 4, .06, (m, t) => .3989 * t ** 1.5 * Math.exp(-t - t * m * m / 2)));
surf('dirichlet', D, 'Dirichlet (α = 3, 5, 4)', T`f(\mathbf p)=\frac{\Gamma(\sum\alpha_i)}{\prod\Gamma(\alpha_i)}\prod_i p_i^{\alpha_i-1}`,
  'A distribution over probabilities that sum to 1. The base is the triangle of all possible three-way splits, shown here in (p₁, p₂).', 'Viridis',
  G(0, 1, .02, (x, y) => { const p = 1 - x - y; return p < -1e-9 ? null : 138600 * x ** 2 * y ** 4 * Math.max(p, 0) ** 3; }));
surf('vonmises', D, 'Bivariate von Mises (torus)', T`f(\phi,\psi)\propto\exp\!\big(\kappa_1\cos\phi+\kappa_2\cos\psi+\lambda\sin\phi\sin\psi\big)`,
  'A distribution over two angles, where the edges wrap around. It is used for protein backbone angles. Shown unnormalized.', 'Portland',
  G(-Math.PI, Math.PI, .1, (p, q) => Math.exp(2 * Math.cos(p) + 2 * Math.cos(q) + 1.5 * Math.sin(p) * Math.sin(q))));
surf('clayton', D, 'Clayton Copula Density (θ = 2)', T`c(u,v)=(1+\theta)(uv)^{-1-\theta}\left(u^{-\theta}+v^{-\theta}-1\right)^{-2-\frac1\theta}`,
  'Models dependence with no marginals attached: strong lower-tail dependence, so variables crash together. Capped at 20.', 'Magma',
  G(.03, 1, .02, (u, v) => Math.min(20, 3 * (u * v) ** -3 * (u ** -2 + v ** -2 - 1) ** -2.5)));
surf('banana', D, 'Banana (Twisted Gaussian)', T`f(x,y)=\frac{1}{2\pi}\exp\!\left(-\frac{x^2}{8}-2\left(y-\frac{x^2}{4}\right)^2\right)`,
  'A curved ridge that is a classic hard target for MCMC samplers, which struggle to follow its bend.', 'Jet',
  GR(-5, 5, .1, -2, 8, .12, (x, y) => Math.exp(-x * x / 8 - 2 * (y - x * x / 4) ** 2) / (2 * Math.PI)));
surf('funnel', D, "Neal's Funnel", T`f(x,y)=\mathcal N(y\mid0,3^2)\;\mathcal N(x\mid0,e^{y})`,
  'The geometry of hierarchical models: wide and gentle at the top, a razor-thin neck at the bottom.', 'Electric',
  G(-4, 4, .08, (x, y) => Math.exp(-y * y / 18 - x * x / (2 * Math.exp(y))) / (3 * 2 * Math.PI * Math.exp(y / 2))));

/* Distribution families: density over (x, parameter) */
surf('gammafam', D, 'Gamma Family (shape k)', T`f(x;k)=\frac{x^{k-1}e^{-x}}{\Gamma(k)}`,
  'Shape k runs from 1 to 9. At k = 1 it is the exponential, and as k grows it slides right and turns bell-shaped.', 'Viridis',
  GR(0, 12, .15, 1, 9, .1, (x, k) => Math.exp((k - 1) * Math.log(Math.max(x, 1e-9)) - x - lnG(k))));
surf('betafam', D, 'Beta Family (α, β = 3)', T`f(x;\alpha)=\frac{x^{\alpha-1}(1-x)^{2}}{B(\alpha,3)}`,
  'The distribution of probabilities themselves. Raising α pushes the mass from the left edge to the right.', 'Plasma',
  GR(.01, .99, .01, 1, 8, .1, (x, a) => Math.exp((a - 1) * Math.log(x) + 2 * Math.log(1 - x) - lnG(a) - lnG(3) + lnG(a + 3))));
surf('tfam', D, "Student's t Family (ν)", T`f(x;\nu)=\frac{\Gamma(\frac{\nu+1}{2})}{\sqrt{\nu\pi}\,\Gamma(\frac\nu2)}\left(1+\frac{x^2}{\nu}\right)^{-\frac{\nu+1}{2}}`,
  'Degrees of freedom ν from 0.5 to 30. Watch the heavy tails thin out as the curve converges on the normal.', 'Earth',
  GR(-5, 5, .1, .5, 30, .5, (x, v) => Math.exp(lnG((v + 1) / 2) - lnG(v / 2)) / Math.sqrt(v * Math.PI) * (1 + x * x / v) ** (-(v + 1) / 2)));
surf('chisqfam', D, 'Chi-Squared Family (k)', T`f(x;k)=\frac{x^{k/2-1}e^{-x/2}}{2^{k/2}\Gamma(k/2)}`,
  'Sums of squared normals. More degrees of freedom k shift the mass right and flatten the peak.', 'Portland',
  GR(0, 30, .4, 2, 14, .15, (x, k) => Math.exp((k / 2 - 1) * Math.log(Math.max(x, 1e-9)) - x / 2 - k / 2 * Math.LN2 - lnG(k / 2))));
surf('weibullfam', D, 'Weibull Family (shape k)', T`f(x;k)=k\,x^{k-1}e^{-x^{k}}`,
  'The distribution of lifetimes and failure times. Shape k below 2 means early failures, and above it wear-out.', 'Magma',
  GR(0, 3, .04, 1, 6, .1, (x, k) => k * Math.max(x, 1e-9) ** (k - 1) * Math.exp(-(x ** k))));
surf('poissonfam', D, 'Poisson Family (rate λ)', T`P(k;\lambda)=\frac{\lambda^{k}e^{-\lambda}}{\Gamma(k+1)}`,
  'Counts of rare events. The true distribution lives on whole numbers, so this smooth surface is its continuous extension via Γ.', 'Jet',
  GR(0, 20, .25, .5, 15, .2, (k, l) => Math.exp(k * Math.log(l) - l - lnG(k + 1))));

/* Optimization landscapes */
const O = 'Optimization Landscapes';
surf('rastrigin', O, 'Rastrigin Function', T`f=20+x^2-10\cos 2\pi x+y^2-10\cos 2\pi y`,
  'A highly multimodal function with countless local minima hiding a single global minimum at the center.', 'Earth',
  G(-5.12, 5.12, .15, (x, y) => 20 + x * x - 10 * Math.cos(2 * Math.PI * x) + y * y - 10 * Math.cos(2 * Math.PI * y)));
surf('rosenbrock', O, 'Rosenbrock Valley', T`f=(1-x)^2+100(y-x^2)^2`,
  'The banana valley: finding the valley is easy, crawling along its flat floor to the minimum is not.', 'Magma',
  () => generateGrid(-2, 2, .1, -1, 3, .1, (x, y) => (1 - x) ** 2 + 100 * (y - x * x) ** 2));
surf('ackley', O, 'Ackley Function', T`f=-20e^{-0.2\sqrt{0.5(x^2+y^2)}}-e^{0.5(\cos 2\pi x+\cos 2\pi y)}+e+20`,
  'A flat outer region full of shallow ripples that plunges into one deep valley.', 'Portland',
  G(-8, 8, .3, (x, y) => -20 * Math.exp(-.2 * Math.sqrt(.5 * (x * x + y * y))) - Math.exp(.5 * (Math.cos(2 * Math.PI * x) + Math.cos(2 * Math.PI * y))) + Math.E + 20));
surf('himmelblau', O, "Himmelblau's Function", T`f=(x^2+y-11)^2+(x+y^2-7)^2`,
  'A polynomial landscape with four identical global minima where the surface touches zero.', 'Electric',
  G(-5, 5, .2, (x, y) => (x * x + y - 11) ** 2 + (x + y * y - 7) ** 2));
surf('beale', O, 'Beale Function', T`f=(1.5-x+xy)^2+(2.25-x+xy^2)^2+(2.625-x+xy^3)^2`,
  'Sharp walls with a very flat region near the minimum. Heights are capped so the valley stays visible.', 'Jet',
  G(-4.5, 4.5, .15, (x, y) => Math.min(200, (1.5 - x + x * y) ** 2 + (2.25 - x + x * y * y) ** 2 + (2.625 - x + x * y ** 3) ** 2)));
surf('crossintray', O, 'Cross-in-Tray Function', T`f=-10^{-4}\left(\left|\sin x\sin y\,e^{\left|100-\frac{\sqrt{x^2+y^2}}{\pi}\right|}\right|+1\right)^{0.1}`,
  'A canopy-like surface with four identical global minima around its central cross.', 'Picnic',
  G(-10, 10, .2, (x, y) => -1e-4 * (Math.abs(Math.sin(x) * Math.sin(y) * Math.exp(Math.abs(100 - Math.hypot(x, y) / Math.PI))) + 1) ** .1));

/* Parametric surfaces */
const S = 'Parametric Surfaces';
surf('torus', S, 'The Torus', T`x=(R+r\cos v)\cos u,\; y=(R+r\cos v)\sin u,\; z=r\sin v`,
  'The mathematical donut: a circle revolved around an axis in its own plane.', 'Viridis',
  P(0, 2 * Math.PI, 60, 0, 2 * Math.PI, 40, (u, v) => ({ x: (3 + Math.cos(v)) * Math.cos(u), y: (3 + Math.cos(v)) * Math.sin(u), z: Math.sin(v) })));
surf('mobius', S, 'Möbius Strip', T`x=\left(1+\tfrac v2\cos\tfrac u2\right)\cos u,\; y=\left(1+\tfrac v2\cos\tfrac u2\right)\sin u`,
  'One side, one edge. Trace its center line and you visit both "sides" before returning home.', 'Plasma',
  P(0, 2 * Math.PI, 80, -1, 1, 20, (u, v) => ({ x: (1 + v / 2 * Math.cos(u / 2)) * Math.cos(u), y: (1 + v / 2 * Math.cos(u / 2)) * Math.sin(u), z: v / 2 * Math.sin(u / 2) })));
surf('helicoid', S, 'Helicoid', T`x=u\cos v,\; y=u\sin v,\; z=cv`,
  'A spiral staircase that locally minimizes area. Apart from the plane, it is the only ruled minimal surface.', 'Magma',
  P(-3, 3, 40, -2 * Math.PI, 2 * Math.PI, 80, (u, v) => ({ x: u * Math.cos(v), y: u * Math.sin(v), z: .5 * v })));
surf('catenoid', S, 'Catenoid', T`x=c\cosh\tfrac vc\cos u,\; y=c\cosh\tfrac vc\sin u,\; z=v`,
  'Found by Euler in 1744: the shape of a soap film stretched between two rings, and the first non-trivial minimal surface.', 'Earth',
  P(0, 2 * Math.PI, 60, -2, 2, 40, (u, v) => ({ x: Math.cosh(v) * Math.cos(u), y: Math.cosh(v) * Math.sin(u), z: v })));
surf('enneper', S, 'Enneper Surface', T`x=u-\tfrac{u^3}{3}+uv^2,\; y=v-\tfrac{v^3}{3}+vu^2,\; z=u^2-v^2`,
  'A self-intersecting minimal surface with elegant symmetry, a staple of differential geometry.', 'Inferno',
  P(-2, 2, 50, -2, 2, 50, (u, v) => ({ x: u * (1 - u * u / 3 + v * v) / 3, y: -v * (1 - v * v / 3 + u * u) / 3, z: (u * u - v * v) / 3 })));
surf('sphere', S, 'Parametric Sphere', T`x=r\sin u\cos v,\; y=r\sin u\sin v,\; z=r\cos u`,
  'The simplest closed 3D manifold, drawn through spherical coordinates.', 'Electric',
  P(0, Math.PI, 40, 0, 2 * Math.PI, 60, (u, v) => ({ x: 2 * Math.sin(u) * Math.cos(v), y: 2 * Math.sin(u) * Math.sin(v), z: 2 * Math.cos(u) })));
surf('dini', S, "Dini's Surface", T`x=\cos u\sin v,\; y=\sin u\sin v,\; z=\cos v+\ln\tan\tfrac v2+cu`,
  'Constant negative curvature in a twisted, spiraling pseudosphere.', 'Viridis',
  P(0, 4 * Math.PI, 80, .01, 2, 40, (u, v) => ({ x: Math.cos(u) * Math.sin(v), y: Math.sin(u) * Math.sin(v), z: Math.cos(v) + Math.log(Math.tan(v / 2)) + .2 * u })));
surf('roman', S, "Steiner's Roman Surface", T`x=r^2\cos u\cos v\sin v,\; y=r^2\sin u\cos v\sin v,\; z=r^2\cos u\sin u\cos^2 v`,
  'Steiner\'s 1852 map of the projective plane into 3D, with self-intersections and pinch points.', 'Plasma',
  P(0, Math.PI, 60, 0, Math.PI / 2, 60, (u, v) => ({ x: 4 * Math.cos(u) * Math.cos(v) * Math.sin(v), y: 4 * Math.sin(u) * Math.cos(v) * Math.sin(v), z: 4 * Math.cos(u) * Math.sin(u) * Math.cos(v) ** 2 })));
surf('klein', S, 'Figure-8 Klein Bottle', T`x=\left(r+\cos\tfrac u2\sin v-\sin\tfrac u2\sin 2v\right)\cos u`,
  'A non-orientable surface with no inside or outside, immersed in 3D as a figure-8.', 'Magma',
  P(0, 2 * Math.PI, 60, 0, 2 * Math.PI, 60, (u, v) => {
    const c = 2 + Math.cos(u / 2) * Math.sin(v) - Math.sin(u / 2) * Math.sin(2 * v);
    return { x: c * Math.cos(u), y: c * Math.sin(u), z: Math.sin(u / 2) * Math.sin(v) + Math.cos(u / 2) * Math.sin(2 * v) };
  }));
surf('catalan', S, "Catalan's Surface", T`x=u-\sin u\cosh v,\; y=1-\cos u\cosh v,\; z=4\sin\tfrac u2\sinh\tfrac v2`,
  'A periodic minimal surface from 1855 that contains real cycloids.', 'Earth',
  P(-Math.PI, Math.PI, 60, -2, 2, 40, (u, v) => ({ x: u - Math.sin(u) * Math.cosh(v), y: 1 - Math.cos(u) * Math.cosh(v), z: 4 * Math.sin(u / 2) * Math.sinh(v / 2) })));
surf('seashell', S, 'Seashell', T`x=2(1-e^{\frac{v}{6\pi}})\cos v\cos^2\tfrac u2,\; z=1-e^{\frac{v}{3\pi}}-\sin u+e^{\frac{v}{6\pi}}\sin u`,
  'An exponentially growing spiral tube, the same logarithmic growth law real mollusks follow.', 'Plasma',
  P(0, 2 * Math.PI, 50, 0, 6 * Math.PI, 120, (u, v) => {
    const e = Math.exp(v / (6 * Math.PI)), c = Math.cos(u / 2) ** 2;
    return { x: 2 * (1 - e) * Math.cos(v) * c, y: 2 * (e - 1) * Math.sin(v) * c, z: 1 - Math.exp(v / (3 * Math.PI)) - Math.sin(u) + e * Math.sin(u) };
  }));

/* 3D curves & knots */
const K = '3D Curves & Knots';
curve('trefoil', K, 'Trefoil Knot', T`x=\sin t+2\sin 2t,\; y=\cos t-2\cos 2t,\; z=-\sin 3t`,
  'The simplest nontrivial knot. It cannot be untied without cutting, the starting point of knot theory.', CY, 10,
  () => polyline(0, 2.05 * Math.PI, .02, t => [Math.sin(t) + 2 * Math.sin(2 * t), Math.cos(t) - 2 * Math.cos(2 * t), -Math.sin(3 * t)]));
curve('torusknot', K, 'Torus Knot (3,5)', T`x=r\cos 3t,\; y=r\sin 3t,\; z=-\sin 5t,\quad r=2+\cos 5t`,
  'A curve that winds 3 times around a torus the long way and 5 times the short way before closing.', 'Rainbow', 8,
  () => polyline(0, 2.01 * Math.PI, .01, t => { const r = 2 + Math.cos(5 * t); return [r * Math.cos(3 * t), r * Math.sin(3 * t), -Math.sin(5 * t)]; }));
curve('lissajous3d', K, '3D Lissajous Curve', T`x=\sin(3t+\tfrac\pi2),\; y=\sin 4t,\; z=\sin 5t`,
  'Three coupled harmonic oscillations tracing a closed, woven path.', 'Rainbow', 6,
  () => polyline(0, 2.05 * Math.PI, .01, t => [Math.sin(3 * t + Math.PI / 2), Math.sin(4 * t), Math.sin(5 * t)]));
curve('viviani', K, "Viviani's Curve", T`x=1+\cos t,\; y=\sin t,\; z=2\sin\tfrac t2`,
  'The figure-8 where a sphere meets a cylinder passing through its center.', 'Portland', 8,
  () => polyline(0, 4.02 * Math.PI, .02, t => [1 + Math.cos(t), Math.sin(t), 2 * Math.sin(t / 2)]));
curve('sphspiral', K, 'Spherical Spiral', T`x=\sin u\cos 12u,\; y=\sin u\sin 12u,\; z=\cos u`,
  'A path that winds from pole to pole, crossing every line of longitude at a steady rate.', 'Viridis', 6,
  () => polyline(0, Math.PI, .004, u => [Math.sin(u) * Math.cos(12 * u), Math.sin(u) * Math.sin(12 * u), Math.cos(u)]));
curve('conespiral', K, 'Conical Spiral', T`x=t\cos 6t,\; y=t\sin 6t,\; z=t`,
  'A helix whose radius grows with height, wrapping the surface of a cone.', 'Plasma', 6,
  () => polyline(0, 5, .01, t => [t * Math.cos(6 * t), t * Math.sin(6 * t), t]));

/* Engineering curves
   Paste this whole block into script.js, right before the "/* Attractors */" comment.
   Uses helpers already in your script: T, CY, reg, polyline. */
const E = 'Engineering Curves';

// Flat curve in the XY plane, coloured along its path
const plane = (k, n, eq, d, cs, w, t0, t1, dt, f) => reg(k, E, n, eq, d, () => {
  const p = polyline(t0, t1, dt, t => [...f(t), 0]);
  return { data: [{ ...p, type: 'scatter3d', mode: 'lines', line: { color: Array.from(p.x, (_, i) => i), colorscale: cs, width: w } }] };
});

// Rolling-circle families: R = fixed circle, r = rolling circle, d = pen distance
const epi = (R, r, d) => t => [(R + r) * Math.cos(t) - d * Math.cos((R + r) / r * t), (R + r) * Math.sin(t) - d * Math.sin((R + r) / r * t)];
const hypo = (R, r, d) => t => [(R - r) * Math.cos(t) + d * Math.cos((R - r) / r * t), (R - r) * Math.sin(t) - d * Math.sin((R - r) / r * t)];
const pe = p => T`x=(R+r)\cos t-d\cos\tfrac{R+r}{r}t,\; y=(R+r)\sin t-d\sin\tfrac{R+r}{r}t\;\;(R,r,d)=(${p})`;
const ph = p => T`x=(R-r)\cos t+d\cos\tfrac{R-r}{r}t,\; y=(R-r)\sin t-d\sin\tfrac{R-r}{r}t\;\;(R,r,d)=(${p})`;
const polar = g => t => [g(t) * Math.cos(t), g(t) * Math.sin(t)];
const TAU = 2 * Math.PI;

// Fresnel integrals by Simpson's rule (for the Euler spiral)
const fres = t => {
  const n = 2 * Math.ceil(Math.abs(t) * 25 + 1), h = t / n;
  let c = 0, s = 0;
  for (let i = 0; i <= n; i++) {
    const w = i === 0 || i === n ? 1 : i % 2 ? 4 : 2, u = i * h;
    c += w * Math.cos(Math.PI * u * u / 2); s += w * Math.sin(Math.PI * u * u / 2);
  }
  return [c * h / 3, s * h / 3];
};

// Four-bar linkage: crank 1, coupler 3, rocker 3, ground 3; t is the crank angle
const fourbar = t => {
  const ax = Math.cos(t), ay = Math.sin(t), dx = 3 - ax, dy = -ay, L = Math.hypot(dx, dy);
  const a = L / 2, h = Math.sqrt(9 - a * a), ux = dx / L, uy = dy / L;
  const vx = (a * ux - h * uy) / 3, vy = (a * uy + h * ux) / 3, c = Math.cos(.5), s = Math.sin(.5);
  return [ax + 3.5 * (vx * c - vy * s), ay + 3.5 * (vx * s + vy * c)];
};

/* Cycloids and trochoids */
plane('cycloid', 'Cycloid', T`x=r(t-\sin t),\; y=r(1-\cos t)`,
  'The path of a point on a rolling wheel\'s rim. Its arches are also the profile behind cycloidal gears.', 'Plasma', 6, 0, 6 * Math.PI, .02,
  t => [t - Math.sin(t), 1 - Math.cos(t)]);
plane('brachistochrone', 'Brachistochrone (Tautochrone)', T`x=r(t-\sin t),\; y=r(\cos t-1)`,
  'An upside-down cycloid: the frictionless slide that gets a bead from A to B fastest, and in equal time from anywhere on the curve.', 'Viridis', 6, 0, TAU, .01,
  t => [t - Math.sin(t), Math.cos(t) - 1]);
plane('trochoidin', 'Inferior Trochoid (curtate)', T`x=rt-d\sin t,\; y=r-d\cos t,\; d<r`,
  'A point inside the wheel, such as one on a spoke. The path is a wavy line with no cusps or loops.', 'Portland', 6, 0, 6 * Math.PI, .02,
  t => [t - .6 * Math.sin(t), 1 - .6 * Math.cos(t)]);
plane('trochoidsup', 'Superior Trochoid (prolate)', T`x=rt-d\sin t,\; y=r-d\cos t,\; d>r`,
  'A point beyond the rim, like a train wheel\'s flange. At the bottom it moves backward, so the path forms loops.', 'Electric', 6, 0, 6 * Math.PI, .02,
  t => [t - 1.6 * Math.sin(t), 1 - 1.6 * Math.cos(t)]);

/* Epicycloids and epitrochoids */
plane('cardioid', 'Cardioid', pe('1,1,1'),
  'An epicycloid with one cusp. It describes the pickup pattern of a cardioid microphone.', 'Magma', 6, 0, TAU, .01, epi(1, 1, 1));
plane('nephroid', 'Nephroid', pe('2,1,1'),
  'Two cusps. It is the caustic that sunlight draws inside a coffee cup.', 'Inferno', 6, 0, TAU, .01, epi(2, 1, 1));
plane('epi3', 'Epicycloid (3 cusps)', pe('3,1,1'),
  'A circle rolling outside a fixed circle three times its size, the flank shape of cycloidal gear teeth.', 'Rainbow', 6, 0, TAU, .01, epi(3, 1, 1));
plane('ranunculoid', 'Ranunculoid (5 cusps)', pe('5,1,1'),
  'Rolling outside a circle five times larger gives five pointed petals.', 'Picnic', 6, 0, TAU, .01, epi(5, 1, 1));
plane('epitroin', 'Inferior Epitrochoid', pe('3,1,0.5'),
  'The pen sits inside the rolling circle, so the cusps soften into rounded lobes.', 'Plasma', 6, 0, TAU, .01, epi(3, 1, .5));
plane('epitrosup', 'Superior Epitrochoid', pe('3,1,2'),
  'The pen sits beyond the rolling circle\'s edge, which ties a small loop into every lobe.', 'Viridis', 6, 0, TAU, .01, epi(3, 1, 2));
plane('wankel', 'Wankel Housing (epitrochoid)', T`x=R\cos t+e\cos 3t,\; y=R\sin t+e\sin 3t`,
  'The two-lobed epitrochoid inside a rotary engine, traced so the triangular rotor always touches its wall.', 'Jet', 7, 0, TAU, .01,
  t => [Math.cos(t) + .18 * Math.cos(3 * t), Math.sin(t) + .18 * Math.sin(3 * t)]);

/* Hypocycloids and hypotrochoids */
plane('deltoid', 'Deltoid (Steiner curve)', ph('3,1,1'),
  'A circle rolling inside one three times its size makes a curved triangle with three cusps.', 'Earth', 6, 0, TAU, .01, hypo(3, 1, 1));
plane('astroid', 'Astroid', ph('4,1,1'),
  'The four-cusped star. It is the envelope of a sliding ladder, and the shape of the Cartesian "pencil of lines" trammel.', 'Portland', 6, 0, TAU, .01, hypo(4, 1, 1));
plane('hypo52', 'Hypocycloid (R/r = 5/2)', ph('5,2,2'),
  'A non-integer ratio takes two turns to close and traces a five-pointed star.', 'Magma', 6, 0, 2 * TAU, .01, hypo(5, 2, 2));
plane('hypotroin', 'Inferior Hypotrochoid', ph('5,3,2'),
  'A Spirograph pattern with the pen inside the rolling circle: a rounded rosette with no loops.', 'Rainbow', 5, 0, 6 * Math.PI, .02, hypo(5, 3, 2));
plane('hypotrosup', 'Superior Hypotrochoid', ph('5,3,5'),
  'The classic Spirograph curve: the pen sits beyond the rolling circle\'s rim, so each lobe gets a loop.', 'Plasma', 5, 0, 6 * Math.PI, .02, hypo(5, 3, 5));

/* Spirals */
plane('archspiral', 'Archimedean Spiral', T`r=a\theta`,
  'Equal spacing between turns, as in scroll compressors, record grooves and constant-lift cams.', 'Viridis', 5, 0, 8 * Math.PI, .02, polar(t => .4 * t));
plane('logspiral', 'Logarithmic Spiral', T`r=ae^{b\theta}`,
  'Equiangular: it crosses every radius at the same angle. Nautilus shells and pump volutes follow it.', 'Inferno', 5, -4 * Math.PI, 2 * Math.PI, .02, polar(t => Math.exp(.2 * t)));
plane('fermat', "Fermat's Spiral", T`r^2=a^2\theta`,
  'A parabolic spiral whose two branches interlock through the origin. Sunflower seed heads grow along it.', 'Portland', 5, -4, 4, .005,
  t => [t * Math.cos(t * t), t * Math.sin(t * t)]);
plane('clothoid', 'Euler Spiral (Clothoid)', T`x=\int_0^t\cos\tfrac{\pi s^2}{2}ds,\; y=\int_0^t\sin\tfrac{\pi s^2}{2}ds`,
  'Curvature grows steadily with distance. Highways and railways use it so steering eases in rather than jerking.', 'Jet', 6, -4, 4, .01, fres);

/* Gears, cams and mechanisms */
plane('involute', 'Involute of a Circle', T`x=r(\cos t+t\sin t),\; y=r(\sin t-t\cos t)`,
  'The path of a taut string unwinding from a circle, and the standard tooth profile for most gears.', 'Electric', 6, 0, 8, .01,
  t => [Math.cos(t) + t * Math.sin(t), Math.sin(t) - t * Math.cos(t)]);
plane('fourbar', 'Four-Bar Coupler Curve', T`P=A+p\,R_\alpha\,\hat{u}_{AC}`,
  'A point on the coupler of a crank-rocker linkage (links 1, 3, 3, 3). Linkage designers use such curves to guide motion.', 'Plasma', 7, 0, TAU, .01, fourbar);
plane('slidercrank', 'Slider-Crank Piston Motion', T`x(\theta)=r\cos\theta+\sqrt{l^2-r^2\sin^2\theta}`,
  'Piston position against crank angle for l/r = 3.5. The connecting rod makes it differ from a pure sine wave.', 'Viridis', 6, 0, 4 * Math.PI, .02,
  t => [t, Math.cos(t) + Math.sqrt(12.25 - Math.sin(t) ** 2)]);
plane('limacon', 'Limaçon', T`r=b+a\cos\theta`,
  'With a > b it grows an inner loop. It shows up in cam profiles and as the path of a crank-driven point.', 'Magma', 6, 0, TAU, .01,
  polar(t => 1 + 2 * Math.cos(t)));

/* Structures and dynamics */
plane('catenary', 'Catenary', T`y=a\cosh\tfrac xa`,
  'How a free-hanging chain sags. Flipped upside down, it is the ideal shape for a masonry arch.', 'Earth', 7, -3, 3, .02,
  t => [t, Math.cosh(t)]);
plane('tractrix', 'Tractrix', T`x=t-\tanh t,\; y=\operatorname{sech}t`,
  'The path of an object dragged by a rope along a straight line. It is also the profile of a Schiele pivot bearing.', 'Portland', 6, -6, 6, .02,
  t => [t - Math.tanh(t), 1 / Math.cosh(t)]);
plane('damped', 'Damped Oscillation', T`y=e^{-\zeta t}\sin\omega t`,
  'A spring-mass system losing energy: the sine wave shrinks under an exponential envelope.', 'Inferno', 5, 0, 20, .02,
  t => [t, Math.exp(-.2 * t) * Math.sin(4 * t)]);
plane('beats', 'Beat Pattern', T`y=\sin 10t+\sin 11t=2\cos\tfrac t2\sin\tfrac{21t}{2}`,
  'Two close frequencies interfere and the amplitude swells and fades, the signal behind out-of-tune strings and vibration beating.', 'Rainbow', 4, 0, 4 * Math.PI, .01,
  t => [t, Math.sin(10 * t) + Math.sin(11 * t)]);
plane('lissajous2d', 'Lissajous Figure (5:4)', T`x=\sin(5t+\tfrac\pi2),\; y=\sin 4t`,
  'What an oscilloscope shows when two signals of related frequency drive its axes. The knot count reveals the ratio.', 'Jet', 5, 0, TAU, .005,
  t => [Math.sin(5 * t + Math.PI / 2), Math.sin(4 * t)]);
plane('superellipse', 'Superellipse (n = 4)', T`\left|\tfrac xa\right|^n+\left|\tfrac yb\right|^n=1`,
  'Between a circle and a rounded square. Designers use it for table tops, plazas and app icons.', 'Viridis', 7, 0, TAU, .01,
  t => [Math.sign(Math.cos(t)) * Math.abs(Math.cos(t)) ** .5, Math.sign(Math.sin(t)) * Math.abs(Math.sin(t)) ** .5]);

/* Classical algebraic curves */
plane('lemniscate', 'Lemniscate of Bernoulli', T`(x^2+y^2)^2=2a^2(x^2-y^2)`,
  'The figure-8 where the product of the distances to two foci stays constant. Railway transition curves borrow its shape.', 'Plasma', 7, 0, TAU, .01,
  t => [2 * Math.cos(t) / (1 + Math.sin(t) ** 2), 2 * Math.sin(t) * Math.cos(t) / (1 + Math.sin(t) ** 2)]);
plane('witch', 'Witch of Agnesi', T`y=\frac{8a^3}{x^2+4a^2}`,
  'A bell-shaped curve named by a mistranslation. It resembles resonance peaks and diffraction profiles.', 'Earth', 7, -8, 8, .02,
  t => [t, 8 / (t * t + 4)]);
plane('cissoid', 'Cissoid of Diocles', T`x=\frac{2at^2}{1+t^2},\; y=\frac{2at^3}{1+t^2}`,
  'Invented to double the cube. Its cusp and asymptote make a shape much like a pointed leaf with open arms.', 'Magma', 7, -4, 4, .01,
  t => [2 * t * t / (1 + t * t), 2 * t ** 3 / (1 + t * t)]);
plane('rose52', 'Rose Curve (k = 5/2)', T`r=\cos(k\theta),\; k=\tfrac52`,
  'A petal curve. With an odd numerator over 2 it needs four turns to close, and the petals overlap.', 'Rainbow', 5, 0, 4 * Math.PI, .01,
  polar(t => Math.cos(2.5 * t)));
plane('butterfly', 'Butterfly Curve', T`r=e^{\cos t}-2\cos 4t-\sin^5\tfrac t{12}`,
  'Temple Fay\'s 1989 polar curve, drawn here over 12π so its wings fill in.', 'Inferno', 4, 0, 12 * Math.PI, .02,
  t => { const r = Math.exp(Math.cos(t)) - 2 * Math.cos(4 * t) - Math.sin(t / 12) ** 5; return [Math.sin(t) * r, Math.cos(t) * r]; });

/* Involutes & Evolutes
   Paste this block right after the Engineering Curves block (before "/* Attractors */").
   Uses helpers from script.js: T, reg, surf, P. */
const IE = 'Involutes & Evolutes';
const PI2 = 2 * Math.PI;

const sample = (t0, t1, dt, f) => { const a = []; for (let t = t0; t <= t1 + 1e-9; t += dt) a.push(f(t)); return a; };
const circ = r => sample(0, PI2, .05, t => [r * Math.cos(t), r * Math.sin(t)]);

// Several flat curves in one plot; each curve gets its own colour band
const bundle = (k, n, eq, d, cs, w, curves) => reg(k, IE, n, eq, d, () => {
  const x = [], y = [], z = [], c = [];
  curves().forEach((pts, j) => {
    pts.forEach((p, i) => { x.push(p[0]); y.push(p[1]); z.push(0); c.push(j + i / pts.length); });
    x.push(null); y.push(null); z.push(null); c.push(j);
  });
  return { data: [{ x, y, z, type: 'scatter3d', mode: 'lines', connectgaps: false, line: { color: c, colorscale: cs, width: w } }] };
});

// Involute of any curve g(t): tip of a taut string unwound from g, starting at parameter tc
const involute = (g, t0, t1, n, tc) => {
  const P0 = [], s = [0];
  for (let i = 0; i <= n; i++) P0.push(g(t0 + (t1 - t0) * i / n));
  for (let i = 1; i <= n; i++) s.push(s[i - 1] + Math.hypot(P0[i][0] - P0[i - 1][0], P0[i][1] - P0[i - 1][1]));
  const L0 = s[Math.round((tc - t0) / (t1 - t0) * n)];
  return P0.map((p, i) => {
    const a = P0[Math.max(i - 1, 0)], b = P0[Math.min(i + 1, n)], l = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1;
    return [p[0] - (s[i] - L0) * (b[0] - a[0]) / l, p[1] - (s[i] - L0) * (b[1] - a[1]) / l];
  });
};

// Normals from a curve g to its centre of curvature c: they envelop the evolute
const normals = (g, c, a, b, k) => Array.from({ length: k }, (_, i) => { const t = a + (b - a) * i / (k - 1); return [g(t), c(t)]; });
const evolutePair = (k, n, eq, d, cs, g, c, a, b) =>
  bundle(k, n, eq, d, cs, 4, () => [sample(a, b, .02, g), sample(a, b, .02, c), ...normals(g, c, a, b, 16).map(p => [p[0], p[1]])]);

/* ---- Involutes ---- */
bundle('invfamily', 'Involute Family of a Circle', T`x=r\cos(t+a_k)+rt\sin(t+a_k),\; y=r\sin(t+a_k)-rt\cos(t+a_k),\; a_k=\tfrac{k\pi}{4}`,
  'Eight involutes of one base circle, each a rotated copy of the others. This is the pinwheel that gear teeth are cut from.', 'Rainbow', 4,
  () => [circ(1), ...Array.from({ length: 8 }, (_, k) => sample(0, 4.5, .05, t => {
    const a = k * Math.PI / 4; return [Math.cos(t + a) + t * Math.sin(t + a), Math.sin(t + a) - t * Math.cos(t + a)];
  }))]);

const gearOutline = () => {
  const N = 14, rp = N / 2, rb = rp * Math.cos(Math.PI / 9), ra = rp + 1, rr = rp - 1.25;
  const hb = Math.PI / (2 * N) + Math.tan(Math.PI / 9) - Math.PI / 9;
  const tm = Math.sqrt((ra / rb) ** 2 - 1), inv = t => t - Math.atan(t), out = [];
  for (let k = 0; k < N; k++) {
    const c = PI2 * k / N, add = (r, a) => out.push([r * Math.cos(c + a), r * Math.sin(c + a)]);
    const flank = s => { for (let i = 0; i <= 16; i++) { const t = tm * (s < 0 ? i : 16 - i) / 16; add(rb * Math.sqrt(1 + t * t), s * (hb - inv(t))); } };
    add(rr, -hb); flank(-1); flank(1); add(rr, hb);
    for (let i = 1; i < 5; i++) add(rr, hb + (PI2 / N - 2 * hb) * i / 5);
  }
  out.push(out[0]);
  return out;
};
bundle('spurgear', 'Involute Spur Gear (14 teeth)', T`\varphi(r)=\varphi_b-\left(\tan\alpha-\alpha\right),\quad \alpha=\arccos\tfrac{r_b}{r}`,
  'Each tooth flank is an involute of the base circle, so the gears roll with a constant velocity ratio. The inner rings mark the pitch and base circles.', 'Plasma', 5,
  () => [gearOutline(), circ(7), circ(7 * Math.cos(Math.PI / 9))]);

const ell = t => [2 * Math.cos(t), Math.sin(t)];
bundle('invellipse', 'Involutes of an Ellipse', T`\mathbf I(t)=\mathbf\gamma(t)-\big(s(t)-s_0\big)\,\mathbf T(t)`,
  'String unwound from an ellipse spirals outward. Starting at the two ends of the axes gives two different involutes.', 'Portland', 4,
  () => [sample(0, PI2, .05, ell), involute(ell, 0, 4 * Math.PI, 800, 0), involute(ell, 0, 4 * Math.PI, 800, Math.PI)]);
const par = t => [t, t * t];
bundle('invparabola', 'Involute of a Parabola', T`\mathbf I(t)=\mathbf\gamma(t)-\big(s(t)-s_0\big)\,\mathbf T(t),\;\; \mathbf\gamma=(t,t^2)`,
  'Unwinding from the vertex gives a curve with a cusp at the start, which bends back toward the parabola\'s axis.', 'Plasma', 5,
  () => [sample(-1.5, 1.5, .05, par), involute(par, -1.5, 1.5, 600, 0)]);
const cycE = t => [t + Math.sin(t), Math.cos(t) - 1];
bundle('invcycloid', 'Involute of a Cycloid', T`\mathbf I(t)=\mathbf\gamma(t)-s(t)\mathbf T(t)\;\Rightarrow\; \text{a congruent cycloid}`,
  'Unwinding a cycloid arch gives another cycloid of the same size. Huygens used this for his isochronous pendulum clock.', 'Viridis', 5,
  () => [sample(0, PI2, .03, cycE), involute(cycE, 0, PI2, 600, 0)]);
const cat = t => [t, Math.cosh(t)];
bundle('invcatenary', 'Involute of a Catenary (Tractrix)', T`\mathbf I(t)=(t-\tanh t,\;\operatorname{sech}t)`,
  'Unwind a hanging chain from its lowest point and the free end draws a tractrix.', 'Earth', 5,
  () => [sample(-3, 3, .05, cat), involute(cat, -3, 3, 600, 0)]);

surf('invhelicoid', IE, 'Involute Helicoid (helical gear flank)',
  T`\mathbf r(u,v)=R_z(cv)\,\big(\cos u+u\sin u,\;\sin u-u\cos u\big),\; z=v`,
  'Sweep an involute up the axis while turning it and you get the tooth flank of a helical gear.', 'Plasma',
  P(0, 1.3, 40, 0, 6, 60, (u, v) => {
    const bx = Math.cos(u) + u * Math.sin(u), by = Math.sin(u) - u * Math.cos(u), a = .45 * v;
    return { x: bx * Math.cos(a) - by * Math.sin(a), y: bx * Math.sin(a) + by * Math.cos(a), z: v };
  }));

/* ---- Parallel curves ---- */
bundle('ellipseoffsets', 'Parallel Curves of an Ellipse', T`\mathbf P_d(t)=\mathbf\gamma(t)+d\,\mathbf n(t)`,
  'Offsetting an ellipse by distance d. Inward offsets past the radius of curvature grow cusps, tracing out the evolute.', 'Rainbow', 4,
  () => [-.8, -.5, -.25, 0, .4, .8, 1.2].map(d => sample(0, PI2, .02, t => {
    const N = Math.hypot(Math.cos(t), 2 * Math.sin(t));
    return [2 * Math.cos(t) + d * Math.cos(t) / N, Math.sin(t) + d * 2 * Math.sin(t) / N];
  })));

/* ---- Evolutes: each curve, its evolute, and the normals that envelop it ---- */
evolutePair('evparabola', 'Parabola and its Evolute', T`\gamma=(t,t^2),\quad \mathbf E=\left(-4t^3,\;3t^2+\tfrac12\right)`,
  'The evolute of a parabola is Neile\'s semicubical parabola, with a cusp at the focus-side of the vertex.', 'Portland',
  t => [t, t * t], t => [-4 * t ** 3, 3 * t * t + .5], -1, 1);
evolutePair('evellipse', 'Ellipse and its Evolute', T`\mathbf E=\left(\tfrac{a^2-b^2}{a}\cos^3t,\;-\tfrac{a^2-b^2}{b}\sin^3t\right)`,
  'The centres of curvature of an ellipse form a stretched astroid with four cusps.', 'Rainbow',
  ell, t => [1.5 * Math.cos(t) ** 3, -3 * Math.sin(t) ** 3], 0, PI2);
evolutePair('evcycloid', 'Cycloid and its Evolute', T`\mathbf E=(t+\sin t,\;\cos t-1)`,
  'The evolute of a cycloid is an identical cycloid shifted down and sideways.', 'Viridis',
  t => [t - Math.sin(t), 1 - Math.cos(t)], t => [t + Math.sin(t), Math.cos(t) - 1], 0, PI2);
evolutePair('evcatenary', 'Catenary and its Evolute', T`\mathbf E=(t-\sinh t\cosh t,\;2\cosh t)`,
  'The centres of curvature of a hanging chain trace a curve that rises steeply on both sides.', 'Earth',
  cat, t => [t - Math.sinh(t) * Math.cosh(t), 2 * Math.cosh(t)], -1.6, 1.6);
evolutePair('evastroid', 'Astroid and its Evolute', T`\mathbf E=\big(\cos^3t+3\cos t\sin^2t,\;\sin^3t+3\sin t\cos^2t\big)`,
  'The evolute of an astroid is another astroid, twice as large and turned 45 degrees.', 'Plasma',
  t => [Math.cos(t) ** 3, Math.sin(t) ** 3],
  t => [Math.cos(t) ** 3 + 3 * Math.cos(t) * Math.sin(t) ** 2, Math.sin(t) ** 3 + 3 * Math.sin(t) * Math.cos(t) ** 2], 0, PI2);

/* Attractors */
att('lorenz', 'Lorenz Attractor', T`\dot x=\sigma(y-x),\; \dot y=x(\rho-z)-y,\; \dot z=xy-\beta z`,
  'The blueprint of chaos, born from a model of atmospheric convection and home of the butterfly effect.', 'Inferno', 8000, .008, [.1, 0, 0],
  (x, y, z) => [10 * (y - x), x * (28 - z) - y, x * y - 8 / 3 * z]);
att('rossler', 'Rössler Attractor', T`\dot x=-y-z,\; \dot y=x+ay,\; \dot z=b+z(x-c)`,
  'Otto Rössler\'s 1976 design: as simple as possible while still being chaotic.', 'Earth', 10000, .04, [1, 1, 1],
  (x, y, z) => [-y - z, x + .2 * y, .2 + z * (x - 5.7)]);
att('chen', 'Chen Attractor', T`\dot x=a(y-x),\; \dot y=(c-a)x-xz+cy,\; \dot z=xy-bz`,
  'Found in 1999, dynamically richer than the Lorenz system despite a similar structure.', 'Electric', 8000, .005, [5, 10, 10],
  (x, y, z) => [35 * (y - x), -7 * x - x * z + 28 * y, x * y - 3 * z]);
att('thomas', "Thomas' Cyclically Symmetric Attractor", T`\dot x=\sin y-bx,\; \dot y=\sin z-by,\; \dot z=\sin x-bx`,
  'Cyclic symmetry in three dimensions: instead of two wings it weaves a labyrinthine lattice.', 'Picnic', 15000, .05, [1, 1.1, 1],
  (x, y, z) => [Math.sin(y) - .208186 * x, Math.sin(z) - .208186 * y, Math.sin(x) - .208186 * z]);
att('halvorsen', 'Halvorsen Attractor', T`\dot x=-ax-4y-4z-y^2\;(\text{and cyclic})`,
  'Cyclically symmetric trajectories that spin out from the origin and fold back into a flower.', 'Magma', 15000, .01, [1, 0, 0],
  (x, y, z) => [-1.89 * x - 4 * y - 4 * z - y * y, -1.89 * y - 4 * z - 4 * x - z * z, -1.89 * z - 4 * x - 4 * y - x * x]);
att('aizawa', 'Aizawa Attractor', T`\dot x=(z-0.7)x-3.5y,\; \dot y=3.5x+(z-0.7)y`,
  'A dense sphere of orbits with a tube bored through its axis.', 'Inferno', 12000, .015, [.1, 0, 0],
  (x, y, z) => [(z - .7) * x - 3.5 * y, 3.5 * x + (z - .7) * y, .6 + .95 * z - z ** 3 / 3 - (x * x + y * y) * (1 + .25 * z) + .1 * z * x ** 3]);
att('rabinovich', 'Rabinovich-Fabrikant', T`\dot x=y(z-1+x^2)+\gamma x,\; \dot y=x(3z+1-x^2)+\gamma y`,
  'Models modulation instability in waves and yields delicate structures that shift with its parameters.', 'Viridis', 10000, .01, [-1, 0, .5],
  (x, y, z) => [y * (z - 1 + x * x) + .1 * x, x * (3 * z + 1 - x * x) + .1 * y, -2 * z * (.2875 + x * y)]);
att('lorenz84', 'Lorenz-84 Attractor', T`\dot x=-ax-y^2-z^2+aF,\; \dot y=-y+xy-bxz+G`,
  'Lorenz\'s later, simpler model of westerly winds interacting with large-scale eddies.', 'Plasma', 15000, .01, [1, 1, 1],
  (x, y, z) => [-.25 * x - y * y - z * z + 2, -y + x * y - 4 * x * z + 1, -z + 4 * x * y + x * z]);
att('sprottA', 'Sprott System A', T`\dot x=y,\; \dot y=-x+yz,\; \dot z=1-y^2`,
  'Found by J.C. Sprott in an automated search: one of the simplest equation sets that still produces chaos.', CY, 12000, .02, [0, 5, 0],
  (x, y, z) => [y, -x + y * z, 1 - y * y]);
att('nosehoover', 'Nosé-Hoover Attractor', T`\dot x=y,\; \dot y=-x+yz,\; \dot z=a-y^2`,
  'Built to hold temperature constant in molecular dynamics, with a symmetric hollow core.', 'Jet', 15000, .015, [1, 0, 0],
  (x, y, z) => [y, -x + y * z, 1.5 - y * y]);
att('burkeshaw', 'Burke-Shaw Attractor', T`\dot x=-s(x+y),\; \dot y=-y-sxz,\; \dot z=sxy+v`,
  'A Lorenz variant that folds into a clean, symmetric butterfly.', 'Electric', 12000, .01, [1, 0, 0],
  (x, y, z) => [-10 * (x + y), -y - 10 * x * z, 10 * x * y + 4.272]);
att('dadras', 'Dadras Attractor', T`\dot x=y-ax+byz,\; \dot y=cy-xz+z,\; \dot z=dxy-ez`,
  'A chaotic system that stretches into a wide multi-lobed ribbon.', 'Rainbow', 15000, .005, [1, 1, 1],
  (x, y, z) => [y - 3 * x + 2.7 * y * z, 1.7 * y - x * z + z, 2 * x * y - 9 * z]);
att('fourwing', 'Four-Wing Attractor', T`\dot x=ax+yz,\; \dot y=bx+cy-xz,\; \dot z=-z-xy`,
  'Trajectories alternate between four lobes, a more intricate cousin of the two-winged Lorenz butterfly.', 'Portland', 12000, .05, [1, 1, 1],
  (x, y, z) => [.2 * x + y * z, .01 * x - .4 * y - x * z, -z - x * y]);

/* ---------- Plot layout ---------- */
const layout = () => ({
  paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
  margin: { t: 0, b: 0, l: 0, r: 0 },
  font: { family: 'Instrument Sans, sans-serif', color: '#9a9fc4' },
  scene: {
    xaxis: { visible: false }, yaxis: { visible: false }, zaxis: { visible: false },
    camera: { eye: { x: 1.4, y: 1.4, z: 1.2 } }, bgcolor: 'rgba(0,0,0,0)'
  }
});

/* ---------- UI ---------- */
const $ = id => document.getElementById(id);
const select = $('function-select');
const keys = Object.keys(M);

const groups = {};
keys.forEach(k => (groups[M[k].group] ||= []).push(k));
for (const [name, ks] of Object.entries(groups)) {
  const og = document.createElement('optgroup');
  og.label = name;
  ks.forEach(k => og.append(new Option(M[k].name, k)));
  select.append(og);
}

function renderPlot(key) {
  const m = M[key], loader = $('loader'), info = $('info');
  select.value = key;
  loader.style.opacity = 1; loader.style.pointerEvents = 'all';
  info.classList.remove('swap');

  setTimeout(() => {
    $('func-name').textContent = m.name;
    $('func-badge').textContent = m.group;
    $('func-desc').textContent = m.description;
    $('func-eq').innerHTML = m.equation;
    (window.MathJax?.startup?.promise || Promise.resolve())
      .then(() => MathJax.typesetPromise?.([$('func-eq')]))
      .catch(console.error);

    Plotly.react('plot', m.generate().data, layout(), { displayModeBar: false, responsive: true }).then(() => {
      loader.style.opacity = 0; loader.style.pointerEvents = 'none';
      void info.offsetWidth;
      info.classList.add('swap');
    });
  }, 50);
}

const step = d => renderPlot(keys[(keys.indexOf(select.value) + d + keys.length) % keys.length]);
select.addEventListener('change', e => renderPlot(e.target.value));
$('prev').addEventListener('click', () => step(-1));
$('next').addEventListener('click', () => step(1));
$('random').addEventListener('click', () => renderPlot(keys[Math.floor(Math.random() * keys.length)]));
document.addEventListener('keydown', e => {
  if (e.target === select) return;
  if (e.key === 'ArrowLeft') step(-1);
  if (e.key === 'ArrowRight') step(1);
});

window.addEventListener('load', () => renderPlot('sinc'));
window.addEventListener('resize', () => { const p = $('plot'); if (p.data) Plotly.Plots.resize(p); });
