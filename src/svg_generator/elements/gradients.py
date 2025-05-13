"""
Gradient library for enhanced SVG visual effects.
"""
from typing import List, Dict, Any, Tuple
import xml.etree.ElementTree as ET


class GradientLibrary:
    """
    Library of gradient definitions for SVG elements.
    Provides methods to create linear and radial gradients with customizable stops.
    """
    
    @staticmethod
    def create_linear_gradient(id: str, x1: float = 0, y1: float = 0,
                              x2: float = 1, y2: float = 0,
                              stops: List[Dict[str, Any]] = None) -> ET.Element:
        """
        Create a linear gradient element.
        
        Args:
            id: Unique identifier for the gradient
            x1: x-coordinate of the start point (0-1)
            y1: y-coordinate of the start point (0-1)
            x2: x-coordinate of the end point (0-1)
            y2: y-coordinate of the end point (0-1)
            stops: List of dictionaries with 'offset', 'color', and optional 'opacity'
            
        Returns:
            The linear gradient element
        """
        gradient = ET.Element("linearGradient")
        gradient.set("id", id)
        gradient.set("x1", str(x1))
        gradient.set("y1", str(y1))
        gradient.set("x2", str(x2))
        gradient.set("y2", str(y2))
        
        if stops:
            for stop in stops:
                stop_el = ET.SubElement(gradient, "stop")
                stop_el.set("offset", str(stop.get("offset", 0)))
                stop_el.set("stop-color", stop.get("color", "#000"))
                if "opacity" in stop:
                    stop_el.set("stop-opacity", str(stop["opacity"]))
                    
        return gradient
        
    @staticmethod
    def create_radial_gradient(id: str, cx: float = 0.5, cy: float = 0.5,
                              r: float = 0.5, fx: float = None, fy: float = None,
                              stops: List[Dict[str, Any]] = None) -> ET.Element:
        """
        Create a radial gradient element.
        
        Args:
            id: Unique identifier for the gradient
            cx: x-coordinate of the center (0-1)
            cy: y-coordinate of the center (0-1)
            r: Radius of the gradient (0-1)
            fx: x-coordinate of the focal point (0-1), defaults to cx if None
            fy: y-coordinate of the focal point (0-1), defaults to cy if None
            stops: List of dictionaries with 'offset', 'color', and optional 'opacity'
            
        Returns:
            The radial gradient element
        """
        gradient = ET.Element("radialGradient")
        gradient.set("id", id)
        gradient.set("cx", str(cx))
        gradient.set("cy", str(cy))
        gradient.set("r", str(r))
        
        if fx is not None:
            gradient.set("fx", str(fx))
        if fy is not None:
            gradient.set("fy", str(fy))
            
        if stops:
            for stop in stops:
                stop_el = ET.SubElement(gradient, "stop")
                stop_el.set("offset", str(stop.get("offset", 0)))
                stop_el.set("stop-color", stop.get("color", "#000"))
                if "opacity" in stop:
                    stop_el.set("stop-opacity", str(stop["opacity"]))
                    
        return gradient
        
    @staticmethod
    def rainbow_gradient(id: str, horizontal: bool = True) -> ET.Element:
        """
        Create a rainbow gradient.
        
        Args:
            id: Unique identifier for the gradient
            horizontal: If True, gradient is horizontal, otherwise vertical
            
        Returns:
            A linear gradient element with rainbow colors
        """
        stops = [
            {"offset": "0%", "color": "#ff0000"},
            {"offset": "16.67%", "color": "#ffff00"},
            {"offset": "33.33%", "color": "#00ff00"},
            {"offset": "50%", "color": "#00ffff"},
            {"offset": "66.67%", "color": "#0000ff"},
            {"offset": "83.33%", "color": "#ff00ff"},
            {"offset": "100%", "color": "#ff0000"}
        ]
        
        if horizontal:
            return GradientLibrary.create_linear_gradient(id, 0, 0, 1, 0, stops)
        else:
            return GradientLibrary.create_linear_gradient(id, 0, 0, 0, 1, stops)
            
    @staticmethod
    def metallic_gradient(id: str, base_color: str = "#888888") -> ET.Element:
        """
        Create a metallic effect gradient.
        
        Args:
            id: Unique identifier for the gradient
            base_color: Base color of the metallic effect
            
        Returns:
            A linear gradient element with metallic effect
        """
        stops = [
            {"offset": "0%", "color": "#ffffff", "opacity": 0.7},
            {"offset": "45%", "color": base_color},
            {"offset": "55%", "color": base_color},
            {"offset": "100%", "color": "#000000", "opacity": 0.3}
        ]
        
        return GradientLibrary.create_linear_gradient(id, 0, 0, 0, 1, stops)
