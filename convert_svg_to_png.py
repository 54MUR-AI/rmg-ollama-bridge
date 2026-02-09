from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET

# Read the SVG file
with open('icon.svg', 'r') as f:
    svg_content = f.read()

# Parse SVG to get the path data
tree = ET.fromstring(svg_content)
path_element = tree.find('.//{http://www.w3.org/2000/svg}path')
path_data = path_element.get('d')

print(f"Path data: {path_data[:100]}...")

# For now, create a simple red flame icon based on the Lucide Flame shape
# Since PIL doesn't natively support SVG path rendering, we'll create a simplified version

def create_lucide_flame_png(size):
    """Create a red flame icon matching Lucide Flame design"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Scale factor
    scale = size / 24
    
    # Red color
    red = (230, 57, 70, 255)
    
    # Simplified Lucide Flame shape as polygon approximation
    # Based on the path: M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z
    
    points = [
        (12*scale, 6*scale),   # Top
        (14*scale, 8*scale),
        (16*scale, 12*scale),
        (17*scale, 15*scale),
        (16*scale, 18*scale),
        (14*scale, 20*scale),
        (12*scale, 21*scale),  # Bottom
        (10*scale, 20*scale),
        (8*scale, 18*scale),
        (7*scale, 15*scale),
        (8*scale, 12*scale),
        (10*scale, 8*scale),
    ]
    
    # Draw filled flame
    draw.polygon(points, fill=red)
    
    return img

# Create all sizes
print("Creating PNG icons from Lucide Flame SVG...")
create_lucide_flame_png(128).save('icon128.png', 'PNG')
print("Created icon128.png")

create_lucide_flame_png(48).save('icon48.png', 'PNG')
print("Created icon48.png")

create_lucide_flame_png(16).save('icon16.png', 'PNG')
print("Created icon16.png")

print("\n✅ All PNG icons created successfully!")
