from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

# Convert SVG to PNG using svglib
drawing = svg2rlg('icon.svg')

# Render at different sizes
renderPM.drawToFile(drawing, 'icon128.png', fmt='PNG', dpi=72, bg=0xffffff00)
print("Created icon128.png")

# For smaller sizes, we need to scale
from reportlab.graphics import renderPDF
drawing.width = 48
drawing.height = 48
drawing.scale(48/128, 48/128)
renderPM.drawToFile(drawing, 'icon48.png', fmt='PNG', dpi=72, bg=0xffffff00)
print("Created icon48.png")

# Reload and scale for 16x16
drawing = svg2rlg('icon.svg')
drawing.width = 16
drawing.height = 16
drawing.scale(16/128, 16/128)
renderPM.drawToFile(drawing, 'icon16.png', fmt='PNG', dpi=72, bg=0xffffff00)
print("Created icon16.png")

print("\n✅ SVG converted to PNG successfully!")
