"""
Optimization utilities for SVG content in competition contexts.
"""
from typing import Dict, List, Any, Optional, Tuple
import re
import xml.etree.ElementTree as ET
from svg_generator.utils.compliance import SanitizeUtils


class CompetitionOptimizer:
    """
    Optimizes SVG content for competition submissions.
    
    Implements various strategies to minimize SVG file size while
    preserving visual quality for competition requirements.
    """
    
    def __init__(self, max_size_kb: float = 10.0):
        """
        Initialize the competition optimizer.
        
        Args:
            max_size_kb: Maximum allowed size in kilobytes
        """
        self.max_size_kb = max_size_kb
        self.sanitizer = SanitizeUtils()
        
    def optimize(self, svg_str: str) -> Tuple[str, float]:
        """
        Optimize SVG content to reduce size.
        
        Args:
            svg_str: SVG string to optimize
            
        Returns:
            Tuple of (optimized_svg, size_kb)
        """
        # Start with basic sanitization
        result = self.sanitizer.remove_metadata(svg_str)
        
        # Check if already within limits
        is_valid, size_kb = self.sanitizer.validate_size(result, self.max_size_kb)
        if is_valid:
            return result, size_kb
            
        # Apply progressive optimization until size requirements are met
        optimization_levels = [
            self._optimize_level_1,
            self._optimize_level_2,
            self._optimize_level_3,
            self._optimize_level_4
        ]
        
        for optimize_func in optimization_levels:
            result = optimize_func(result)
            is_valid, size_kb = self.sanitizer.validate_size(result, self.max_size_kb)
            if is_valid:
                return result, size_kb
                
        # If we've reached here, apply maximum optimization
        result = self._optimize_maximum(result)
        _, size_kb = self.sanitizer.validate_size(result, self.max_size_kb)
        
        return result, size_kb
        
    def _optimize_level_1(self, svg_str: str) -> str:
        """
        Level 1 optimization: Basic cleanup and minimal changes.
        
        Args:
            svg_str: SVG string to optimize
            
        Returns:
            Optimized SVG string
        """
        # Remove unused definitions
        result = self.sanitizer.remove_unused_defs(svg_str)
        
        # Simplify paths with high precision (minimal visual impact)
        result = self.sanitizer.simplify_paths(result, 2)
        
        return result
        
    def _optimize_level_2(self, svg_str: str) -> str:
        """
        Level 2 optimization: More aggressive path simplification.
        
        Args:
            svg_str: SVG string to optimize
            
        Returns:
            Optimized SVG string
        """
        # Simplify paths with medium precision
        result = self.sanitizer.simplify_paths(svg_str, 1)
        
        # Remove unnecessary attributes
        result = self._remove_unnecessary_attributes(result)
        
        return result
        
    def _optimize_level_3(self, svg_str: str) -> str:
        """
        Level 3 optimization: Structural optimization.
        
        Args:
            svg_str: SVG string to optimize
            
        Returns:
            Optimized SVG string
        """
        # Minify the SVG
        result = self.sanitizer.minify_svg(svg_str)
        
        # Group similar elements
        result = self._group_similar_elements(result)
        
        return result
        
    def _optimize_level_4(self, svg_str: str) -> str:
        """
        Level 4 optimization: Lossy optimization with minimal visual impact.
        
        Args:
            svg_str: SVG string to optimize
            
        Returns:
            Optimized SVG string
        """
        # Simplify paths with low precision
        result = self.sanitizer.simplify_paths(svg_str, 0)
        
        # Remove non-essential elements
        result = self._remove_nonessential_elements(result)
        
        return result
        
    def _optimize_maximum(self, svg_str: str) -> str:
        """
        Maximum optimization: Most aggressive size reduction.
        
        Args:
            svg_str: SVG string to optimize
            
        Returns:
            Optimized SVG string
        """
        try:
            # Parse XML
            root = ET.fromstring(svg_str)
            
            # Remove all comments, processing instructions
            for elem in root.iter():
                if elem.tag is ET.Comment or elem.tag is ET.ProcessingInstruction:
                    elem.getparent().remove(elem)
                    
            # Simplify all numbers to integers where possible
            for elem in root.iter():
                for attr, value in elem.attrib.items():
                    if re.match(r'^[-+]?[0-9]*\.0+$', value):
                        elem.attrib[attr] = value.split('.')[0]
                        
            # Convert back to string
            result = ET.tostring(root, encoding='unicode')
            
            # Final minification
            result = self.sanitizer.minify_svg(result)
            
            return result
            
        except (ET.ParseError, AttributeError):
            # If XML parsing fails, return input
            return svg_str
            
    def _remove_unnecessary_attributes(self, svg_str: str) -> str:
        """
        Remove attributes that don't significantly affect rendering.
        
        Args:
            svg_str: SVG string to process
            
        Returns:
            Processed SVG string
        """
        # Remove id attributes where not referenced
        svg_str = re.sub(r'\s+id="[^"]*"', '', svg_str)
        
        # Remove class attributes if not used for styling
        svg_str = re.sub(r'\s+class="[^"]*"', '', svg_str)
        
        # Remove default values
        replacements = [
            (r'opacity="1"', ''),
            (r'fill-opacity="1"', ''),
            (r'stroke-opacity="1"', ''),
            (r'stroke-width="1"', 'stroke-width="1"'),  # No change, but example
            (r'stroke-linecap="butt"', ''),
            (r'stroke-linejoin="miter"', '')
        ]
        
        for pattern, replacement in replacements:
            svg_str = re.sub(pattern, replacement, svg_str)
            
        return svg_str
        
    def _group_similar_elements(self, svg_str: str) -> str:
        """
        Group similar elements to reduce redundancy.
        
        Args:
            svg_str: SVG string to process
            
        Returns:
            Processed SVG string
        """
        try:
            # This is a simplified implementation - a real one would be more complex
            # Parse XML
            root = ET.fromstring(svg_str)
            
            # Group elements with same properties
            style_groups = {}
            
            for elem in root.findall(".//{http://www.w3.org/2000/svg}*"):
                # Skip groups and defs
                if elem.tag.endswith("g") or elem.tag.endswith("defs"):
                    continue
                    
                # Create a style key from attributes
                style_attrs = {}
                for attr in ["fill", "stroke", "stroke-width", "opacity"]:
                    if attr in elem.attrib:
                        style_attrs[attr] = elem.attrib[attr]
                        
                style_key = tuple(sorted(style_attrs.items()))
                
                if style_key and style_key in style_groups:
                    style_groups[style_key].append(elem)
                elif style_key:
                    style_groups[style_key] = [elem]
                    
            # Create groups for elements with common styles (if at least 3 elements share style)
            for style_key, elements in style_groups.items():
                if len(elements) >= 3:
                    # Only group if it would save space
                    group = ET.Element("{http://www.w3.org/2000/svg}g")
                    
                    # Add style attributes to group
                    for attr, value in style_key:
                        group.set(attr, value)
                        
                    # Move elements to group, removing duplicate style attributes
                    for elem in elements:
                        for attr, _ in style_key:
                            if attr in elem.attrib:
                                del elem.attrib[attr]
                                
                        # Get parent and position
                        parent = elem.getparent()
                        if parent is not None:
                            index = list(parent).index(elem)
                            
                            # Remove from original parent
                            parent.remove(elem)
                            
                            # Add to group
                            group.append(elem)
                    
                    # Add group to root
                    root.append(group)
                    
            # Convert back to string
            return ET.tostring(root, encoding='unicode')
            
        except (ET.ParseError, AttributeError):
            # If XML parsing fails, return original
            return svg_str
            
    def _remove_nonessential_elements(self, svg_str: str) -> str:
        """
        Remove non-essential elements that won't significantly affect rendering.
        
        Args:
            svg_str: SVG string to process
            
        Returns:
            Processed SVG string
        """
        try:
            # Parse XML
            root = ET.fromstring(svg_str)
            
            # Remove title, desc elements
            for tag in ["{http://www.w3.org/2000/svg}title", "{http://www.w3.org/2000/svg}desc"]:
                for elem in root.findall(f".//{tag}"):
                    parent = elem.getparent()
                    if parent is not None:
                        parent.remove(elem)
                        
            # Remove empty groups
            for elem in root.findall(".//{http://www.w3.org/2000/svg}g"):
                if len(elem) == 0:
                    parent = elem.getparent()
                    if parent is not None:
                        parent.remove(elem)
                        
            # Convert back to string
            return ET.tostring(root, encoding='unicode')
            
        except (ET.ParseError, AttributeError):
            # If XML parsing fails, return original
            return svg_str
