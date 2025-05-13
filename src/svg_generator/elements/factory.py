"""
Factory for SVG element creation with customization options.
"""
from typing import Dict, Any, Optional
import xml.etree.ElementTree as ET


class ElementFactory:
    """
    Factory for creating SVG elements with optimized attributes.
    Provides a standardized way to create different SVG elements.
    """
    
    @staticmethod
    def create(element_type: str, **attributes) -> str:
        """
        Create an SVG element as a string.
        
        Args:
            element_type: The type of SVG element to create (e.g., 'circle', 'rect')
            **attributes: Key-value pairs of attributes for the element
            
        Returns:
            String representation of the SVG element
        """
        element = ET.Element(element_type)
        for key, value in attributes.items():
            element.set(key, str(value))
        return ET.tostring(element, encoding='unicode')
        
    @staticmethod
    def create_circle(cx: float, cy: float, radius: float, **attributes) -> str:
        """
        Create a circle SVG element.
        
        Args:
            cx: x-coordinate of the center
            cy: y-coordinate of the center
            radius: Radius of the circle
            **attributes: Additional attributes for the circle
            
        Returns:
            String representation of the circle element
        """
        attributes.update({"cx": cx, "cy": cy, "r": radius})
        return ElementFactory.create("circle", **attributes)
        
    @staticmethod
    def create_rectangle(x: float, y: float, width: float, height: float, **attributes) -> str:
        """
        Create a rectangle SVG element.
        
        Args:
            x: x-coordinate of the top-left corner
            y: y-coordinate of the top-left corner
            width: Width of the rectangle
            height: Height of the rectangle
            **attributes: Additional attributes for the rectangle
            
        Returns:
            String representation of the rectangle element
        """
        attributes.update({"x": x, "y": y, "width": width, "height": height})
        return ElementFactory.create("rect", **attributes)
        
    @staticmethod
    def create_line(x1: float, y1: float, x2: float, y2: float, **attributes) -> str:
        """
        Create a line SVG element.
        
        Args:
            x1: x-coordinate of the start point
            y1: y-coordinate of the start point
            x2: x-coordinate of the end point
            y2: y-coordinate of the end point
            **attributes: Additional attributes for the line
            
        Returns:
            String representation of the line element
        """
        attributes.update({"x1": x1, "y1": y1, "x2": x2, "y2": y2})
        return ElementFactory.create("line", **attributes)
        
    @staticmethod
    def create_path(d: str, **attributes) -> str:
        """
        Create a path SVG element.
        
        Args:
            d: Path data string
            **attributes: Additional attributes for the path
            
        Returns:
            String representation of the path element
        """
        attributes.update({"d": d})
        return ElementFactory.create("path", **attributes)
        
    @staticmethod
    def create_text(x: float, y: float, text: str, **attributes) -> str:
        """
        Create a text SVG element.
        
        Args:
            x: x-coordinate of the text
            y: y-coordinate of the text
            text: The text content
            **attributes: Additional attributes for the text element
            
        Returns:
            String representation of the text element
        """
        attributes.update({"x": x, "y": y})
        element = ET.Element("text")
        for key, value in attributes.items():
            element.set(key, str(value))
        element.text = text
        return ET.tostring(element, encoding='unicode')
