# Advanced Usage Guide

This guide covers more advanced features and usage patterns for the SVG Generator library.

## 3D Rendering Techniques

The SVG Generator includes a powerful 3D rendering system that projects 3D objects onto a 2D SVG canvas.

### Grid3D Renderer

```python
from svg_generator.rendering.grid3d import Grid3DRenderer

# Create a renderer with custom dimensions
renderer = Grid3DRenderer(width=800, height=600)

# Generate a 3D cube
cube = renderer.generate_cube([0, 0, 0], 200, stroke="#333", stroke_width="1.5")

# Generate a 3D grid
grid = renderer.generate_grid([0, 0, 0], 300, 10, stroke="#ddd")

# Generate a radial pattern with perspective
radial = renderer.generate_radial_pattern(200, segments=36, rings=8, stroke="#555")
```

## Chord Map Visualizations

Chord maps are useful for visualizing relationships between entities:

```python
from svg_generator.rendering.chord_map import ChordMapRenderer

# Create the renderer
renderer = ChordMapRenderer(width=800, height=600)

# Create a chord diagram from relationship data
data = [
    {"source": "A", "target": "B", "value": 5},
    {"source": "B", "target": "C", "value": 3},
    {"source": "A", "target": "C", "value": 2},
    {"source": "D", "target": "A", "value": 7}
]

chord_diagram = renderer.generate_chord_diagram(
    data, radius=250, stroke="#333", stroke_width="1.5"
)

# Create a chord diagram from a matrix
matrix = [
    [0, 5, 2, 7],
    [5, 0, 3, 0],
    [2, 3, 0, 1],
    [7, 0, 1, 0]
]
labels = ["A", "B", "C", "D"]

matrix_chord = renderer.generate_matrix_chord(
    matrix, labels, radius=250,
    entity_fill="#f0f0f0", stroke="#444"
)
```

## String Art Patterns

Create beautiful string art patterns:

```python
from svg_generator.layout.patterns import StringArtPatterns

# Create a circle pattern
circle_pattern = StringArtPatterns.create_circle_pattern(
    400, 300, 200, 48, stroke="#444", stroke_width="0.5"
)

# Create a spiral pattern
spiral_pattern = StringArtPatterns.create_spiral_pattern(
    400, 300, 50, 200, 3, 100, stroke="#222", stroke_width="0.5"
)

# Create a Lissajous curve pattern
lissajous_pattern = StringArtPatterns.create_lissajous_pattern(
    400, 300, 150, 150, 3, 2, 0.5, 300,
    stroke="#333", stroke_width="0.5", fill="none"
)
```

## Gradient Effects

Create and use advanced gradient effects:

```python
from svg_generator.elements.gradients import GradientLibrary
import xml.etree.ElementTree as ET

# Create an SVG element
svg = ET.Element("svg")
svg.set("xmlns", "http://www.w3.org/2000/svg")
svg.set("width", "800")
svg.set("height", "600")

# Create defs section
defs = ET.SubElement(svg, "defs")

# Create a linear gradient
linear_gradient = GradientLibrary.create_linear_gradient(
    "myGradient", 0, 0, 1, 0,
    stops=[
        {"offset": "0%", "color": "#ff0000"},
        {"offset": "50%", "color": "#00ff00"},
        {"offset": "100%", "color": "#0000ff"}
    ]
)
defs.append(linear_gradient)

# Create a radial gradient
radial_gradient = GradientLibrary.create_radial_gradient(
    "myRadialGradient", 0.5, 0.5, 0.5, 0.3, 0.3,
    stops=[
        {"offset": "0%", "color": "#ffffff"},
        {"offset": "100%", "color": "#000000", "opacity": 0.8}
    ]
)
defs.append(radial_gradient)

# Create a rainbow gradient
rainbow = GradientLibrary.rainbow_gradient("rainbowGradient", horizontal=False)
defs.append(rainbow)

# Create a metallic effect gradient
metallic = GradientLibrary.metallic_gradient("metallicGradient", base_color="#888888")
defs.append(metallic)

# Use the gradients in elements
rect1 = ET.SubElement(svg, "rect")
rect1.set("x", "50")
rect1.set("y", "50")
rect1.set("width", "200")
rect1.set("height", "100")
rect1.set("fill", "url(#myGradient)")

circle = ET.SubElement(svg, "circle")
circle.set("cx", "400")
circle.set("cy", "100")
circle.set("r", "50")
circle.set("fill", "url(#myRadialGradient)")

rect2 = ET.SubElement(svg, "rect")
rect2.set("x", "50")
rect2.set("y", "200")
rect2.set("width", "200")
rect2.set("height", "100")
rect2.set("fill", "url(#rainbowGradient)")

rect3 = ET.SubElement(svg, "rect")
rect3.set("x", "50")
rect3.set("y", "350")
rect3.set("width", "200")
rect3.set("height", "100")
rect3.set("fill", "url(#metallicGradient)")
```

## Size Optimization

For competition scenarios, size optimization is critical:

```python
from svg_generator.utils.compliance import SanitizeUtils
from svg_generator.utils.optimization import CompetitionOptimizer

# Generate your SVG content
# ...

# Optimize the SVG for competition submission
optimizer = CompetitionOptimizer(max_size_kb=10)
optimized_svg, size_kb = optimizer.optimize(svg_content)

print(f"Optimized SVG size: {size_kb:.2f} KB")

# Ensure compliance with competition rules
compliant_svg = SanitizeUtils.ensure_compliance(svg_content, max_size_kb=10)
```

## Integration with External Tools

You can export your SVG for use with other tools:

```python
# Save as SVG
with open("output.svg", "w") as f:
    f.write(svg_content)

# Convert to PNG using Pillow (requires cairosvg)
from cairosvg import svg2png

svg2png(bytestring=svg_content, write_to="output.png", 
        output_width=800, output_height=600)
```

## Batch Processing

For batch generation of SVGs:

```python
import os
from svg_generator.core.orchestrator import SceneOrchestrator

def generate_batch(output_dir, count=10, width=800, height=600):
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(count):
        scene = SceneOrchestrator(width, height)
        
        # Set up layers
        scene.create_layer("background", z_index=0)
        scene.create_layer("content", z_index=10)
        
        # Add elements with variations
        scene.add_to_layer("background", "rect", {
            "x": 0, "y": 0, "width": width, "height": height,
            "fill": f"hsl({(i * 36) % 360}, 80%, 90%)"
        })
        
        # Add varied content
        for j in range(5):
            scene.add_to_layer("content", "circle", {
                "cx": width * (0.2 + 0.15 * j),
                "cy": height * 0.5,
                "r": 30 + i * 3,
                "fill": f"hsl({(i * 36 + j * 20) % 360}, 80%, 50%)",
                "stroke": "#333",
                "stroke-width": "1"
            })
        
        # Generate SVG
        svg = scene.generate_svg()
        
        # Save file
        with open(os.path.join(output_dir, f"svg_{i:03d}.svg"), "w") as f:
            f.write(svg)
```
