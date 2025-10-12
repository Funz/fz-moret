# fz-moret

fz Moret model plugin for MORET calculations

## Description

This plugin is dedicated to launch MORET calculations from fz (Funz parametric computing framework).
It supports the following syntax and features:

### Input

- **File type supported**: `*.m5`, any other format for resources
- **Parameter syntax**:
  - Variable syntax: `$(...)`
  - Formula syntax: `@{...}`
  - Comment char: `*`
  
#### Example input file:

```
MORET_BEGIN

...
GEOM
  MODU 0
  TYPE 1 SPHE $(radius~[1,20])
  VOLU Ext0 0 1 1 0.0 0.0 0.0
  ENDM
ENDG

MATE
  ...
  COMP UMET
    CONC
    U234     4.91895E-04
    U235     $(u5~4.49988E-02)
    U238     2.49865E-03
  ENDC   
ENDM
...
ENDD
MORET_END
```

This will identify input variables:
- `radius`, expected to vary inside [1,20]
- `u5`, expected to vary inside [0,1] (by default), with default value 4.49988E-02

### Output

- **File type supported**: `*.listing`
- **Extracted values**: `mean_keff`, `sigma_keff`, `dkeff_pertu`, `sigma_dkeff_pertu`

#### Example output file:

```
...
##                                             ESTIMATION FINALE DU KEFF                                              ##
##                                                                                                                    ##
##                                                          KEFF     ECART TYPE    INTERVALLE A +/- 3 SIGMA           ##
##                 ETAPE    417  ESTI. + FAIBLE SIGMA     0.99612 +/-  0.00100  :  0.99314 < KEFF < 0.99911           ##
...
```

This will return output:
- `mean_keff` = 0.99612
- `sigma_keff` = 0.00100

## Usage

### Example Script

Run the included example script to see how the plugin works:

```bash
python example_usage.py
```

This will demonstrate:
- Parsing input files to identify variables
- Creating parametric templates
- Compiling input files with specific parameter values

### Basic Example

```python
import fz

# Define parameter values
input_variables = {
    "radius": [8.0, 8.5, 9.0],
    "u5": 4.49988E-02
}

# Run parametric study
results = fz.fzr(
    "godiva.m5",
    input_variables,
    "Moret",
    calculators="Localhost_Moret",
    results_dir="moret_results"
)

print(results)
```

### Parsing Input Variables

```python
import fz

# Parse input file to identify variables
variables = fz.fzi("godiva.m5", "Moret")
print(variables)
```

### Compiling Input Files

```python
import fz

# Compile input file with specific parameter values
fz.fzc(
    "godiva.m5",
    {"radius": 8.5, "u5": 5.0e-02},
    "Moret",
    output_dir="compiled"
)
```

### Model Structure

The plugin provides:
- `.fz/models/Moret.json` - Model definition with input/output parsing
- `.fz/calculators/Moret.sh` - Shell script to run MORET
- `.fz/calculators/Localhost_Moret.json` - Local calculator configuration

## Installation

This plugin requires MORET to be installed at `/opt/MORET/scripts/moret.py`.
If your MORET installation is in a different location, update the path in `.fz/calculators/Moret.sh`.

## Repository Structure

```
fz-moret/
├── .fz/
│   ├── models/
│   │   └── Moret.json              # Model definition
│   ├── calculators/
│   │   ├── Moret.sh                # Calculator script
│   │   └── Localhost_Moret.json    # Calculator alias
├── godiva.m5                        # Sample input file
├── example_usage.py                 # Example usage script
├── .gitignore                       # Git ignore patterns
└── README.md                        # This file
```

## Files Description

- **`.fz/models/Moret.json`**: Defines the Moret model including:
  - Input parsing configuration (variable prefix `$`, formula prefix `@`, comment char `*`)
  - Output extraction commands for `mean_keff`, `sigma_keff`, `dkeff_pertu`, `sigma_dkeff_pertu`

- **`.fz/calculators/Moret.sh`**: Shell script that:
  - Accepts a `.m5` file or directory as input
  - Validates the input is a MORET file
  - Runs the MORET calculation
  - Checks for successful output generation

- **`.fz/calculators/Localhost_Moret.json`**: Calculator alias configuration for local execution

- **`godiva.m5`**: Sample MORET input file (GODIVA critical assembly)

- **`example_usage.py`**: Example Python script demonstrating various plugin features

