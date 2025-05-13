"""
3D grid rendering for SVG with perspective effects.
"""
from typing import List, Tuple, Dict, Any, Optional
import math
import xml.etree.ElementTree as ET


class Grid3DRenderer:
    """
    Renders 3D grid structures in SVG with perspective effects.
    
    Implements various algorithms for 3D projections onto a 2D SVG canvas,
    with options for different viewpoints and rendering styles.
    """
    
    def __init__(self, width: float = 800, height: float = 600, 
                 fov: float = 60, z_near: float = 0.1, z_far: float = 100):
        """
        Initialize the 3D grid renderer.
        
        Args:
            width: Width of the view plane
            height: Height of the view plane
            fov: Field of view in degrees
            z_near: Near clipping plane distance
            z_far: Far clipping plane distance
        """
        self.width = width
        self.height = height
        self.fov = fov * math.pi / 180  # Convert to radians
        self.z_near = z_near
        self.z_far = z_far
        
        # Camera position and orientation
        self.camera_pos = [0, 0, -5]
        self.camera_target = [0, 0, 0]
        self.camera_up = [0, 1, 0]
        
    def _project_point(self, point: List[float]) -> Tuple[float, float]:
        """
        Project a 3D point onto the 2D canvas using perspective projection.
        
        Args:
            point: 3D point [x, y, z]
            
        Returns:
            2D projected point (x, y)
        """
        # Translate point relative to camera
        rel_x = point[0] - self.camera_pos[0]
        rel_y = point[1] - self.camera_pos[1]
        rel_z = point[2] - self.camera_pos[2]
        
        # Simple perspective projection
        if rel_z == 0:  # Avoid division by zero
            rel_z = 0.0001
            
        # Perspective division
        aspect = self.width / self.height
        scale = math.tan(self.fov / 2)
        
        projected_x = (rel_x / (rel_z * scale * aspect)) * (self.width / 2) + (self.width / 2)
        projected_y = (-rel_y / (rel_z * scale)) * (self.height / 2) + (self.height / 2)
        
        return (projected_x, projected_y)
        
    def generate_cube(self, center: List[float], size: float, **attributes) -> ET.Element:
        """
        Generate a 3D cube in SVG.
        
        Args:
            center: Center point of the cube [x, y, z]
            size: Size of the cube
            **attributes: Additional attributes for the cube lines
            
        Returns:
            A group element containing the cube lines
        """
        group = ET.Element("g")
        
        # Set default attributes
        if "stroke" not in attributes:
            attributes["stroke"] = "#000"
        if "stroke-width" not in attributes:
            attributes["stroke-width"] = "1"
        if "fill" not in attributes:
            attributes["fill"] = "none"
            
        # Define the cube vertices
        half_size = size / 2
        vertices = [
            [center[0] - half_size, center[1] - half_size, center[2] - half_size],  # 0: front bottom left
            [center[0] + half_size, center[1] - half_size, center[2] - half_size],  # 1: front bottom right
            [center[0] + half_size, center[1] + half_size, center[2] - half_size],  # 2: front top right
            [center[0] - half_size, center[1] + half_size, center[2] - half_size],  # 3: front top left
            [center[0] - half_size, center[1] - half_size, center[2] + half_size],  # 4: back bottom left
            [center[0] + half_size, center[1] - half_size, center[2] + half_size],  # 5: back bottom right
            [center[0] + half_size, center[1] + half_size, center[2] + half_size],  # 6: back top right
            [center[0] - half_size, center[1] + half_size, center[2] + half_size]   # 7: back top left
        ]
        
        # Define the edges
        edges = [
            # Front face
            (0, 1), (1, 2), (2, 3), (3, 0),
            # Back face
            (4, 5), (5, 6), (6, 7), (7, 4),
            # Connecting edges
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        
        # Project vertices
        projected_vertices = [self._project_point(v) for v in vertices]
        
        # Create lines for edges
        for edge in edges:
            start, end = edge
            line = ET.SubElement(group, "line")
            line.set("x1", str(projected_vertices[start][0]))
            line.set("y1", str(projected_vertices[start][1]))
            line.set("x2", str(projected_vertices[end][0]))
            line.set("y2", str(projected_vertices[end][1]))
            
            for key, value in attributes.items():
                line.set(key, str(value))
                
        return group
        
    def generate_grid(self, center: List[float], size: float, 
                     divisions: int, **attributes) -> ET.Element:
        """
        Generate a 3D grid in SVG.
        
        Args:
            center: Center point of the grid [x, y, z]
            size: Size of the grid
            divisions: Number of divisions along each axis
            **attributes: Additional attributes for the grid lines
            
        Returns:
            A group element containing the grid
        """
        group = ET.Element("g")
        
        # Set default attributes
        if "stroke" not in attributes:
            attributes["stroke"] = "#888"
        if "stroke-width" not in attributes:
            attributes["stroke-width"] = "0.5"
            
        half_size = size / 2
        step = size / divisions
        
        # Create horizontal grid lines (along X-axis)
        for i in range(divisions + 1):
            z = center[2] - half_size + i * step
            for j in range(divisions + 1):
                y = center[1] - half_size + j * step
                
                # Create horizontal line along X
                start = [center[0] - half_size, y, z]
                end = [center[0] + half_size, y, z]
                
                # Project points and create line
                start_2d = self._project_point(start)
                end_2d = self._project_point(end)
                
                line = ET.SubElement(group, "line")
                line.set("x1", str(start_2d[0]))
                line.set("y1", str(start_2d[1]))
                line.set("x2", str(end_2d[0]))
                line.set("y2", str(end_2d[1]))
                
                for key, value in attributes.items():
                    line.set(key, str(value))
                    
        # Create vertical grid lines (along Y-axis)
        for i in range(divisions + 1):
            z = center[2] - half_size + i * step
            for j in range(divisions + 1):
                x = center[0] - half_size + j * step
                
                # Create vertical line along Y
                start = [x, center[1] - half_size, z]
                end = [x, center[1] + half_size, z]
                
                # Project points and create line
                start_2d = self._project_point(start)
                end_2d = self._project_point(end)
                
                line = ET.SubElement(group, "line")
                line.set("x1", str(start_2d[0]))
                line.set("y1", str(start_2d[1]))
                line.set("x2", str(end_2d[0]))
                line.set("y2", str(end_2d[1]))
                
                for key, value in attributes.items():
                    line.set(key, str(value))
                    
        return group
        
    def generate_radial_pattern(self, radius: float, segments: int = 36, 
                               rings: int = 5, **attributes) -> ET.Element:
        """
        Generate a 3D radial pattern.
        
        Args:
            radius: Maximum radius of the pattern
            segments: Number of angular segments
            rings: Number of concentric rings
            **attributes: Additional attributes for the pattern
            
        Returns:
            A group element containing the radial pattern
        """
        group = ET.Element("g")
        
        # Set default attributes
        if "stroke" not in attributes:
            attributes["stroke"] = "#444"
        if "stroke-width" not in attributes:
            attributes["stroke-width"] = "0.5"
        if "fill" not in attributes:
            attributes["fill"] = "none"
            
        # Create rings
        for r in range(1, rings + 1):
            current_radius = radius * r / rings
            
            # Create circle points
            points = []
            for s in range(segments):
                angle = 2 * math.pi * s / segments
                x = current_radius * math.cos(angle)
                y = 0
                z = current_radius * math.sin(angle)
                
                # Transform to camera space
                points.append([x, y, z])
                
            # Project points
            projected_points = [self._project_point(p) for p in points]
            
            # Create path
            path = ET.SubElement(group, "path")
            d = f"M {projected_points[0][0]},{projected_points[0][1]}"
            for point in projected_points[1:]:
                d += f" L {point[0]},{point[1]}"
            d += " Z"  # Close the path
            
            path.set("d", d)
            for key, value in attributes.items():
                path.set(key, str(value))
                
        # Create radial lines
        for s in range(segments):
            angle = 2 * math.pi * s / segments
            
            start = [0, 0, 0]
            end = [radius * math.cos(angle), 0, radius * math.sin(angle)]
            
            # Project points
            start_2d = self._project_point(start)
            end_2d = self._project_point(end)
            
            line = ET.SubElement(group, "line")
            line.set("x1", str(start_2d[0]))
            line.set("y1", str(start_2d[1]))
            line.set("x2", str(end_2d[0]))
            line.set("y2", str(end_2d[1]))
            
            for key, value in attributes.items():
                line.set(key, str(value))
                
        return group
