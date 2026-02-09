from PIL import Image, ImageDraw

def create_flame_icon(size):
    """Create a red flame icon matching the Lucide Flame design"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Scale factor from 24x24 viewBox to desired size
    scale = size / 24
    
    # Red color matching RMG theme
    red = (230, 57, 70, 255)
    
    # Lucide Flame path simplified to drawable shapes
    # Main flame body
    points = [
        (8.5*scale, 14.5*scale),
        (11*scale, 12*scale),
        (10*scale, 9*scale),
        (12*scale, 6*scale),
        (14*scale, 12.5*scale),
        (17*scale, 14*scale),
        (18*scale, 15*scale),
        (18*scale, 17*scale),
        (12*scale, 21*scale),
        (6*scale, 17*scale),
        (6*scale, 15*scale),
        (8.5*scale, 14.5*scale)
    ]
    
    # Draw flame outline
    draw.polygon(points, outline=red, width=max(2, int(2*scale)))
    
    # Add inner detail
    inner_points = [
        (11*scale, 14*scale),
        (12*scale, 12*scale),
        (13*scale, 14*scale),
        (12*scale, 16*scale),
        (11*scale, 14*scale)
    ]
    draw.polygon(inner_points, fill=red)
    
    return img

# Create all icon sizes
create_flame_icon(128).save('icon128.png')
create_flame_icon(48).save('icon48.png')
create_flame_icon(16).save('icon16.png')
create_flame_icon(32).save('favicon.png')

print('✅ Created red flame icons: icon128.png, icon48.png, icon16.png, favicon.png')
