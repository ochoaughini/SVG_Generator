"""
Core generator logic for SVG creation with constraints.
"""
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, List


class ConstrainedGenerator:
    """
    Generator for SVG elements with customizable constraints.
    This class handles the creation of SVG elements while ensuring they meet specific
    size, complexity, and style requirements for competition submissions.
    """
    
    def __init__(self, max_size_kb: int = 10, max_elements: int = 1000):
        """
        Initialize the constrained generator.
        
        Args:
            max_size_kb: Maximum size of the generated SVG in kilobytes
            max_elements: Maximum number of elements allowed in the SVG
        """
        self.max_size_kb = max_size_kb
        self.max_elements = max_elements
        self.root = ET.Element("svg")
        self.root.set("xmlns", "http://www.w3.org/2000/svg")
        self.element_count = 0
        
    def add_element(self, element_type: str, attributes: Dict[str, Any]) -> Optional[ET.Element]:
        """
        Add an element to the SVG document with validation.
        
        Args:
            element_type: The type of SVG element to create (e.g., 'circle', 'rect')
            attributes: Dictionary of attributes to apply to the element
            
        Returns:
            The created element if successful, None if constraints were violated
        """
        if self.element_count >= self.max_elements:
            return None
            
        element = ET.SubElement(self.root, element_type)
        for key, value in attributes.items():
            element.set(key, str(value))
            
        self.element_count += 1
        return element
        
    def add_elements(self, elements: List[Dict[str, Any]]) -> int:
        """
        Add multiple elements to the SVG at once.
        
        Args:
            elements: List of dictionaries with 'type' and 'attributes' keys
            
        Returns:
            Number of elements successfully added
        """
        added = 0
        for element_data in elements:
            element = self.add_element(
                element_data["type"], 
                element_data.get("attributes", {})
            )
            if element is not None:
                added += 1
        return added
        
    def to_string(self) -> str:
        """
        Convert the SVG document to a string representation.
        
        Returns:
            The XML string representation of the SVG
        """
        return ET.tostring(self.root, encoding='unicode')
        
    def validate_size(self) -> bool:
        """
        Check if the current SVG meets size constraints.
        
        Returns:
            True if size constraints are met, False otherwise
        """
        svg_str = self.to_string()
        size_kb = len(svg_str.encode('utf-8')) / 1024
        return size_kb <= self.max_size_kb
