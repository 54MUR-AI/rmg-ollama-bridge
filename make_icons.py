from PIL import Image, ImageDraw

# Create a simple, solid red flame icon
def create_simple_flame(size):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Red color
    red = (230, 57, 70, 255)
    
    # Simple flame shape - teardrop
    center_x = size // 2
    
    # Draw main flame body as ellipse
    draw.ellipse([size*0.25, size*0.15, size*0.75, size*0.85], fill=red)
    
    # Draw flame tip (triangle on top)
    tip_points = [
        (center_x, size*0.05),
        (size*0.35, size*0.3),
        (size*0.65, size*0.3)
    ]
    draw.polygon(tip_points, fill=red)
    
    return img

# Generate icons
print("Creating icons...")
icon128 = create_simple_flame(128)
icon128.save('icon128.png', 'PNG')
print(f"icon128.png created - size: {icon128.size}")

icon48 = create_simple_flame(48)
icon48.save('icon48.png', 'PNG')
print(f"icon48.png created - size: {icon48.size}")

icon16 = create_simple_flame(16)
icon16.save('icon16.png', 'PNG')
print(f"icon16.png created - size: {icon16.size}")

favicon = create_simple_flame(32)
favicon.save('favicon.png', 'PNG')
print(f"favicon.png created - size: {favicon.size}")

print("\n✅ All icons created successfully!")
