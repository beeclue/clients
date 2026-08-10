import os
import argparse
from PIL import Image

def convert_to_webp(input_path, output_path=None, quality=80):
    """Converts an image to WebP format."""
    try:
        if not output_path:
            # Create output path by changing extension to .webp
            base_name, _ = os.path.splitext(input_path)
            output_path = f"{base_name}.webp"
            
        # Open the image
        with Image.open(input_path) as img:
            # Convert RGBA images properly if needed, though WebP supports transparency
            img.save(output_path, 'WEBP', quality=quality)
        print(f"Successfully converted: {input_path} -> {output_path}")
        return True
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Convert JPG/PNG images to WebP.")
    parser.add_argument("input", nargs='+', help="Input image file(s) or directory to process")
    parser.add_argument("-q", "--quality", type=int, default=80, help="WebP quality (0-100), default: 80")
    parser.add_argument("-o", "--outdir", help="Output directory for converted images (optional)")
    
    args = parser.parse_args()
    
    valid_extensions = ('.png', '.jpg', '.jpeg')
    
    files_to_convert = []
    for item in args.input:
        if os.path.isdir(item):
            for file in os.listdir(item):
                if file.lower().endswith(valid_extensions):
                    files_to_convert.append(os.path.join(item, file))
        elif os.path.isfile(item):
            if item.lower().endswith(valid_extensions):
                files_to_convert.append(item)
            else:
                print(f"Skipping {item}: not a .jpg, .jpeg, or .png file")
        else:
            print(f"Skipping {item}: path does not exist")
            
    if not files_to_convert:
        print("No valid images found to convert.")
        return
        
    if args.outdir and not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
        
    for file_path in files_to_convert:
        output_path = None
        if args.outdir:
            base_name = os.path.basename(file_path)
            name_without_ext, _ = os.path.splitext(base_name)
            output_path = os.path.join(args.outdir, f"{name_without_ext}.webp")
            
        convert_to_webp(file_path, output_path, args.quality)

if __name__ == "__main__":
    main()
