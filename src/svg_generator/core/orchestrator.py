"""
Scene orchestration for SVG generation with layering and composition.
"""
from typing import List, Dict, Any, Optional
import xml.etree.ElementTree as ET
from svg_generator.core.generator import ConstrainedGenerator
from svg_generator.layout.managers import LayerManager


class SceneOrchestrator:
    """
    Coordinates multiple layers and elements to create complex SVG scenes.
    Manages the overall composition, layering, and styling of SVG elements.
    """
    
    def __init__(self, width: int = 800, height: int = 600, 
                 max_size_kb: int = 10, max_elements: int = 1000):
        """
        Initialize the scene orchestrator.
        
        Args:
            width: Width of the SVG viewport
            height: Height of the SVG viewport
            max_size_kb: Maximum size of the generated SVG in kilobytes
            max_elements: Maximum number of elements allowed in the SVG
        """
        self.width = width
        self.height = height
        self.generator = ConstrainedGenerator(max_size_kb, max_elements)
        self.layer_manager = LayerManager()
        self.setup_document()
        
    def setup_document(self):
        """Configure the initial SVG document properties."""
        self.generator.root.set("width", str(self.width))
        self.generator.root.set("height", str(self.height))
        self.generator.root.set("viewBox", f"0 0 {self.width} {self.height}")
        
    def create_layer(self, layer_id: str, z_index: int = 0) -> str:
        """
        Create a new layer in the SVG document.
        
        Args:
            layer_id: Unique identifier for the layer
            z_index: Stacking order of the layer (higher values are on top)
            
        Returns:
            The layer ID that was created
        """
        layer = self.generator.add_element("g", {"id": layer_id, "data-z-index": z_index})
        if layer is not None:
            self.layer_manager.add_layer(layer_id, layer, z_index)
        return layer_id
        
    def add_to_layer(self, layer_id: str, element_type: str, 
                     attributes: Dict[str, Any]) -> Optional[ET.Element]:
        """
        Add an element to a specific layer.
        
        Args:
            layer_id: ID of the layer to add the element to
            element_type: The type of SVG element to create
            attributes: Dictionary of attributes for the element
            
        Returns:
            The created element if successful, None otherwise
        """
        layer = self.layer_manager.get_layer(layer_id)
        if layer is None:
            return None
            
        element = ET.SubElement(layer, element_type)
        for key, value in attributes.items():
            element.set(key, str(value))
            
        self.generator.element_count += 1
        return element
        
    def arrange_layers(self):
        """
        Rearrange layers according to their z-index.
        This ensures proper stacking order in the final SVG.
        """
        self.layer_manager.sort_layers()
        # Reorder layers in the SVG DOM
        for layer_id in self.layer_manager.get_ordered_layer_ids():
            layer = self.layer_manager.get_layer(layer_id)
            if layer is not None:
                # Remove and re-add to place at the end (top)
                self.generator.root.remove(layer)
                self.generator.root.append(layer)
                
    def generate_svg(self) -> str:
        """
        Generate the final SVG with all layers properly arranged.
        
        Returns:
            The XML string representation of the SVG
        """
        self.arrange_layers()
        return self.generator.to_string()
        
    def validate(self) -> bool:
        """
        Validate if the current scene meets all constraints.
        
        Returns:
            True if all constraints are met, False otherwise
        """
        return (self.generator.validate_size() and 
                self.generator.element_count <= self.generator.max_elements)
