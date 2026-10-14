// Helper to generate 2D grids (Z-surfaces)
const generateGrid = (xMin, xMax, xStep, yMin, yMax, yStep, func) => {
    let z = [], x = [], y = [];
    for (let i = xMin; i <= xMax; i += xStep) x.push(i);
    for (let j = yMin; j <= yMax; j += yStep) y.push(j);
    
    for (let i = 0; i < y.length; i++) {
        let z_row = [];
        for (let j = 0; j < x.length; j++) {
            z_row.push(func(x[j], y[i]));
        }
        z.push(z_row);
    }
    return { z, x, y };
};

// Helper to generate parametric surfaces
const generateParametric = (uMin, uMax, uSteps, vMin, vMax, vSteps, func) => {
    let x = [], y = [], z = [];
    let du = (uMax - uMin) / uSteps;
    let dv = (vMax - vMin) / vSteps;
    
    for (let i = 0; i <= uSteps; i++) {
        let u = uMin + i * du;
        let x_row = [], y_row = [], z_row = [];
        for (let j = 0; j <= vSteps; j++) {
            let v = vMin + j * dv;
            let pt = func(u, v);
            x_row.push(pt.x);
            y_row.push(pt.y);
            z_row.push(pt.z);
        }
        x.push(x_row);
        y.push(y_row);
        z.push(z_row);
    }
    return { x, y, z };
};

// Helper for differential equation attractors
const generateAttractor = (steps, dt, init, eq) => {
    let x = [], y = [], z = [];
    let curr = { ...init };
    
    for(let i=0; i<steps; i++) {
        let d = eq(curr.x, curr.y, curr.z);
        curr.x += d.dx * dt;
        curr.y += d.dy * dt;
        curr.z += d.dz * dt;
        x.push(curr.x);
        y.push(curr.y);
        z.push(curr.z);
    }
    return { x, y, z };
};

// Database of our mathematical surfaces and attractors
const mathData = {
    sinc: {
        group: "Surfaces",
        name: "The Sinc Function",
        equation: "$$ z = \\frac{\\sin(R)}{R} \\quad \\text{where } R = \\sqrt{x^2 + y^2} $$",
        description: "Often described as a mathematical raindrop hitting a pond, the unnormalized 2D Sinc function creates perfectly decaying concentric ripples. It acts as the ideal interpolation filter in signal processing.",
        generate: () => {
            const {x, y, z} = generateGrid(-10, 10, 0.4, -10, 10, 0.4, (x, y) => {
                let r = Math.sqrt(x*x + y*y) + 0.0001; 
                return Math.sin(r) / r;
            });
            return { data: [{ z, x, y, type: 'surface', colorscale: 'Cyan', bg: 'black' }], type: 'surface' };
        }
    },
    gaussian: {
        group: "Surfaces",
        name: "Bivariate Gaussian",
        equation: "$$ f(x,y) = \\frac{1}{2\\pi\\sigma^2} e^{-\\frac{x^2+y^2}{2\\sigma^2}} $$",
        description: "The classic 'Bell Curve' extended into 3D. This probability distribution is a foundational block of statistics, naturally emerging everywhere from quantum mechanics to the behavior of vast populations.",
        generate: () => {
            let sigma = 2;
            const {x, y, z} = generateGrid(-6, 6, 0.25, -6, 6, 0.25, (x, y) => {
                return (1 / (2 * Math.PI * sigma**2)) * Math.exp(-(x**2 + y**2) / (2 * sigma**2));
            });
            return { data: [{ z, x, y, type: 'surface', colorscale: 'Viridis' }], type: 'surface' };
        }
    },
    saddle: {
        group: "Surfaces",
        name: "Hyperbolic Paraboloid",
        equation: "$$ z = x^2 - y^2 $$",
        description: "Known as a Saddle Point or Minimax, this gorgeous surface curves upwards in one direction and downwards in the other. It's notoriously difficult to navigate in deep learning optimization, as algorithms can easily stall here during gradient descent.",
        generate: () => {
            const {x, y, z} = generateGrid(-5, 5, 0.2, -5, 5, 0.2, (x, y) => x*x - y*y);
            return { data: [{ z, x, y, type: 'surface', colorscale: 'Plasma' }], type: 'surface' };
        }
    },
    lorenz: {
        group: "Attractors",
        name: "Lorenz Attractor",
        equation: "$$ \\frac{dx}{dt} = \\sigma(y-x), \\; \\frac{dy}{dt} = x(\\rho-z)-y $$",
        description: "The blueprint of chaos. Originally designed to model atmospheric convection, it revealed the 'butterfly effect'—how tiny changes in initial conditions result in completely wildly different, beautifully chaotic trajectories.",
        generate: () => {
            let sigma = 10, rho = 28, beta = 8/3;
            let {x, y, z} = generateAttractor(8000, 0.008, {x:0.1, y:0, z:0}, (x, y, z) => ({
                dx: sigma * (y - x),
                dy: x * (rho - z) - y,
                dz: x * y - beta * z
            }));
            return { data: [{ x, y, z, type: 'scatter3d', mode: 'lines', line: { color: z, colorscale: 'Inferno', width: 3 } }], type: 'line' };
        }
    },

    rastrigin: {
        group: "Optimization Landscapes",
        name: "Rastrigin Function",
        equation: "$$ f(x,y) = 20 + x^2 - 10\\cos(2\\pi x) + y^2 - 10\\cos(2\\pi y) $$",
        description: "A highly multimodal function regularly used to test optimization algorithms. Its vast number of local minima make it incredibly difficult for standard gradient descent algorithms to find the true global minimum at the center.",
        generate: () => {
            const {x, y, z} = generateGrid(-5.12, 5.12, 0.15, -5.12, 5.12, 0.15, (x, y) => {
                return 20 + x*x - 10*Math.cos(2*Math.PI*x) + y*y - 10*Math.cos(2*Math.PI*y);
            });
            return { data: [{ z, x, y, type: 'surface', colorscale: 'Earth' }], type: 'surface' };
        }
    },
    rosenbrock: {
        group: "Optimization Landscapes",
        name: "Rosenbrock Valley",
        equation: "$$ f(x,y) = (1 - x)^2 + 100(y - x^2)^2 $$",
        description: "Also known as the 'Banana Valley', the Rosenbrock function features a long, narrow, parabolic valley. Finding the valley is trivial, but navigating its flat floor to the global minimum is a classic challenge for mathematical optimizers.",
        generate: () => {
            const {x, y, z} = generateGrid(-2, 2, 0.1, -1, 3, 0.1, (x, y) => {
                return Math.pow(1-x, 2) + 100 * Math.pow(y - x*x, 2);
            });
            return { data: [{ z, x, y, type: 'surface', colorscale: 'Magma' }], type: 'surface' };
        }
    },
    ackley: {
        group: "Optimization Landscapes",
        name: "Ackley Function",
        equation: "$$ f(x,y) = -20\\exp(-0.2\\sqrt{0.5(x^2+y^2)}) - \\exp(0.5(\\cos(2\\pi x)+\\cos(2\\pi y))) + e + 20 $$",
        description: "Characterized by a nearly flat outer region full of shallow peaks and valleys, which steeply drops into a single massive valley containing the global minimum. It forces algorithms to search globally before diving deep.",
        generate: () => {
            const {x, y, z} = generateGrid(-8, 8, 0.3, -8, 8, 0.3, (x, y) => {
                let term1 = -20 * Math.exp(-0.2 * Math.sqrt(0.5 * (x*x + y*y)));
                let term2 = -Math.exp(0.5 * (Math.cos(2*Math.PI*x) + Math.cos(2*Math.PI*y)));
                return term1 + term2 + Math.E + 20;
            });
            return { data: [{ z, x, y, type: 'surface', colorscale: 'Portland' }], type: 'surface' };
        }
    },
    himmelblau: {
        group: "Optimization Landscapes",
        name: "Himmelblau's Function",
        equation: "$$ f(x,y) = (x^2 + y - 11)^2 + (x + y^2 - 7)^2 $$",
        description: "A multi-modal polynomial function used to test the performance of optimization algorithms. Uniquely, it possesses four distinct, identical global minima located where the surface touches zero.",
        generate: () => {
            const {x, y, z} = generateGrid(-5, 5, 0.2, -5, 5, 0.2, (x, y) => {
                return Math.pow(x*x + y - 11, 2) + Math.pow(x + y*y - 7, 2);
            });
            return { data: [{ z, x, y, type: 'surface', colorscale: 'Electric' }], type: 'surface' };
        }
    },
    beale: {
        group: "Optimization Landscapes",
        name: "Beale Function",
        equation: "$$ f(x,y) = (1.5 - x + xy)^2 + (2.25 - x + xy^2)^2 + (2.625 - x + xy^3)^2 $$",
        description: "This landscape features sharp peaks and corners with a very flat region near the global minimum. It tests an algorithm's ability to navigate tight spaces.",
        generate: () => {
            const {x, y, z} = generateGrid(-4.5, 4.5, 0.15, -4.5, 4.5, 0.15, (x, y) => {
                return Math.pow(1.5 - x + x*y, 2) + Math.pow(2.25 - x + x*y*y, 2) + Math.pow(2.625 - x + x*y*y*y, 2);
            });
            // Cap Z for visualization so the valley is visible
            let cappedZ = z.map(row => row.map(val => Math.min(val, 200)));
            return { data: [{ z: cappedZ, x, y, type: 'surface', colorscale: 'Jet' }], type: 'surface' };
        }
    },
    crossintray: {
        group: "Optimization Landscapes",
        name: "Cross-in-Tray Function",
        equation: "$$ f(x,y) = -0.0001 \\left( \\left| \\sin(x)\\sin(y) e^{\\left|100 - \\frac{\\sqrt{x^2+y^2}}{\\pi}\\right|} \\right| + 1 \\right)^{0.1} $$",
        description: "An incredibly striking function resembling a canopy or tent. It contains four identical global minima located in the corners of the 'cross' shape at its center.",
        generate: () => {
            const {x, y, z} = generateGrid(-10, 10, 0.2, -10, 10, 0.2, (x, y) => {
                let r = Math.sqrt(x*x + y*y);
                let expTerm = Math.abs(100 - (r / Math.PI));
                let inner = Math.abs(Math.sin(x) * Math.sin(y) * Math.exp(expTerm)) + 1;
                return -0.0001 * Math.pow(inner, 0.1);
            });
            return { data: [{ z, x, y, type: 'surface', colorscale: 'Picnic' }], type: 'surface' };
        }
    },

    dropwave: {
        group: "Surfaces",
        name: "Drop-Wave Function",
        equation: "$$ f(x,y) = -\\frac{1 + \\cos(12\\sqrt{x^2+y^2})}{0.5(x^2+y^2) + 2} $$",
        description: "Resembles the physical splash of a water drop. It is multimodal and highly symmetrical, making it a beautiful topological structure to observe and a decent test for optimizers.",
        generate: () => {
            const {x, y, z} = generateGrid(-5.12, 5.12, 0.15, -5.12, 5.12, 0.15, (x, y) => {
                let r2 = x*x + y*y;
                return -(1 + Math.cos(12 * Math.sqrt(r2))) / (0.5 * r2 + 2);
            });
            return { data: [{ z, x, y, type: 'surface', colorscale: 'Cyan' }], type: 'surface' };
        }
    },
    eggcarton: {
        group: "Surfaces",
        name: "Egg Carton Surface",
        equation: "$$ z = \\sin(x) \\cdot \\cos(y) $$",
        description: "A perfectly repeating lattice of peaks and pits resembling a conventional egg carton. It perfectly visually represents a 2D standing wave interference pattern.",
        generate: () => {
            const {x, y, z} = generateGrid(-10, 10, 0.3, -10, 10, 0.3, (x, y) => Math.sin(x) * Math.cos(y));
            return { data: [{ z, x, y, type: 'surface', colorscale: 'Portland' }], type: 'surface' };
        }
    },
    torus: {
        group: "Parametric Surfaces",
        name: "The Torus",
        equation: "$$ x = (R + r\\cos(v))\\cos(u), \\; y = (R + r\\cos(v))\\sin(u), \\; z = r\\sin(v) $$",
        description: "The mathematical donut. A surface of revolution generated by revolving a circle in three-dimensional space about an axis coplanar with the circle.",
        generate: () => {
            let R = 3, r = 1;
            const {x, y, z} = generateParametric(0, 2*Math.PI, 60, 0, 2*Math.PI, 40, (u, v) => ({
                x: (R + r*Math.cos(v)) * Math.cos(u),
                y: (R + r*Math.cos(v)) * Math.sin(u),
                z: r * Math.sin(v)
            }));
            return { data: [{ x, y, z, type: 'surface', colorscale: 'Viridis' }], type: 'surface' };
        }
    },
    mobius: {
        group: "Parametric Surfaces",
        name: "Möbius Strip",
        equation: "$$ x = \\left(1 + \\frac{v}{2}\\cos\\frac{u}{2}\\right)\\cos(u), \\; y = \\left(1 + \\frac{v}{2}\\cos\\frac{u}{2}\\right)\\sin(u) $$",
        description: "A surface with only one side and one boundary curve. If you trace a line along the center, you will traverse both 'sides' before returning to your starting point.",
        generate: () => {
            const {x, y, z} = generateParametric(0, 2*Math.PI, 80, -1, 1, 20, (u, v) => ({
                x: (1 + (v/2)*Math.cos(u/2)) * Math.cos(u),
                y: (1 + (v/2)*Math.cos(u/2)) * Math.sin(u),
                z: (v/2) * Math.sin(u/2)
            }));
            return { data: [{ x, y, z, type: 'surface', colorscale: 'Plasma' }], type: 'surface' };
        }
    },
    helicoid: {
        group: "Parametric Surfaces",
        name: "Helicoid",
        equation: "$$ x = u\\cos(v), \\; y = u\\sin(v), \\; z = c v $$",
        description: "A minimal surface (locally area-minimizing) that resembles a spiral staircase. It is the only ruled minimal surface other than the plane.",
        generate: () => {
            let c = 0.5;
            const {x, y, z} = generateParametric(-3, 3, 40, -Math.PI*2, Math.PI*2, 80, (u, v) => ({
                x: u * Math.cos(v),
                y: u * Math.sin(v),
                z: c * v
            }));
            return { data: [{ x, y, z, type: 'surface', colorscale: 'Magma' }], type: 'surface' };
        }
    },
    catenoid: {
        group: "Parametric Surfaces",
        name: "Catenoid",
        equation: "$$ x = c \\cosh\\left(\\frac{v}{c}\\right) \\cos(u), \\; y = c \\cosh\\left(\\frac{v}{c}\\right) \\sin(u), \\; z = v $$",
        description: "Discovered by Leonhard Euler in 1744, it was the first non-trivial minimal surface discovered. It perfectly describes the shape of a soap film formed between two circular rings.",
        generate: () => {
            let c = 1;
            const {x, y, z} = generateParametric(0, 2*Math.PI, 60, -2, 2, 40, (u, v) => ({
                x: c * Math.cosh(v/c) * Math.cos(u),
                y: c * Math.cosh(v/c) * Math.sin(u),
                z: v
            }));
            return { data: [{ x, y, z, type: 'surface', colorscale: 'Earth' }], type: 'surface' };
        }
    },
    enneper: {
        group: "Parametric Surfaces",
        name: "Enneper Surface",
        equation: "$$ x = u(1-\\frac{u^2}{3}+v^2), \\; y = -v(1-\\frac{v^2}{3}+u^2), \\; z = u^2 - v^2 $$",
        description: "A self-intersecting minimal surface that is wonderfully symmetric. It can be described algebraically and acts as a standard subject in differential geometry.",
        generate: () => {
            const {x, y, z} = generateParametric(-2, 2, 50, -2, 2, 50, (u, v) => ({
                x: u * (1 - u*u/3 + v*v) / 3,
                y: -v * (1 - v*v/3 + u*u) / 3,
                z: (u*u - v*v) / 3
            }));
            return { data: [{ x, y, z, type: 'surface', colorscale: 'Inferno' }], type: 'surface' };
        }
    },
    sphere: {
        group: "Parametric Surfaces",
        name: "Parametric Sphere",
        equation: "$$ x = r\\sin(u)\\cos(v), \\; y = r\\sin(u)\\sin(v), \\; z = r\\cos(u) $$",
        description: "The most basic and perfect 3D manifold. Represented here using its spherical coordinate mapping.",
        generate: () => {
            let r = 2;
            const {x, y, z} = generateParametric(0, Math.PI, 40, 0, 2*Math.PI, 60, (u, v) => ({
                x: r * Math.sin(u) * Math.cos(v),
                y: r * Math.sin(u) * Math.sin(v),
                z: r * Math.cos(u)
            }));
            return { data: [{ x, y, z, type: 'surface', colorscale: 'Electric' }], type: 'surface' };
        }
    },

    trefoil: {
        group: "3D Curves & Knots",
        name: "Trefoil Knot",
        equation: "$$ x = \\sin(t) + 2\\sin(2t), \\; y = \\cos(t) - 2\\cos(2t), \\; z = -\\sin(3t) $$",
        description: "The simplest example of a nontrivial knot. It cannot be 'untied' into a circle without cutting it. Mathematically, it is fundamentally studied in knot theory.",
        generate: () => {
            let x=[], y=[], z=[];
            for(let t=0; t<=Math.PI*2.05; t+=0.02) {
                x.push(Math.sin(t) + 2*Math.sin(2*t));
                y.push(Math.cos(t) - 2*Math.cos(2*t));
                z.push(-Math.sin(3*t));
            }
            return { data: [{ x, y, z, type: 'scatter3d', mode: 'lines', line: { color: z, colorscale: 'Cyan', width: 10 } }], type: 'line' };
        }
    },
    lissajous3d: {
        group: "3D Curves & Knots",
        name: "3D Lissajous Curve",
        equation: "$$ x = \\sin(3t + \\pi/2), \\; y = \\sin(4t), \\; z = \\sin(5t) $$",
        description: "The graph of a system of parametric equations which describe complex harmonic motion. Often seen on oscilloscopes in 2D, its 3D counterpart weaves beautiful, enclosed paths.",
        generate: () => {
            let x=[], y=[], z=[];
            for(let t=0; t<=Math.PI*2.05; t+=0.01) {
                x.push(Math.sin(3*t + Math.PI/2));
                y.push(Math.sin(4*t));
                z.push(Math.sin(5*t));
            }
            return { data: [{ x, y, z, type: 'scatter3d', mode: 'lines', line: { color: x, colorscale: 'Rainbow', width: 6 } }], type: 'line' };
        }
    },
    rossler: {
        group: "Attractors",
        name: "Rössler Attractor",
        equation: "$$ \\dot{x} = -y - z, \\; \\dot{y} = x + ay, \\; \\dot{z} = b + z(x - c) $$",
        description: "Designed by Otto Rössler in 1976. This attractor is simpler than the Lorenz attractor and was designed specifically to be as simple as possible while still exhibiting chaos.",
        generate: () => {
            let a=0.2, b=0.2, c=5.7;
            let {x, y, z} = generateAttractor(10000, 0.04, {x:1, y:1, z:1}, (x, y, z) => ({
                dx: -y - z,
                dy: x + a*y,
                dz: b + z*(x - c)
            }));
            return { data: [{ x, y, z, type: 'scatter3d', mode: 'lines', line: { color: z, colorscale: 'Earth', width: 3 } }], type: 'line' };
        }
    },
    chen: {
        group: "Attractors",
        name: "Chen Attractor",
        equation: "$$ \\dot{x} = a(y - x), \\; \\dot{y} = (c - a)x - xz + cy, \\; \\dot{z} = xy - bz $$",
        description: "Discovered in 1999, the Chen system is dynamically more complex and topologically more intricate than the Lorenz system, despite their structural similarities.",
        generate: () => {
            let a=35, b=3, c=28;
            let {x, y, z} = generateAttractor(8000, 0.005, {x:5, y:10, z:10}, (x, y, z) => ({
                dx: a*(y - x),
                dy: (c - a)*x - x*z + c*y,
                dz: x*y - b*z
            }));
            return { data: [{ x, y, z, type: 'scatter3d', mode: 'lines', line: { color: z, colorscale: 'Electric', width: 2.5 } }], type: 'line' };
        }
    },
    thomas: {
        group: "Attractors",
        name: "Thomas' Cyclically Symmetric Attractor",
        equation: "$$ \\dot{x} = \\sin(y) - bx, \\; \\dot{y} = \\sin(z) - by, \\; \\dot{z} = \\sin(x) - bz $$",
        description: "Unique for its beautiful cyclical symmetry. Unlike most attractors that bundle into two 'wings', Thomas' attractor forms a mesmerizing, labyrinthine lattice in 3D space.",
        generate: () => {
            let b = 0.208186;
            let {x, y, z} = generateAttractor(15000, 0.05, {x:1, y:1.1, z:1}, (x, y, z) => ({
                dx: Math.sin(y) - b*x,
                dy: Math.sin(z) - b*y,
                dz: Math.sin(x) - b*z
            }));
            return { data: [{ x, y, z, type: 'scatter3d', mode: 'lines', line: { color: x, colorscale: 'Picnic', width: 2 } }], type: 'line' };
        }
    },
    halvorsen: {
        group: "Attractors",
        name: "Halvorsen Attractor",
        equation: "$$ \\dot{x} = -ax - 4y - 4z - y^2 $$",
        description: "Another cyclically symmetric chaotic attractor. Its trajectories spin wildly out from the origin before being pulled back, forming an elegant, flower-like geometry.",
        generate: () => {
            let a = 1.89;
            let {x, y, z} = generateAttractor(15000, 0.01, {x:1, y:0, z:0}, (x, y, z) => ({
                dx: -a*x - 4*y - 4*z - y*y,
                dy: -a*y - 4*z - 4*x - z*z,
                dz: -a*z - 4*x - 4*y - x*x
            }));
            return { data: [{ x, y, z, type: 'scatter3d', mode: 'lines', line: { color: z, colorscale: 'Magma', width: 2.5 } }], type: 'line' };
        }
    },
    aizawa: {
        group: "Attractors",
        name: "Aizawa Attractor",
        equation: "$$ \\dot{x} = (z-0.7)x - 3.5y, \\; \\dot{y} = 3.5x + (z-0.7)y $$",
        description: "A highly intricate attractor that creates a dense spherical cluster with a distinct tube burrowing straight through its axis. It exhibits stunning rotational symmetry.",
        generate: () => {
            let {x, y, z} = generateAttractor(12000, 0.015, {x:0.1, y:0, z:0}, (x, y, z) => ({
                dx: (z - 0.7)*x - 3.5*y,
                dy: 3.5*x + (z - 0.7)*y,
                dz: 0.6 + 0.95*z - Math.pow(z,3)/3 - (x*x + y*y)*(1 + 0.25*z) + 0.1*z*x*x*x
            }));
            return { data: [{ x, y, z, type: 'scatter3d', mode: 'lines', line: { color: z, colorscale: 'Inferno', width: 2 } }], type: 'line' };
        }
    },
    rabinovich: {
        group: "Attractors",
        name: "Rabinovich-Fabrikant",
        equation: "$$ \\dot{x} = y(z - 1 + x^2) + \\gamma x, \\; \\dot{y} = x(3z + 1 - x^2) + \\gamma y $$",
        description: "Models the stochasticity in modulation of waves. Depending on parameters, it can produce incredibly varied and delicate geometric structures.",
        generate: () => {
            let a = 0.1, b = 0.2875; // a is gamma, b is alpha in literature
            let {x, y, z} = generateAttractor(10000, 0.01, {x:-1, y:0, z:0.5}, (x, y, z) => ({
                dx: y*(z - 1 + x*x) + a*x,
                dy: x*(3*z + 1 - x*x) + a*y,
                dz: -2*z*(b + x*y)
            }));
            return { data: [{ x, y, z, type: 'scatter3d', mode: 'lines', line: { color: y, colorscale: 'Viridis', width: 2 } }], type: 'line' };
        }
    },
    lorenz84: {
        group: "Attractors",
        name: "Lorenz-84 Attractor",
        equation: "$$ \\dot{x} = -ax - y^2 - z^2 + aF, \\; \\dot{y} = -y + xy - bxz + G $$",
        description: "A later, simpler model by Edward Lorenz designed to study atmospheric circulation, focusing on the interactions between westerly winds and large-scale eddies.",
        generate: () => {
            let a=0.25, b=4, F=8, G=1;
            let {x, y, z} = generateAttractor(15000, 0.01, {x:1, y:1, z:1}, (x, y, z) => ({
                dx: -a*x - y*y - z*z + a*F,
                dy: -y + x*y - b*x*z + G,
                dz: -z + b*x*y + x*z
            }));
            return { data: [{ x, y, z, type: 'scatter3d', mode: 'lines', line: { color: z, colorscale: 'Plasma', width: 2 } }], type: 'line' };
        }
    },
    sprottA: {
        group: "Attractors",
        name: "Sprott System A",
        equation: "$$ \\dot{x} = y, \\; \\dot{y} = -x + yz, \\; \\dot{z} = 1 - y^2 $$",
        description: "Discovered by J.C. Sprott through an exhaustive automated computer search of simple differential equations. It is one of the simplest expressions that still yields chaos.",
        generate: () => {
            let {x, y, z} = generateAttractor(12000, 0.02, {x:0, y:0, z:0}, (x, y, z) => ({
                dx: y,
                dy: -x + y*z,
                dz: 1 - y*y
            }));
            return { data: [{ x, y, z, type: 'scatter3d', mode: 'lines', line: { color: x, colorscale: 'Cyan', width: 2 } }], type: 'line' };
        }
    },
    dini: {
        group: "Parametric Surfaces",
        name: "Dini's Surface",
        equation: "$$ x = \\cos(u)\\sin(v), \\; y = \\sin(u)\\sin(v), \\; z = \\cos(v) + \\ln(\\tan(\\frac{v}{2})) + cu $$",
        description: "A surface with constant negative curvature that resembles a twisted pseudosphere. It's named after Ulisse Dini and looks like a beautiful spiraling funnel.",
        generate: () => {
            let c = 0.2;
            const {x, y, z} = generateParametric(0, 4*Math.PI, 80, 0.01, 2, 40, (u, v) => ({
                x: Math.cos(u) * Math.sin(v),
                y: Math.sin(u) * Math.sin(v),
                z: Math.cos(v) + Math.log(Math.tan(v/2)) + c*u
            }));
            return { data: [{ x, y, z, type: 'surface', colorscale: 'Viridis' }], type: 'surface' };
        }
    },
    roman: {
        group: "Parametric Surfaces",
        name: "Steiner's Roman Surface",
        equation: "$$ x = r^2\\cos(u)\\cos(v)\\sin(v), \\; y = r^2\\sin(u)\\cos(v)\\sin(v), \\; z = r^2\\cos(u)\\sin(u)\\cos^2(v) $$",
        description: "Discovered by Jakob Steiner in Rome in 1852. It is a highly self-intersecting mapping of the real projective plane into three-dimensional space, containing four distinct 'pinch points'.",
        generate: () => {
            let r = 2;
            const {x, y, z} = generateParametric(0, Math.PI, 60, 0, Math.PI/2, 60, (u, v) => ({
                x: r*r * Math.cos(u) * Math.cos(v) * Math.sin(v),
                y: r*r * Math.sin(u) * Math.cos(v) * Math.sin(v),
                z: r*r * Math.cos(u) * Math.sin(u) * Math.cos(v)*Math.cos(v)
            }));
            return { data: [{ x, y, z, type: 'surface', colorscale: 'Plasma' }], type: 'surface' };
        }
    },
    klein: {
        group: "Parametric Surfaces",
        name: "Figure-8 Klein Bottle",
        equation: "$$ x = (r + \\cos\\frac{u}{2}\\sin(v) - \\sin\\frac{u}{2}\\sin(2v))\\cos(u) $$",
        description: "A non-orientable surface with no distinct 'inside' and 'outside'. This is the 'figure-8' or 'bagel' immersion of the 4D Klein bottle mapped into 3D space.",
        generate: () => {
            let r = 2;
            const {x, y, z} = generateParametric(0, 2*Math.PI, 60, 0, 2*Math.PI, 60, (u, v) => {
                let cx = r + Math.cos(u/2)*Math.sin(v) - Math.sin(u/2)*Math.sin(2*v);
                return {
                    x: cx * Math.cos(u),
                    y: cx * Math.sin(u),
                    z: Math.sin(u/2)*Math.sin(v) + Math.cos(u/2)*Math.sin(2*v)
                };
            });
            return { data: [{ x, y, z, type: 'surface', colorscale: 'Magma' }], type: 'surface' };
        }
    },
    nosehoover: {
        group: "Attractors",
        name: "Nosé-Hoover Attractor",
        equation: "$$ \\dot{x} = y, \\; \\dot{y} = -x + yz, \\; \\dot{z} = a - y^2 $$",
        description: "Originally developed for molecular dynamics simulations to keep temperature constant. Its dynamic system exhibits striking chaotic properties with a beautiful, symmetrical hollow core.",
        generate: () => {
            let a = 1.5;
            let {x, y, z} = generateAttractor(15000, 0.015, {x:1, y:0, z:0}, (x, y, z) => ({
                dx: y,
                dy: -x + y*z,
                dz: a - y*y
            }));
            return { data: [{ x, y, z, type: 'scatter3d', mode: 'lines', line: { color: z, colorscale: 'Jet', width: 2 } }], type: 'line' };
        }
    },
    burkeshaw: {
        group: "Attractors",
        name: "Burke-Shaw Attractor",
        equation: "$$ \\dot{x} = -s(x+y), \\; \\dot{y} = -y - sxz, \\; \\dot{z} = sxy + v $$",
        description: "Developed as a variation of the Lorenz system, this attractor drops the 'y' term in the z-derivative. It results in a stunningly clean and symmetric butterfly-like structure.",
        generate: () => {
            let s = 10, v = 4.272;
            let {x, y, z} = generateAttractor(12000, 0.01, {x:1, y:0, z:0}, (x, y, z) => ({
                dx: -s*(x + y),
                dy: -y - s*x*z,
                dz: s*x*y + v
            }));
            return { data: [{ x, y, z, type: 'scatter3d', mode: 'lines', line: { color: x, colorscale: 'Electric', width: 2 } }], type: 'line' };
        }
    },
    catalan: {
        group: "Parametric Surfaces",
        name: "Catalan's Surface",
        equation: "$$ x = u - \\sin(u)\\cosh(v), \\; y = 1 - \\cos(u)\\cosh(v), \\; z = 4\\sin(\\frac{u}{2})\\sinh(\\frac{v}{2}) $$",
        description: "Discovered by Eugène Charles Catalan in 1855, this is a beautiful minimal surface (it locally minimizes its area). It is periodic and contains real cycloids.",
        generate: () => {
            const {x, y, z} = generateParametric(-Math.PI, Math.PI, 60, -2, 2, 40, (u, v) => ({
                x: u - Math.sin(u) * Math.cosh(v),
                y: 1 - Math.cos(u) * Math.cosh(v),
                z: 4 * Math.sin(u/2) * Math.sinh(v/2)
            }));
            return { data: [{ x, y, z, type: 'surface', colorscale: 'Earth' }], type: 'surface' };
        }
    }
};

// Standard styling layout for Plotly (Dark Theme Optimized)
const getLayout = (isLine = false) => ({
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    margin: { t: 0, b: 0, l: 0, r: 0 },
    font: { family: 'Inter, sans-serif', color: '#94a3b8' },
    scene: {
        xaxis: { visible: false, showgrid: false, zeroline: false },
        yaxis: { visible: false, showgrid: false, zeroline: false },
        zaxis: { visible: false, showgrid: false, zeroline: false },
        camera: { eye: { x: 1.4, y: 1.4, z: 1.2 } },
        bgcolor: 'transparent'
    }
});

// Initialize UI Elements
const select = document.getElementById('function-select');

// Group and populate the dropdown
const groups = {};
for (const [key, val] of Object.entries(mathData)) {
    if (!groups[val.group]) groups[val.group] = [];
    groups[val.group].push({key, name: val.name});
}

for (const [groupName, items] of Object.entries(groups)) {
    const optgroup = document.createElement('optgroup');
    optgroup.label = groupName;
    items.forEach(item => {
        const opt = document.createElement('option');
        opt.value = item.key;
        opt.textContent = item.name;
        optgroup.appendChild(opt);
    });
    select.appendChild(optgroup);
}

async function renderPlot(funcKey) {
    const config = mathData[funcKey];
    const loader = document.getElementById('loader');
    const infoContainer = document.getElementById('info-container');
    
    // Show loader
    loader.style.opacity = '1';
    loader.style.pointerEvents = 'all';
    
    // Add subtle exit animation to info
    infoContainer.classList.remove('fade-in');
    
    // Small timeout to allow DOM to paint the loader
    setTimeout(() => {
        // Update text details
        document.getElementById('func-name').innerText = config.name;
        document.getElementById('func-eq').innerHTML = config.equation;
        document.getElementById('func-desc').innerText = config.description;
        document.getElementById('func-type-badge').innerText = config.group;
        
        // Trigger MathJax re-render
        if (window.MathJax) {
            MathJax.typesetPromise([document.getElementById('func-eq')]).catch(err => console.error(err));
        }

        // Generate Data
        const plotData = config.generate();
        
        // Hide loader and render Plotly
        Plotly.react('plot', plotData.data, getLayout(plotData.type === 'line'), { 
            displayModeBar: false, 
            responsive: true 
        }).then(() => {
            loader.style.opacity = '0';
            loader.style.pointerEvents = 'none';
            
            // Trigger enter animation
            void infoContainer.offsetWidth; // trigger reflow
            infoContainer.classList.add('fade-in');
        });
    }, 50); // 50ms delay is enough for browser to paint loader
}

// Event Listeners
select.addEventListener('change', (e) => {
    renderPlot(e.target.value);
});

// Initial Render on Load
window.onload = () => renderPlot('sinc');

// Handle window resizing smoothly for Plotly
window.addEventListener('resize', () => {
    let plotDiv = document.getElementById('plot');
    if(plotDiv.data) {
        Plotly.Plots.resize(plotDiv);
    }
});
