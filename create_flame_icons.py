from PIL import Image, ImageDraw

def create_flame_icon(size):
    """Create a solid red flame icon"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Scale factor from 24x24 viewBox to desired size
    scale = size / 24
    
    # Red color matching RMG theme
    red = (230, 57, 70, 255)
    
    # Simplified flame shape - filled polygon
    points = [
        (12*scale, 4*scale),   # Top point
        (16*scale, 8*scale),   # Right upper
        (18*scale, 12*scale),  # Right middle
        (17*scale, 16*scale),  # Right lower
        (14*scale, 20*scale),  # Bottom right
        (12*scale, 22*scale),  # Bottom center
        (10*scale, 20*scale),  # Bottom left
        (7*scale, 16*scale),   # Left lower
        (6*scale, 12*scale),   # Left middle
        (8*scale, 8*scale),    # Left upper
    ]
    
    # Draw filled flame
    draw.polygon(points, fill=red)
    
    # Add inner lighter flame for depth
    inner_points = [
        (12*scale, 8*scale),
        (14*scale, 11*scale),
        (13*scale, 15*scale),
        (12*scale, 17*scale),
        (11*scale, 15*scale),
        (10*scale, 11*scale),
    ]
    draw.polygon(inner_points, fill=(255, 107, 107, 255))
    
    return img

# Create all icon sizes
create_flame_icon(128).save('icon128.png')
create_flame_icon(48).save('icon48.png')
create_flame_icon(16).save('icon16.png')
create_flame_icon(32).save('favicon.png')

print('✅ Created red flame icons: icon128.png, icon48.png, icon16.png, favicon.png')
