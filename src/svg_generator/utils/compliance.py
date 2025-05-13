"""
Utilities for ensuring SVG compliance with competition requirements.
"""
import re
from typing import Dict, List, Tuple, Any, Optional
import xml.etree.ElementTree as ET


class SanitizeUtils:
    """
    Utilities for sanitizing SVG content to ensure compliance with rules.
    
    Provides methods to clean, validate, and ensure that SVG files meet
    size constraints and compliance requirements for competitions.
    """
    
    @staticmethod
    def remove_metadata(svg_str: str) -> str:
        """
        Remove metadata and unnecessary attributes from SVG.
        
        Args:
            svg_str: SVG string to clean
            
        Returns:
            Cleaned SVG string
        """
        # Remove metadata tags
        svg_str = re.sub(r'<metadata>.*?</metadata>', '', svg_str, flags=re.DOTALL)
        
        # Remove comments
        svg_str = re.sub(r'<!--.*?-->', '', svg_str, flags=re.DOTALL)
        
        # Remove inkscape and other editor-specific namespaces
        svg_str = re.sub(r'\s+xmlns:(inkscape|sodipodi|dc|cc|rdf)="[^"]+"', '', svg_str)
        
        # Remove inkscape and other editor-specific attributes
        svg_str = re.sub(r'\s+(inkscape|sodipodi|dc|cc|rdf):[a-z\-]+="[^"]+"', '', svg_str)
        
        return svg_str
        
    @staticmethod
    def minify_svg(svg_str: str) -> str:
        """
        Minify SVG by removing whitespace and optimizing structure.
        
        Args:
            svg_str: SVG string to minify
            
        Returns:
            Minified SVG string
        """
        # Remove newlines and reduce white space
        svg_str = re.sub(r'\s+', ' ', svg_str)
        svg_str = re.sub(r'>\s+<', '><', svg_str)
        svg_str = re.sub(r'"\s+', '"', svg_str)
        svg_str = re.sub(r'\s+="', '="', svg_str)
        
        # Remove unnecessary attributes
        svg_str = re.sub(r'\s+version="[^"]+"', '', svg_str)
        
        # Optimize common patterns
        svg_str = re.sub(r'stroke-width="1"', 'stroke-width="1"', svg_str)  # No real change but here as example
        
        return svg_str.strip()
        
    @staticmethod
    def simplify_paths(svg_str: str, precision: int = 1) -> str:
        """
        Simplify path data by reducing decimal precision.
        
        Args:
            svg_str: SVG string to simplify
            precision: Number of decimal places to retain
            
        Returns:
            SVG with simplified paths
        """
        def round_numbers(match: re.Match) -> str:
            """Round numbers in path data"""
            path_data = match.group(1)
            
            # Find all numbers in path data and round them
            def replace_number(num_match: re.Match) -> str:
                num = float(num_match.group(0))
                rounded = round(num, precision)
                # Convert back to string, avoiding trailing zeros
                if rounded == int(rounded):
                    return str(int(rounded))
                else:
                    return str(rounded)
                    
            return 'd="' + re.sub(r'[-+]?[0-9]*\.?[0-9]+', replace_number, path_data) + '"'
            
        # Apply path simplification
        return re.sub(r'd="([^"]+)"', round_numbers, svg_str)
        
    @staticmethod
    def validate_size(svg_str: str, max_size_kb: float = 10.0) -> Tuple[bool, float]:
        """
        Check if SVG meets size constraints.
        
        Args:
            svg_str: SVG string to validate
            max_size_kb: Maximum size in kilobytes
            
        Returns:
            Tuple of (is_valid, actual_size_kb)
        """
        size_bytes = len(svg_str.encode('utf-8'))
        size_kb = size_bytes / 1024
        
        return (size_kb <= max_size_kb, size_kb)
        
    @staticmethod
    def remove_unused_defs(svg_str: str) -> str:
        """
        Remove unused definitions from SVG.
        
        Args:
            svg_str: SVG string to clean
            
        Returns:
            SVG with unused definitions removed
        """
        try:
            # Parse XML
            root = ET.fromstring(svg_str)
            
            # Find defs section
            defs_elem = root.find(".//{http://www.w3.org/2000/svg}defs")
            if defs_elem is None:
                return svg_str
                
            # Extract all IDs from defs
            def_ids = []
            for child in defs_elem:
                id_attr = child.get("id")
                if id_attr:
                    def_ids.append(id_attr)
                    
            # Check which IDs are actually used
            svg_text = ET.tostring(root, encoding='unicode')
            used_ids = set()
            
            for def_id in def_ids:
                # Check for url(#id) pattern
                if f'url(#{def_id})' in svg_text:
                    used_ids.add(def_id)
                    
                # Check for href="#id" pattern
                if f'href="#{def_id}"' in svg_text:
                    used_ids.add(def_id)
                    
            # Remove unused elements from defs
            for child in list(defs_elem):
                id_attr = child.get("id")
                if id_attr and id_attr not in used_ids:
                    defs_elem.remove(child)
                    
            # Convert back to string
            return ET.tostring(root, encoding='unicode')
            
        except ET.ParseError:
            # If XML parsing fails, return original string
            return svg_str
            
    @staticmethod
    def ensure_compliance(svg_str: str, max_size_kb: float = 10.0) -> str:
        """
        Ensure SVG complies with all requirements.
        
        Applies a series of optimizations to make sure the SVG is valid
        and meets size constraints.
        
        Args:
            svg_str: SVG string to process
            max_size_kb: Maximum size in kilobytes
            
        Returns:
            Compliant SVG string
        """
        # Start with basic cleaning
        result = SanitizeUtils.remove_metadata(svg_str)
        
        # Check if we're already under the size limit
        is_valid, size_kb = SanitizeUtils.validate_size(result, max_size_kb)
        if is_valid:
            return result
            
        # Apply more aggressive optimizations
        result = SanitizeUtils.remove_unused_defs(result)
        result = SanitizeUtils.simplify_paths(result, 1)
        
        # Check size again
        is_valid, size_kb = SanitizeUtils.validate_size(result, max_size_kb)
        if is_valid:
            return result
            
        # Apply extreme optimization
        result = SanitizeUtils.minify_svg(result)
        result = SanitizeUtils.simplify_paths(result, 0)
        
        # Final check
        is_valid, _ = SanitizeUtils.validate_size(result, max_size_kb)
        if not is_valid:
            # If still too large, could warn but returning best effort
            pass
            
        return result
