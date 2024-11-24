import os

OUTPUT_DIR = "./assets/images/"  # Directory containing processed images
HTML_OUTPUT_FILE = "responsive_images.html"  # Output HTML file name

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
                html_lines.append(f"        <source srcset='{OUTPUT_DIR}{file_path}' media='(max-width: {res_name[:-1]}px)'>")

            # Add fallback <img> tag
            fallback_image = sorted_resolutions[-1][1]  # Use the largest resolution as fallback
            html_lines.append(f"        <img src='{OUTPUT_DIR}{fallback_image}' alt='{base_name}' loading='lazy'>")
            html_lines.append(f"    </picture>")
            html_lines.append(f"    <br>")  # Add a line break between images

    # Close HTML tags
    html_lines.extend([
        "</body>",
        "</html>"
    ])

    # Write the HTML code to a file
    with open(HTML_OUTPUT_FILE, "w") as html_file:
        html_file.write("\n".join(html_lines))

    print(f"HTML code written to {HTML_OUTPUT_FILE}")

if __name__ == "__main__":
    generate_html()
