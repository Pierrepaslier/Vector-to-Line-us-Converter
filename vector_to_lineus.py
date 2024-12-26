import os
import re
import sys

def generate_new_filename(output_dir):
    """Generate the next sequential filename in the LineUs folder."""
    files = [f for f in os.listdir(output_dir) if f.endswith(".txt")]
    highest_number = 0
    for file in files:
        match = re.search(r"(\d+)\.txt$", file)
        if match:
            highest_number = max(highest_number, int(match.group(1)))
    return os.path.join(output_dir, f"{highest_number + 1:08d}.txt")

def process_hpgl_file(input_file, output_file):
    """Convert the HPGL file to Line Us format and write it to the output file."""
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        outfile.write("G54 X437 Y574 S0.1\n")  # Header
        
        for line in infile:
            instructions = line.strip().split(";")
            for instruction in instructions:
                if not instruction or instruction == "IN":
                    continue  # Skip empty instructions and the "IN" command
                
                pen_action = instruction[:2]
                coordinates = instruction[2:]
                
                # Handle coordinates with error handling
                try:
                    coords = list(map(str.strip, coordinates.split(",")))
                    if len(coords) != 2:
                        raise ValueError(f"Invalid coordinate format: {coordinates}")
                    x, y = coords
                except Exception as e:
                    print(f"Error processing instruction: {instruction} - {e}")
                    continue

                if pen_action == "PU":  # Pen UP
                    outfile.write(f"G01 X{x} Y{y} Z1000\n")
                    outfile.write(f"G01 X{x} Y{y} Z0\n")
                elif pen_action == "PD":  # Pen DOWN
                    outfile.write(f"G01 X{x} Y{y} Z0\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 vector_to_lineus.py input.hpgl")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = "/Users/sylvain/Documents/LineUsFiles"  # Default Line-us directory
    
    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)
    
    if not os.path.isdir(output_dir):
        print(f"Error: Output directory '{output_dir}' does not exist.")
        sys.exit(1)
    
    output_file = generate_new_filename(output_dir)
    process_hpgl_file(input_file, output_file)
    
    print(f"Conversion complete. File saved to {output_file}")

if __name__ == "__main__":
    main()
