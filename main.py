import os
from PIL import Image, ImageOps

# Define target resolutions and their folder names
RESOLUTIONS = {
    "144p": 256,   # 144p is approximately 256 pixels wide
    "240p": 426,
    "360p": 640,
    "480p": 854,
    "720p": 1280,
    "1080p": 1920,
    "1440p": 2048,
    "2160p": 3840
}

# Source and output directories
SOURCE_DIR = "./"  # Replace with your source directory
OUTPUT_DIR = "./assets/images/"  # Replace with your target directory

def convert_to_webp(input_path, output_dir, resolution_name, max_width):
    """Convert an image to WebP format with specified settings."""
    with Image.open(input_path) as img:
        # Apply EXIF orientation (preserve current rotation)
        img = ImageOps.exif_transpose(img)

        # Preserve aspect ratio by resizing
        img.thumbnail((max_width, max_width * img.height // img.width))

        # Convert image to RGB (no transparency)
        img = img.convert("RGB")

        # Define output file path
        output_path = os.path.join(output_dir, resolution_name, os.path.splitext(os.path.basename(input_path))[0] + ".webp")

        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save the image in WebP format with 256 colors and 75% quality
        img.save(output_path, format="WEBP", quality=75, method=6)
        print(f"Saved: {output_path}")

def process_images():
    """Process all images in the source directory."""
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            input_path = os.path.join(root, file)
            if not file.lower().endswith(("jpg", "jpeg", "png")):
                continue  # Skip non-image files

            for resolution_name, max_width in RESOLUTIONS.items():
                convert_to_webp(input_path, OUTPUT_DIR, resolution_name, max_width)

def generate_html():
    """Generate HTML code for the images in output_images folder."""
    html_lines = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "    <meta charset='UTF-8'>",
        "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        "    <title>Responsive Images</title>",
        "</head>",
        "<body>",
        "    <h1>Responsive Images</h1>"
    ]

    for root, dirs, _ in os.walk(OUTPUT_DIR):
        dirs.sort()  # Ensure resolutions are processed in order
        images = {}

        for resolution in dirs:
            resolution_dir = os.path.join(root, resolution)
            for file in os.listdir(resolution_dir):
                if file.endswith(".webp"):
                    # Extract base name without resolution
                    base_name = os.path.splitext(file)[0]
                    if base_name not in images:
                        images[base_name] = {}
                    images[base_name][resolution] = os.path.join(resolution, file)

        for base_name, resolution_files in images.items():
            html_lines.append(f"    <picture>")

            # Sort resolutions in ascending order of size for `srcset`
            sorted_resolutions = sorted(
                resolution_files.items(),
                key=lambda x: int(x[0][:-1].replace('p', ''))  # Extract numeric resolution
            )

            for res_name, file_path in sorted_resolutions:
                html_lines.append(f"        <source srcset='{file_path}' media='(max-width: {res_name[:-1]}px)'>")

            # Add fallback <img> tag
            fallback_image = sorted_resolutions[-1][1]  # Use the largest resolution as fallback
            html_lines.append(f"        <img src='{fallback_image}' alt='{base_name}' loading='lazy'>")
            html_lines.append(f"    </picture>")
            html_lines.append(f"    <br>")  # Add a line break between images

    # Close HTML tags
    html_lines.extend([
        "</body>",
        "</html>"
    ])

    # Write the HTML code to a file
    with open(OUTPUT_DIR, "w") as html_file:
        html_file.write("\n".join(html_lines))

    print(f"HTML code written to {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_html()

