#!/usr/bin/env python3
"""
Example usage of the Moret plugin with fz

This script demonstrates how to run MORET parametric calculations
using the fz-moret plugin.
"""

import fz

# Example 1: Basic usage with single parameter variation
print("Example 1: Single parameter variation")
print("=" * 50)

# Define parameter values to vary the sphere radius
input_variables_1 = {
    "radius": [8.0, 8.5, 9.0],  # Three different radius values
}

# Note: This example assumes MORET is installed and configured
# It will parse the input file and identify variables, but won't actually
# run the calculation unless MORET is available

# Parse the input file to identify variables
variables = fz.fzi("godiva.m5", "Moret")
print(f"Variables found in godiva.m5: {variables}")

# Example 2: Multi-parameter variation
print("\nExample 2: Multi-parameter variation")
print("=" * 50)

# Create a template file with multiple parameters
template_content = """MORET_BEGIN
TITLE GODIVA PARAMETRIC

TERM
  CYCL
    ACTI 100
    PASS 3
  KEFF
    SIGM 0.001
ENDT

* Geometry modelling
GEOM
  MODU 0
  TYPE 1 SPHE $(radius)
  VOLU Ext0 0 1 1 0.0 0.0 0.0
  ENDM
ENDG

* Description of the materials
MATE
  CONT 
  LIBR jeff311.xml 
  TEMP 300 
  
  COMP UMET
    CONC
    U234     4.91895E-04
    U235     $(u235_frac)
    U238     2.49865E-03
  ENDC   
ENDM

* Neutron source distribution
SOUR
  POIN 1000
    MODU 0
    VOLU Ext0 0.0 0.0 0.0
  ENDP
ENDS

* geometry plotting 
GRAP  Z 0.0  ENDG
PAIN  Z 0.0  ENDP

* Simuation properties
SIMU
  NATU
FSIM

ENDD
MORET_END
"""

# Save the template
with open("godiva_template.m5", "w") as f:
    f.write(template_content)

# Define multiple parameters
input_variables_2 = {
    "radius": [8.0, 8.5, 9.0],
    "u235_frac": [4.49988e-02, 5.0e-02, 5.5e-02]
}

# Parse the template
variables_2 = fz.fzi("godiva_template.m5", "Moret")
print(f"Variables found in template: {variables_2}")

# Example 3: Compile input files (substitute values)
print("\nExample 3: Compiling input files")
print("=" * 50)

# Compile the template with specific values
fz.fzc(
    "godiva_template.m5",
    {"radius": 8.5, "u235_frac": 5.0e-02},
    "Moret",
    output_dir="compiled_example"
)
print("Compiled input saved to: compiled_example/")

# Example 4: Full parametric run (requires MORET installation)
print("\nExample 4: Full parametric calculation")
print("=" * 50)
print("Note: This requires MORET to be installed at /opt/MORET/scripts/moret.py")
print("If MORET is not installed, this step will be skipped.\n")

# Uncomment the following code to run a full parametric study
# (only if MORET is installed)
"""
results = fz.fzr(
    "godiva_template.m5",
    input_variables_2,
    "Moret",
    calculators="Localhost_Moret",
    results_dir="moret_results"
)

print("Results:")
print(results[['radius', 'u235_frac', 'mean_keff', 'sigma_keff', 'status']])

# Access specific results
print(f"\nMean keff values: {results['mean_keff'].tolist()}")
print(f"Sigma keff values: {results['sigma_keff'].tolist()}")
"""

print("\nExample complete!")
print("\nTo run full calculations:")
print("  1. Install MORET at /opt/MORET/scripts/moret.py")
print("  2. Uncomment the fzr call in this script")
print("  3. Run: python example_usage.py")
