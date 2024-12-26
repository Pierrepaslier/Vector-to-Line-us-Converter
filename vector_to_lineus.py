import sys
import os
import re

def generate_new_filename(output_dir):
    """Generate the next sequential filename in the LineUs folder."""
    files = [f for f in os.listdir(output_dir) if f.endswith(".txt")]
    highest_number = 0
    for file in files:
        match = re.search(r"(\d+)\.txt$", file)
        if match:
            highest_number = max(highest_number, int(match.group(1)))
    return os.path.join(output_dir, f"{highest_number + 1:08d}.txt")

def process_plt_file(input_file, output_file):
    """Convert the .plt file to Line Us format and write it to the output file."""
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        outfile.write("G54 X437 Y574 S0.1\n")  # Header
        
        for line in infile:
            instructions = line.strip().split(";")
            for instruction in instructions:
                if not instruction or instruction == "IN":
                    continue
                
                pen_action = instruction[:2]
                coordinates = instruction[2:]
                
                if pen_action == "PU":  # Pen UP
                    if coordinates:
                        x, y = map(str.strip, coordinates.split(","))
                        outfile.write(f"G01 X{x} Y{y} Z1000\n")
                        outfile.write(f"G01 X{x} Y{y} Z0\n")
                    else:
                        outfile.write("G01 Z1000\n")
                elif pen_action == "PD":  # Pen DOWN
                    if coordinates:
                        x, y = map(str.strip, coordinates.split(","))
                        outfile.write(f"G01 X{x} Y{y} Z0\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 vector_to_lineus.py input.plt /path/to/LineUsFiles/")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)
    
    if not os.path.isdir(output_dir):
        print(f"Error: Output directory '{output_dir}' does not exist.")
        sys.exit(1)
    
    output_file = generate_new_filename(output_dir)
    process_plt_file(input_file, output_file)
    
    print(f"Conversion complete. File saved to {output_file}")

if __name__ == "__main__":
    main()
