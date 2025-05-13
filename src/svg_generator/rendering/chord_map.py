"""
Chord map rendering for complex relationship visualization.
"""
from typing import List, Dict, Tuple, Any, Optional
import math
import xml.etree.ElementTree as ET


class ChordMapRenderer:
    """
    Renders chord maps for visualizing relationships between entities.
    
    Implements algorithms for creating aesthetically pleasing chord diagrams
    that efficiently represent complex relationships for competitions.
    """
    
    def __init__(self, width: float = 800, height: float = 600):
        """
        Initialize the chord map renderer.
        
        Args:
            width: Width of the SVG canvas
            height: Height of the SVG canvas
        """
        self.width = width
        self.height = height
        
    def generate_chord_diagram(self, data: List[Dict[str, Any]], radius: float = None,
                              **attributes) -> ET.Element:
        """
        Generate a chord diagram based on relationship data.
        
        Args:
            data: List of dictionaries with 'source', 'target', and 'value' keys
            radius: Radius of the chord diagram, defaults to 40% of min(width, height)
            **attributes: Additional attributes for the chord elements
            
        Returns:
            A group element containing the chord diagram
        """
        group = ET.Element("g")
        
        # Calculate center and radius
        cx = self.width / 2
        cy = self.height / 2
        if radius is None:
            radius = min(self.width, self.height) * 0.4
            
        # Set default attributes
        if "stroke" not in attributes:
            attributes["stroke"] = "#333"
        if "stroke-width" not in attributes:
            attributes["stroke-width"] = "1"
            
        # Extract unique entities and assign them positions around the circle
        entities = set()
        for item in data:
            entities.add(item["source"])
            entities.add(item["target"])
            
        entity_list = sorted(list(entities))
        entity_positions = {}
        
        for i, entity in enumerate(entity_list):
            angle = 2 * math.pi * i / len(entity_list)
            entity_positions[entity] = {
                "angle": angle,
                "x": cx + radius * math.cos(angle),
                "y": cy + radius * math.sin(angle)
            }
            
        # Draw entity markers
        for entity, pos in entity_positions.items():
            # Draw circle for entity
            circle = ET.SubElement(group, "circle")
            circle.set("cx", str(pos["x"]))
            circle.set("cy", str(pos["y"]))
            circle.set("r", "5")
            circle.set("fill", attributes.get("entity_fill", "#666"))
            
            # Draw entity label
            text = ET.SubElement(group, "text")
            text.set("x", str(cx + (radius + 15) * math.cos(pos["angle"])))
            text.set("y", str(cy + (radius + 15) * math.sin(pos["angle"])))
            text.set("text-anchor", "middle")
            text.set("dominant-baseline", "middle")
            text.set("font-size", attributes.get("font_size", "12"))
            text.set("fill", attributes.get("text_fill", "#000"))
            
            # Adjust text rotation for readability
            if pos["angle"] > math.pi/2 and pos["angle"] < 3*math.pi/2:
                text.set("transform", f"rotate({180 + pos['angle']*180/math.pi}, {cx + (radius + 15) * math.cos(pos['angle'])}, {cy + (radius + 15) * math.sin(pos['angle'])})")
            else:
                text.set("transform", f"rotate({pos['angle']*180/math.pi}, {cx + (radius + 15) * math.cos(pos['angle'])}, {cy + (radius + 15) * math.sin(pos['angle'])})")
                
            text.text = entity
            
        # Draw the chords
        for item in data:
            source_pos = entity_positions[item["source"]]
            target_pos = entity_positions[item["target"]]
            value = item.get("value", 1)
            
            # Scale value to determine chord width
            max_width = 10
            width = max(1, min(max_width, value))
            
            # Create a Bezier curve representing the chord
            path = ET.SubElement(group, "path")
            
            # Control points for the curve (toward the center)
            cp1x = cx + (source_pos["x"] - cx) * 0.5
            cp1y = cy + (source_pos["y"] - cy) * 0.5
            cp2x = cx + (target_pos["x"] - cx) * 0.5
            cp2y = cy + (target_pos["y"] - cy) * 0.5
            
            # Create the path
            d = f"M {source_pos['x']},{source_pos['y']} "
            d += f"C {cp1x},{cp1y} {cp2x},{cp2y} {target_pos['x']},{target_pos['y']}"
            
            path.set("d", d)
            path.set("fill", "none")
            
            # Apply additional attributes
            for key, value in attributes.items():
                if key not in ["entity_fill", "text_fill", "font_size"]:
                    path.set(key, str(value))
                    
            # Set chord-specific attributes
            path.set("stroke-width", str(width))
            
            # Add opacity based on value
            opacity = 0.3 + (0.7 * min(1, value / 10))
            path.set("opacity", str(opacity))
            
        return group
        
    def generate_matrix_chord(self, matrix: List[List[float]], 
                            labels: List[str] = None, 
                            radius: float = None,
                            **attributes) -> ET.Element:
        """
        Generate a chord diagram from a matrix of relationships.
        
        Args:
            matrix: Square matrix where [i][j] represents relationship from i to j
            labels: Optional list of labels for entities
            radius: Radius of the chord diagram, defaults to 40% of min(width, height)
            **attributes: Additional attributes for the chord elements
            
        Returns:
            A group element containing the chord diagram
        """
        group = ET.Element("g")
        
        # Calculate center and radius
        cx = self.width / 2
        cy = self.height / 2
        if radius is None:
            radius = min(self.width, self.height) * 0.4
            
        # Set default attributes
        if "stroke" not in attributes:
            attributes["stroke"] = "#333"
        if "stroke-width" not in attributes:
            attributes["stroke-width"] = "1"
            
        # Ensure matrix is square
        n = len(matrix)
        if not all(len(row) == n for row in matrix):
            raise ValueError("Matrix must be square")
            
        # Create default labels if not provided
        if labels is None:
            labels = [f"Entity {i+1}" for i in range(n)]
        elif len(labels) != n:
            raise ValueError("Number of labels must match matrix dimensions")
            
        # Calculate entity positions
        entity_positions = []
        for i in range(n):
            angle = 2 * math.pi * i / n
            entity_positions.append({
                "angle": angle,
                "x": cx + radius * math.cos(angle),
                "y": cy + radius * math.sin(angle)
            })
            
        # Draw entity markers and labels
        for i, pos in enumerate(entity_positions):
            # Draw arc segment for entity
            arc_width = 2 * math.pi / n
            arc_path = ET.SubElement(group, "path")
            
            # Draw arc
            start_angle = pos["angle"] - arc_width/2
            end_angle = pos["angle"] + arc_width/2
            
            # Create arc path
            large_arc_flag = 0 if arc_width <= math.pi else 1
            
            start_x = cx + radius * math.cos(start_angle)
            start_y = cy + radius * math.sin(start_angle)
            end_x = cx + radius * math.cos(end_angle)
            end_y = cy + radius * math.sin(end_angle)
            
            d = f"M {cx},{cy} "
            d += f"L {start_x},{start_y} "
            d += f"A {radius},{radius} 0 {large_arc_flag},1 {end_x},{end_y} "
            d += f"Z"
            
            arc_path.set("d", d)
            arc_path.set("fill", attributes.get(f"entity_fill_{i}", attributes.get("entity_fill", "#ccc")))
            arc_path.set("stroke", "none")
            
            # Draw label
            text = ET.SubElement(group, "text")
            text.set("x", str(cx + (radius + 20) * math.cos(pos["angle"])))
            text.set("y", str(cy + (radius + 20) * math.sin(pos["angle"])))
            text.set("text-anchor", "middle")
            text.set("dominant-baseline", "middle")
            text.set("font-size", attributes.get("font_size", "12"))
            text.set("fill", attributes.get("text_fill", "#000"))
            
            # Adjust text rotation for readability
            if pos["angle"] > math.pi/2 and pos["angle"] < 3*math.pi/2:
                text.set("transform", f"rotate({180 + pos['angle']*180/math.pi}, {cx + (radius + 20) * math.cos(pos['angle'])}, {cy + (radius + 20) * math.sin(pos['angle'])})")
            else:
                text.set("transform", f"rotate({pos['angle']*180/math.pi}, {cx + (radius + 20) * math.cos(pos['angle'])}, {cy + (radius + 20) * math.sin(pos['angle'])})")
                
            text.text = labels[i]
            
        # Draw chords
        for i in range(n):
            for j in range(i+1, n):  # Only draw connections once (i->j)
                value_ij = matrix[i][j]
                value_ji = matrix[j][i]
                
                # Skip if no relationship exists
                if value_ij <= 0 and value_ji <= 0:
                    continue
                    
                # Draw chord based on combined values
                combined_value = value_ij + value_ji
                
                # Scale value to determine chord width
                max_width = 10
                width = max(1, min(max_width, combined_value))
                
                source_pos = entity_positions[i]
                target_pos = entity_positions[j]
                
                # Create a Bezier curve for the chord
                path = ET.SubElement(group, "path")
                
                # Control points for the curve
                cp1x = cx + (source_pos["x"] - cx) * 0.5
                cp1y = cy + (source_pos["y"] - cy) * 0.5
                cp2x = cx + (target_pos["x"] - cx) * 0.5
                cp2y = cy + (target_pos["y"] - cy) * 0.5
                
                # Create the path
                d = f"M {source_pos['x']},{source_pos['y']} "
                d += f"C {cp1x},{cp1y} {cp2x},{cp2y} {target_pos['x']},{target_pos['y']}"
                
                path.set("d", d)
                path.set("fill", "none")
                
                # Apply additional attributes
                for key, value in attributes.items():
                    if key not in ["entity_fill", "text_fill", "font_size"] and not key.startswith("entity_fill_"):
                        path.set(key, str(value))
                        
                # Set chord-specific attributes
                path.set("stroke-width", str(width))
                
                # Set color based on direction
                if value_ij > value_ji:
                    path.set("stroke", attributes.get("forward_color", "#3366cc"))
                elif value_ji > value_ij:
                    path.set("stroke", attributes.get("backward_color", "#cc3366"))
                else:
                    path.set("stroke", attributes.get("equal_color", "#666666"))
                    
                # Add opacity based on value
                opacity = 0.3 + (0.7 * min(1, combined_value / 10))
                path.set("opacity", str(opacity))
                
        return group
