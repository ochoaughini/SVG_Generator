"""
Layer management for handling complex SVG compositions.
"""
from typing import Dict, List, Optional, Any
import xml.etree.ElementTree as ET


class LayerManager:
    """
    Manages layers within an SVG document.
    
    Handles the creation, organization, and z-index ordering of layers
    to enable complex compositions with proper stacking order.
    """
    
    def __init__(self):
        """Initialize a new layer manager."""
        self.layers: Dict[str, ET.Element] = {}
        self.z_indices: Dict[str, int] = {}
        
    def add_layer(self, layer_id: str, element: ET.Element, z_index: int = 0) -> None:
        """
        Add a layer to the manager.
        
        Args:
            layer_id: Unique identifier for the layer
            element: The SVG element representing the layer
            z_index: Stacking order value (higher values are rendered on top)
        """
        self.layers[layer_id] = element
        self.z_indices[layer_id] = z_index
        
    def get_layer(self, layer_id: str) -> Optional[ET.Element]:
        """
        Retrieve a layer by its ID.
        
        Args:
            layer_id: The layer's unique identifier
            
        Returns:
            The layer element if found, None otherwise
        """
        return self.layers.get(layer_id)
        
    def set_z_index(self, layer_id: str, z_index: int) -> bool:
        """
        Update the z-index of a layer.
        
        Args:
            layer_id: The layer's unique identifier
            z_index: New stacking order value
            
        Returns:
            True if successful, False if layer not found
        """
        if layer_id in self.z_indices:
            self.z_indices[layer_id] = z_index
            return True
        return False
        
    def get_ordered_layer_ids(self) -> List[str]:
        """
        Get layer IDs sorted by their z-index.
        
        Returns:
            List of layer IDs in ascending z-index order
        """
        return sorted(self.layers.keys(), key=lambda x: self.z_indices.get(x, 0))
        
    def sort_layers(self) -> None:
        """
        Sort layers according to their z-index values.
        This prepares the layers for proper rendering order.
        """
        # The actual reordering happens in the orchestrator
        pass
        
    def merge_layers(self, target_id: str, source_ids: List[str]) -> bool:
        """
        Merge multiple layers into a target layer.
        
        Args:
            target_id: ID of the target layer
            source_ids: List of source layer IDs to merge
            
        Returns:
            True if successful, False otherwise
        """
        target = self.get_layer(target_id)
        if target is None:
            return False
            
        success = True
        for source_id in source_ids:
            source = self.get_layer(source_id)
            if source is None:
                success = False
                continue
                
            # Move all children from source to target
            for child in list(source):
                source.remove(child)
                target.append(child)
                
            # Remove the source layer
            self.layers.pop(source_id, None)
            self.z_indices.pop(source_id, None)
            
        return success
        
    def clear(self) -> None:
        """Clear all layers from the manager."""
        self.layers.clear()
        self.z_indices.clear()
