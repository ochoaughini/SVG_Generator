"""
Basic example of using the SVG generator to create a composition.
"""
import os
import math
from svg_generator.core.orchestrator import SceneOrchestrator
from svg_generator.rendering.grid3d import Grid3DRenderer
from svg_generator.layout.patterns import StringArtPatterns
from svg_generator.elements.gradients import GradientLibrary


def create_sample_svg():
    """Create a sample SVG using the generator library."""
    # Create scene with size constraints
    scene = SceneOrchestrator(width=800, height=600, max_size_kb=10)
    
    # Create layers for composition
    scene.create_layer("background", z_index=0)
    scene.create_layer("grid", z_index=5)
    scene.create_layer("patterns", z_index=10)
    scene.create_layer("foreground", z_index=15)
    
    # Add background
    scene.add_to_layer("background", "rect", {
        "x": 0, "y": 0, "width": 800, "height": 600, 
        "fill": "#f0f0f0"
    })
    
    # Add grid using the 3D grid renderer
    grid_renderer = Grid3DRenderer(width=800, height=600)
    grid = grid_renderer.generate_grid([0, 0, 0], 300, 10, 
                                      stroke="#dddddd", stroke_width="0.5")
    
    # We need to manually add the grid to our scene since it's a complex element
    layer = scene.layer_manager.get_layer("grid")
    if layer is not None:
        for child in grid:
            layer.append(child)
    
    # Add string art pattern
    pattern_layer = scene.layer_manager.get_layer("patterns")
    if pattern_layer is not None:
        pattern = StringArtPatterns.create_circle_pattern(
            400, 300, 200, 36, stroke="#2266aa", stroke_width="0.5"
        )
        for child in pattern:
            pattern_layer.append(child)
    
    # Add foreground elements
    scene.add_to_layer("foreground", "circle", {
        "cx": 400, "cy": 300, "r": 50, "fill": "#aa2266", "fill-opacity": "0.7"
    })
    
    # Add a gradient definition
    defs = scene.generator.add_element("defs", {})
    
    # Create a rainbow gradient
    rainbow = GradientLibrary.rainbow_gradient("rainbowGradient", horizontal=True)
    defs.append(rainbow)
    
    # Add an element using the gradient
    scene.add_to_layer("foreground", "rect", {
        "x": 300, "y": 400, "width": 200, "height": 80, 
        "fill": "url(#rainbowGradient)", "rx": "10", "ry": "10"
    })
    
    # Generate the final SVG
    svg = scene.generate_svg()
    
    # Save to file
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "output.svg")
    
    with open(output_path, "w") as f:
        f.write(svg)
        
    print(f"SVG saved to {output_path}")
    print(f"Size: {len(svg.encode('utf-8')) / 1024:.2f} KB")
    
    # Validate size constraints
    if scene.validate():
        print("SVG meets competition requirements!")
    else:
        print("SVG exceeds size limits.")
        

if __name__ == "__main__":
    create_sample_svg()
