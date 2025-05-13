# SVG Generator

An advanced SVG generator toolkit built for competition-ready graphics with optimized file sizes.

## Features

- Size-constrained SVG generation with automated optimization
- 3D perspective rendering for complex visualizations
- Layered composition system with z-index support
- String art pattern generation
- Chord map visualization
- Multiple gradient effects and styling options

## Installation

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install -e .
```

## Basic Usage

```python
from svg_generator.core.orchestrator import SceneOrchestrator

# Create a scene with size constraints
scene = SceneOrchestrator(width=800, height=600, max_size_kb=10)

# Create layers for composition
background = scene.create_layer("background", z_index=0)
foreground = scene.create_layer("foreground", z_index=10)

# Add elements to layers
scene.add_to_layer("background", "rect", {
    "x": 0, "y": 0, "width": 800, "height": 600, "fill": "#f0f0f0"
})

scene.add_to_layer("foreground", "circle", {
    "cx": 400, "cy": 300, "r": 150, "fill": "blue", "fill-opacity": 0.6
})

# Generate the final SVG
svg = scene.generate_svg()

# Validate size constraints
if scene.validate():
    print("SVG meets competition requirements!")
else:
    print("SVG exceeds size limits.")

# Save to file
with open("output.svg", "w") as f:
    f.write(svg)
```

## Advanced Examples

Check the `examples/` directory for more complex visualization samples:

- 3D grid rendering
- String art patterns
- Chord map visualizations
- Gradient effects

## Development

```bash
# Install development dependencies
pip install -r requirements/requirements-dev.txt

# Run tests
pytest tests/

# Format code
black src/ tests/

# Check types
mypy src/
```

## License

MIT License
