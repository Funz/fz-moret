# fz-Moret

Funz plugin for MORET (Monte Carlo calculations for reactor physics)

## Features

This plugin integrates MORET calculations with the Funz parametric computing framework, enabling:
- Automated parametric studies for criticality safety calculations
- Variable substitution in MORET input files
- Formula expressions for derived parameters
- Automatic extraction of keff and uncertainty results
- Support for perturbation calculations

### Input

- **File type supported**: `*.m5`, any other format for resources
- **Parameter syntax**:
  - Variable syntax: `${...}`
  - Formula syntax: `@{...}`
  - Comment char: `*`
  
#### Example input file:

```
MORET_BEGIN

...
GEOM
  MODU 0
  TYPE 1 SPHE ${radius~[8.0,9.0]}
  VOLU Ext0 0 1 1 0.0 0.0 0.0
  ENDM
ENDG

MATE
  ...
  COMP UMET
    CONC
    U234     4.91895E-04
    U235     ${u5~4.49988E-02}
    U238     2.49865E-03
  ENDC   
ENDM
...
ENDD
MORET_END
```

This will identify input variables:
- `radius`, expected to vary inside [8.0,9.0]
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

## Installation

### Prerequisites

1. Install the Funz framework:
   ```bash
   pip install git+https://github.com/Funz/fz.git
   ```

2. Install the Moret plugin:
   ```python
   import fz
   fz.install('Moret')
   ```

3. Install MORET at `/opt/MORET/scripts/moret.py` (or update the path in `.fz/calculators/Moret.sh`)

## Usage

### Quick Start

Open the included Jupyter notebook to see how the plugin works:

```bash
jupyter notebook example_usage.ipynb
```

The notebook demonstrates:
- Parsing input files to identify variables
- Creating parametric templates
- Compiling input files with specific parameter values
- Running parametric studies
- Visualizing results

### Basic Usage

```python
import fz

# Define parameter values
input_variables = {
    "radius": [8.0, 8.5, 9.0],
    "u5": 4.49988E-02
}

# Run parametric study
results = fz.fzr(
    "examples/Moret/godiva.m5",
    input_variables,
    "Moret",
    calculators="localhost_Moret",
    results_dir="moret_results"
)

print(results)
```

### Parsing Input Variables

```python
import fz

# Parse input file to identify variables
variables = fz.fzi("examples/Moret/godiva.m5", "Moret")
print(variables)
```

### Compiling Input Files

```python
import fz

# Compile input file with specific parameter values
fz.fzc(
    "examples/Moret/godiva.m5",
    {"radius": 8.5, "u5": 5.0e-02},
    "Moret",
    output_dir="compiled"
)
```

## Directory Structure

```
fz-Moret/
├── .fz/
│   ├── models/
│   │   └── Moret.json              # Model configuration with syntax rules
│   └── calculators/
│       ├── Moret.sh                # Calculator execution script
│       └── localhost_Moret.json    # Local calculator configuration
├── examples/
│   └── Moret/
│       └── godiva.m5               # Example MORET input file
├── tests/
│   └── test_plugin.py              # Test suite
├── example_usage.ipynb             # Example usage notebook (Jupyter)
├── .gitignore
├── LICENSE                         # BSD-3-Clause license
└── README.md                       # This file
```

## Configuration

### Model Configuration (`.fz/models/Moret.json`)

Defines the input/output syntax for MORET files:
- `id`: Model identifier (`Moret`)
- `varprefix`: Variable prefix character (`$`)
- `formulaprefix`: Formula prefix character (`@`)
- `delim`: Delimiter around variables (`{}`)
- `commentline`: Comment character (`*`)
- `output`: Shell commands mapping output variable names to extraction methods

**Extracted Output Variables:**
- `mean_keff`: Mean effective multiplication factor
- `sigma_keff`: Standard deviation of keff
- `dkeff_pertu`: Perturbation delta-keff (if PERTU is used)
- `sigma_dkeff_pertu`: Standard deviation of delta-keff

### Calculator Configuration (`.fz/calculators/localhost_Moret.json`)

Specifies execution method and command mappings:
- `uri`: Execution protocol (`sh://` for local shell)
- `models`: Maps model name to execution command

### Remote Execution

To run MORET calculations on a remote server via SSH:

1. Create a new calculator configuration file (e.g., `.fz/calculators/Remote_Moret.json`):
   ```json
   {
       "uri": "ssh://username@hostname",
       "models": {
           "Moret": "/path/to/Moret.sh"
       }
   }
   ```

2. Use it in your Funz calls:
   ```python
   results = fz.fzr("examples/Moret/godiva.m5", input_variables, "Moret",
                     calculators="Remote_Moret")
   ```

## Testing

Run the test suite to validate the plugin:

```bash
python tests/test_plugin.py
```

## Customization

To adapt this plugin for your specific needs:

1. **Modify input syntax**: Edit `.fz/models/Moret.json` to change variable/formula prefixes or delimiters
2. **Add output variables**: Add new extraction commands in the `output` section
3. **Change MORET path**: Update the MORET installation path in `.fz/calculators/Moret.sh`
4. **Custom calculator**: Create additional calculator configurations for different execution environments

## Troubleshooting

**Calculator script not executing:**
- Ensure `.fz/calculators/Moret.sh` is executable: `chmod +x .fz/calculators/Moret.sh`
- Verify MORET installation path in the script

**Output extraction failing:**
- Check that MORET produces `.listing` files
- Verify output extraction commands in `.fz/models/Moret.json`
- Test commands manually on a sample `.listing` file

**Variables not recognized:**
- Ensure variable syntax matches the configuration: `${variable_name}`
- Check that comment character `*` is not interfering with variable definitions

## Related Resources

- [Funz framework](https://github.com/Funz/fz) - Main parametric computing framework
- [Funz plugins](https://github.com/Funz) - Other available model plugins
- MORET documentation - Consult your MORET installation for detailed usage

## License

This project is licensed under the BSD 3-Clause License - see the LICENSE file for details.
