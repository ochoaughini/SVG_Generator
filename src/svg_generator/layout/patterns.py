"""
String art pattern generation for SVG compositions.
"""
from typing import List, Tuple, Dict, Any
import math
import xml.etree.ElementTree as ET


class StringArtPatterns:
    """
    Generator for string art patterns in SVG.
    
    Creates aesthetic string art patterns using mathematical algorithms
    that are optimized for size and visual appeal in competitions.
    """
    
    @staticmethod
    def create_circle_pattern(cx: float, cy: float, radius: float, 
                             points: int, **attributes) -> ET.Element:
        """
        Create a string art pattern using evenly spaced points on a circle.
        
        Args:
            cx: x-coordinate of the center
            cy: y-coordinate of the center
            radius: Radius of the circle
            points: Number of points to distribute on the circle
            **attributes: Additional attributes for the path elements
            
        Returns:
            A group element containing the string art pattern
        """
        group = ET.Element("g")
        
        # Set default attributes
        if "stroke" not in attributes:
            attributes["stroke"] = "#000"
        if "stroke-width" not in attributes:
            attributes["stroke-width"] = "0.5"
            
        # Generate points on the circle
        circle_points = []
        for i in range(points):
            angle = 2 * math.pi * i / points
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            circle_points.append((x, y))
            
        # Create paths between points
        for i in range(points):
            for j in range(i + 1, points):
                path = ET.SubElement(group, "path")
                d = f"M {circle_points[i][0]},{circle_points[i][1]} L {circle_points[j][0]},{circle_points[j][1]}"
                path.set("d", d)
                
                for key, value in attributes.items():
                    path.set(key, str(value))
                    
        return group
        
    @staticmethod
    def create_spiral_pattern(cx: float, cy: float, start_radius: float,
                             end_radius: float, turns: float, points: int, 
                             **attributes) -> ET.Element:
        """
        Create a spiral string art pattern.
        
        Args:
            cx: x-coordinate of the center
            cy: y-coordinate of the center
            start_radius: Starting radius of the spiral
            end_radius: Ending radius of the spiral
            turns: Number of turns in the spiral
            points: Number of points to use along the spiral
            **attributes: Additional attributes for the path elements
            
        Returns:
            A group element containing the spiral pattern
        """
        group = ET.Element("g")
        
        # Set default attributes
        if "stroke" not in attributes:
            attributes["stroke"] = "#000"
        if "stroke-width" not in attributes:
            attributes["stroke-width"] = "0.5"
            
        # Generate points on the spiral
        spiral_points = []
        for i in range(points):
            t = i / (points - 1)  # Parameter from 0 to 1
            radius = start_radius + t * (end_radius - start_radius)
            angle = 2 * math.pi * turns * t
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            spiral_points.append((x, y))
            
        # Create a single path for the spiral
        spiral_path = ET.SubElement(group, "path")
        d = f"M {spiral_points[0][0]},{spiral_points[0][1]}"
        for point in spiral_points[1:]:
            d += f" L {point[0]},{point[1]}"
            
        spiral_path.set("d", d)
        for key, value in attributes.items():
            spiral_path.set(key, str(value))
            
        return group
        
    @staticmethod
    def create_lissajous_pattern(cx: float, cy: float, a: float, b: float,
                              a_freq: float, b_freq: float, phase: float,
                              points: int, **attributes) -> ET.Element:
        """
        Create a Lissajous curve pattern.
        
        Args:
            cx: x-coordinate of the center
            cy: y-coordinate of the center
            a: Amplitude in x direction
            b: Amplitude in y direction
            a_freq: Frequency in x direction
            b_freq: Frequency in y direction
            phase: Phase difference
            points: Number of points to use
            **attributes: Additional attributes for the path
            
        Returns:
            A path element containing the Lissajous curve
        """
        path = ET.Element("path")
        
        # Set default attributes
        if "stroke" not in attributes:
            attributes["stroke"] = "#000"
        if "stroke-width" not in attributes:
            attributes["stroke-width"] = "0.5"
        if "fill" not in attributes:
            attributes["fill"] = "none"
            
        # Generate points on the Lissajous curve
        lissajous_points = []
        for i in range(points):
            t = 2 * math.pi * i / points
            x = cx + a * math.sin(a_freq * t + phase)
            y = cy + b * math.sin(b_freq * t)
            lissajous_points.append((x, y))
            
        # Create path
        d = f"M {lissajous_points[0][0]},{lissajous_points[0][1]}"
        for point in lissajous_points[1:]:
            d += f" L {point[0]},{point[1]}"
        d += " Z"  # Close the path
        
        path.set("d", d)
        for key, value in attributes.items():
            path.set(key, str(value))
            
        return path
