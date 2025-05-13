"""
Unit tests for SVG element creation and manipulation.
"""
import pytest
import xml.etree.ElementTree as ET
from svg_generator.elements.factory import ElementFactory


def test_create_circle():
    """Test that circle elements are created correctly."""
    circle = ElementFactory.create_circle(100, 100, 50, fill="red", stroke="black")
    
    # Check that the created circle contains the expected attributes
    assert '<circle' in circle
    assert 'cx="100"' in circle
    assert 'cy="100"' in circle
    assert 'r="50"' in circle
    assert 'fill="red"' in circle
    assert 'stroke="black"' in circle


def test_create_rectangle():
    """Test that rectangle elements are created correctly."""
    rect = ElementFactory.create_rectangle(10, 20, 100, 50, fill="blue")
    
    # Check that the created rectangle contains the expected attributes
    assert '<rect' in rect
    assert 'x="10"' in rect
    assert 'y="20"' in rect
    assert 'width="100"' in rect
    assert 'height="50"' in rect
    assert 'fill="blue"' in rect


def test_create_line():
    """Test that line elements are created correctly."""
    line = ElementFactory.create_line(0, 0, 100, 100, stroke="green", stroke_width=2)
    
    # Check that the created line contains the expected attributes
    assert '<line' in line
    assert 'x1="0"' in line
    assert 'y1="0"' in line
    assert 'x2="100"' in line
    assert 'y2="100"' in line
    assert 'stroke="green"' in line
    assert 'stroke_width="2"' in line


def test_create_path():
    """Test that path elements are created correctly."""
    path_data = "M 0,0 L 100,100 L 0,100 Z"
    path = ElementFactory.create_path(path_data, fill="yellow", stroke="black")
    
    # Check that the created path contains the expected attributes
    assert '<path' in path
    assert f'd="{path_data}"' in path
    assert 'fill="yellow"' in path
    assert 'stroke="black"' in path


def test_create_text():
    """Test that text elements are created correctly."""
    text = ElementFactory.create_text(50, 50, "Hello, SVG!", font_size=14)
    
    # Check that the created text contains the expected attributes and content
    assert '<text' in text
    assert 'x="50"' in text
    assert 'y="50"' in text
    assert 'font_size="14"' in text
    assert '>Hello, SVG!</text>' in text
