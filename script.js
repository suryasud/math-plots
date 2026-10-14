// Database of our mathematical surfaces
const mathData = {
    sinc: {
        name: "The Sinc Function",
        equation: "$$ z = \\frac{\\sin(R)}{R} \\quad \\text{where } R = \\sqrt{x^2 + y^2} $$",
        description: "Often described as a mathematical raindrop hitting a pond, the unnormalized 2D Sinc function creates perfectly decaying concentric ripples. It acts as the ideal interpolation filter in signal processing.",
        generate: () => {
            let z = [], x = [], y = [];
            for (let i = -10; i <= 10; i += 0.5) { x.push(i); y.push(i); }
            for (let i = 0; i < x.length; i++) {
                let z_row = [];
                for (let j = 0; j < y.length; j++) {
                    let r = Math.sqrt(x[i]*x[i] + y[j]*y[j]) + 0.001; // Avoid divide by zero
                    z_row.push(Math.sin(r) / r);
                }
                z.push(z_row);
            }
            return { data: [{ z, x, y, type: 'surface', colorscale: 'Cyan' }], type: 'surface' };
        }
    },
    gaussian: {
        name: "Bivariate Gaussian",
        equation: "$$ f(x,y) = \\frac{1}{2\\pi\\sigma^2} e^{-\\frac{x^2+y^2}{2\\sigma^2}} $$",
        description: "The classic 'Bell Curve' extended into 3D. This probability distribution is a foundational block of statistics, naturally emerging everywhere from quantum mechanics to the behavior of vast populations.",
        generate: () => {
            let z = [], x = [], y = [];
            let sigma = 2;
            for (let i = -6; i <= 6; i += 0.3) { x.push(i); y.push(i); }
            for (let i = 0; i < x.length; i++) {
                let z_row = [];
                for (let j = 0; j < y.length; j++) {
                    let val = (1 / (2 * Math.PI * sigma**2)) * Math.exp(-(x[i]**2 + y[j]**2) / (2 * sigma**2));
                    z_row.push(val);
                }
                z.push(z_row);
            }
            return { data: [{ z, x, y, type: 'surface', colorscale: 'Viridis' }], type: 'surface' };
        }
    },
    saddle: {
        name: "Hyperbolic Paraboloid",
        equation: "$$ z = x^2 - y^2 $$",
        description: "Known as a Saddle Point or Minimax, this gorgeous surface curves upwards in one direction and downwards in the other. It's notoriously difficult to navigate in deep learning optimization, as algorithms can easily stall here during gradient descent instead of finding the true minimum.",
        generate: () => {
            let z = [], x = [], y = [];
            for (let i = -5; i <= 5; i += 0.4) { x.push(i); y.push(i); }
            for (let i = 0; i < x.length; i++) {
                let z_row = [];
                for (let j = 0; j < y.length; j++) {
                    z_row.push((x[i]*x[i]) - (y[j]*y[j]));
                }
                z.push(z_row);
            }
            return { data: [{ z, x, y, type: 'surface', colorscale: 'Plasma' }], type: 'surface' };
        }
    },
    lorenz: {
        name: "Lorenz Attractor",
        equation: "$$ \\frac{dx}{dt} = \\sigma(y-x), \\; \\frac{dy}{dt} = x(\\rho-z)-y $$",
        description: "The blueprint of chaos. Originally designed to model atmospheric convection, it revealed the 'butterfly effect'—how tiny changes in initial conditions result in completely wildly different, beautifully chaotic trajectories.",
        generate: () => {
            let x = [], y = [], z = [];
            let cx = 0.1, cy = 0, cz = 0;
            let dt = 0.01;
            let sigma = 10, rho = 28, beta = 8/3;
            for(let i=0; i<5000; i++) {
                let dx = sigma * (cy - cx);
                let dy = cx * (rho - cz) - cy;
                let dz = cx * cy - beta * cz;
                cx += dx * dt; cy += dy * dt; cz += dz * dt;
                x.push(cx); y.push(cy); z.push(cz);
            }
            return { 
                data: [{ x, y, z, type: 'scatter3d', mode: 'lines', line: { color: z, colorscale: 'Inferno', width: 4 } }],
                type: 'line'
            };
        }
    }
};

// Standard styling layout for Plotly
const getLayout = (isLine = false) => ({
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    margin: { t: 0, b: 0, l: 0, r: 0 },
    scene: {
        xaxis: { visible: false },
        yaxis: { visible: false },
        zaxis: { visible: false },
        camera: {
            eye: { x: 1.5, y: 1.5, z: 1.2 }
        }
    }
});

// Main render function
function renderPlot(funcKey) {
    const config = mathData[funcKey];
    
    // Update UI Elements
    document.getElementById('func-name').innerText = config.name;
    document.getElementById('func-eq').innerHTML = config.equation;
    document.getElementById('func-desc').innerText = config.description;
    
    // Trigger MathJax to re-render the new equation
    if (window.MathJax) {
        MathJax.typesetPromise([document.getElementById('func-eq')]).catch(err => console.error(err));
    }

    // Generate and plot data
    const plotData = config.generate();
    Plotly.react('plot', plotData.data, getLayout(plotData.type === 'line'), { displayModeBar: false, responsive: true });
}

// Event Listeners
document.getElementById('function-select').addEventListener('change', (e) => {
    renderPlot(e.target.value);
});

// Initial Render
window.onload = () => renderPlot('sinc');

// Handle window resizing smoothly
window.addEventListener('resize', () => {
    Plotly.Plots.resize(document.getElementById('plot'));
});
