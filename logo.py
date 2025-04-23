import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    # Create a new image with white background
    width, height = 300, 300
    background_color = (255, 255, 255)
    image = Image.new("RGBA", (width, height), background_color)
    
    # Create a drawing context
    draw = ImageDraw.Draw(image)
    
    # Draw a circle
    circle_color = (245, 235, 224)  # Light beige
    circle_position = (width // 2, height // 2)
    circle_radius = 120
    draw.ellipse(
        (
            circle_position[0] - circle_radius,
            circle_position[1] - circle_radius,
            circle_position[0] + circle_radius,
            circle_position[1] + circle_radius,
        ),
        fill=circle_color,
    )
    
    # Draw another smaller circle
    inner_circle_color = (200, 180, 160)  # Darker beige
    inner_circle_radius = 90
    draw.ellipse(
        (
            circle_position[0] - inner_circle_radius,
            circle_position[1] - inner_circle_radius,
            circle_position[0] + inner_circle_radius,
            circle_position[1] + inner_circle_radius,
        ),
        fill=inner_circle_color,
    )
    
    # Draw the "E" letter in the center
    text_color = (255, 255, 255)  # White
    try:
        # Try to use Arial font, fallback to default if not available
        font = ImageFont.truetype("arial.ttf", 150)
    except IOError:
        font = ImageFont.load_default()
    
    text = "E"
    text_position = (width // 2, height // 2)
    
    # Get text size to center it
    text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (80, 80)
    text_position = (text_position[0] - text_width // 2, text_position[1] - text_height // 2)
    
    # Draw the text
    try:
        draw.text(text_position, text, font=font, fill=text_color)
    except:
        # Fallback method for newer versions of Pillow
        draw.text((width // 2 - 40, height // 2 - 60), text, fill=text_color, font=font)
    
    # Save the image
    logo_path = "logo.png"
    image.save(logo_path)
    print(f"Logo saved to {logo_path}")
    
    return logo_path

if __name__ == "__main__":
    create_logo() 