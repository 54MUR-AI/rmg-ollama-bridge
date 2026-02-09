from PIL import Image, ImageDraw

# Create the exact flame shape from the image shown
def create_exact_flame(size):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    scale = size / 100
    red = (230, 57, 70, 255)
    
    # Flame shape matching the reference image
    # Smooth curved flame
    points = [
        (50*scale, 20*scale),   # Top
        (60*scale, 25*scale),
        (70*scale, 35*scale),
        (75*scale, 50*scale),
        (75*scale, 65*scale),
        (70*scale, 75*scale),
        (60*scale, 82*scale),
        (50*scale, 85*scale),   # Bottom
        (40*scale, 82*scale),
        (30*scale, 75*scale),
        (25*scale, 65*scale),
        (25*scale, 50*scale),
        (30*scale, 35*scale),
        (40*scale, 25*scale),
    ]
    
    draw.polygon(points, fill=red)
    
    # Add the characteristic notch/curve on the left side
    notch_points = [
        (35*scale, 60*scale),
        (30*scale, 55*scale),
        (28*scale, 50*scale),
        (30*scale, 45*scale),
        (35*scale, 42*scale),
        (40*scale, 50*scale),
    ]
    draw.polygon(notch_points, fill=(0, 0, 0, 0))  # Cut out
    
    return img

# Create icons
create_exact_flame(128).save('icon128.png')
create_exact_flame(48).save('icon48.png')
create_exact_flame(16).save('icon16.png')
print("✅ Created exact flame icons")
