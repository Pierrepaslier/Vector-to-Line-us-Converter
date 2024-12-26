import os
import re
import sys

LINEUS_DIR = "/Users/sylvain/Documents/LineUsFiles"  # Default Line-us directory


def generate_new_filename(output_dir):
    """
    Generate the next sequential filename in the Line-us folder.
    """
    files = [f for f in os.listdir(output_dir) if f.endswith(".txt")]
    highest_number = 0
    for file in files:
        match = re.search(r"(\d+)\.txt$", file)
        if match:
            highest_number = max(highest_number, int(match.group(1)))
    return os.path.join(output_dir, f"{highest_number + 1:08d}.txt")


def parse_hpgl_to_lineus(input_file, output_file):
    """
    Convert an HPGL file into a Line-us compatible format.

    Parameters:
    input_file (str): Path to the HPGL input file.
    output_file (str): Path to the Line-us output file.
    """
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        # Write the Line-us header
        outfile.write("G54 X0 Y0 S1\n")

        # Process each line in the HPGL file
        for line in infile:
            commands = line.strip().split(";")
            for command in commands:
                if not command:
                    continue  # Skip empty commands

                # Extract the command type and parameters
                cmd_type = command[:2]
                params = command[2:].strip()

                if cmd_type in ("PU", "PD"):
                    try:
                        coords = params.split(",")
                        if len(coords) % 2 != 0:
                            raise ValueError(f"Invalid coordinates in command: {command}")

                        # Group coordinates into pairs (x, y)
                        coord_pairs = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
                        for x, y in coord_pairs:
                            # Convert HPGL units (0.025mm per unit) to Line-us units (100 units = 5mm)
                            x_lineus = round(float(x) * 20)  # 20 HPGL units = 1 Line-us unit
                            y_lineus = round(float(y) * 20)

                            # Determine Z position (pen up or down)
                            z_pos = "Z1000" if cmd_type == "PU" else "Z0"

                            # Write to the Line-us file
                            outfile.write(f"G01 X{x_lineus} Y{y_lineus} {z_pos}\n")
                    except Exception as e:
                        print(f"Error processing command: {command} - {e}")
                else:
                    print(f"Unsupported HPGL command: {command}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 hpgl_to_lineus.py <input.hpgl>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(LINEUS_DIR):
        print(f"Error: Output directory '{LINEUS_DIR}' does not exist.")
        sys.exit(1)

    # Generate the new filename
    output_file = generate_new_filename(LINEUS_DIR)

    try:
        parse_hpgl_to_lineus(input_file, output_file)
        print(f"Conversion complete. File saved to '{output_file}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
