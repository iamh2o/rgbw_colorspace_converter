#!/bin/bash

# Number of loops
LOOPS=100

# Timeout duration (set this variable before running the script)
TOUT=${TOUT:-10} # Default to 10 seconds if TOUT is not set

# Array of character patterns to cycle through
CHAR_PATTERNS=("~^." "===" "#####" "||--==" "XOxo." "-|" "|/\\*-o")

# Loop through the commands 100 times
for ((i=1; i<=LOOPS; i++)); do
    echo "Iteration $i of $LOOPS"

    # Dynamically pick a character pattern from the array
    CURRENT_PATTERN=${CHAR_PATTERNS[$((i % ${#CHAR_PATTERNS[@]}))]}

    # Execute commands with the current pattern
    timeout $TOUT run_spectrum_saturation_cycler.py
    timeout $TOUT path_between_2_colors.py
    timeout $TOUT run_color_module_RGB_HSV_HEX_demo.py -z -y -g -u 33
    timeout $TOUT run_color_module_RGB_HSV_HEX_demo.py -b "$CURRENT_PATTERN" -z -y -u 30 -f
    timeout $TOUT run_color_module_RGB_HSV_HEX_demo.py -b "$CURRENT_PATTERN" -z -r -g -u 40 -f
    timeout $TOUT run_color_module_RGB_HSV_HEX_demo.py -b "$CURRENT_PATTERN" -z -n -r -u 20 -f
    timeout $TOUT run_color_module_RGB_HSV_HEX_demo.py -b "$CURRENT_PATTERN" -z -g -y -u 60 -f
    timeout $TOUT run_color_module_RGB_HSV_HEX_demo.py -b "$CURRENT_PATTERN" -z -r -y -u 25 -f
    timeout $TOUT run_color_module_RGB_HSV_HEX_demo.py -b "$CURRENT_PATTERN" -z -g -u 15 -f

    echo "Completed iteration $i with pattern '$CURRENT_PATTERN'"
done

echo "All iterations complete!"