from PIL import Image, ImageDraw
import os

# Create icon directory
icon_dir = "assets"
if not os.path.exists(icon_dir):
    os.makedirs(icon_dir)

# Create a simple OmniSync icon (256x256)
size = 256
img = Image.new('RGB', (size, size), color='#1e1e1e')
draw = ImageDraw.Draw(img)

# Draw a circle in the center (representing phone/sync)
circle_size = 180
x0 = (size - circle_size) // 2
y0 = (size - circle_size) // 2
draw.ellipse([x0, y0, x0 + circle_size, y0 + circle_size], fill='#0066ff', outline='#0066ff')

# Draw a phone shape inside
phone_width = 80
phone_height = 140
phone_x = (size - phone_width) // 2
phone_y = (size - phone_height) // 2 + 10
draw.rectangle([phone_x, phone_y, phone_x + phone_width, phone_y + phone_height], outline='#ffffff', width=3)

# Draw sync arrows
arrow_size = 40
for offset in [-50, 50]:
    x = size // 2 + offset
    y = size // 2 - 70
    draw.line([(x - arrow_size//2, y), (x + arrow_size//2, y)], fill='#00ff00', width=4)
    draw.polygon([(x + arrow_size//2, y), (x + arrow_size//2 - 15, y - 10), (x + arrow_size//2 - 15, y + 10)], fill='#00ff00')

# Save icon as ICO and PNG
img.save(f'{icon_dir}/omnisync.ico')
img.save(f'{icon_dir}/omnisync.png')
print("Icons created successfully!")
print(f"- {icon_dir}/omnisync.ico")
print(f"- {icon_dir}/omnisync.png")
