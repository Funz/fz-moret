# Moret Plugin Migration Summary

This document describes how the old Moret plugin (https://github.com/Funz/plugin-Moret) was ported to the new fz format.

## Old Plugin Structure

The old plugin used the following files:
- `src/main/io/Moret.ioplugin` - Input/output configuration
- `src/main/scripts/Moret.sh` - Shell script to run MORET
- `src/main/samples/godiva.m5` - Sample input file

## New Plugin Structure

The new plugin uses the fz format:
- `.fz/models/Moret.json` - Model definition (replaces Moret.ioplugin)
- `.fz/calculators/Moret.sh` - Calculator script (similar to old script)
- `.fz/calculators/Localhost_Moret.json` - Calculator alias configuration
- `godiva.m5` - Sample input file (same as old plugin)

## Migration Mapping

### 1. Input/Output Configuration

**Old format** (`Moret.ioplugin`):
```
variableStartSymbol=$
variableLimit=(...)
formulaStartSymbol=@
formulaLimit={...}
commentLineChar=*
```

**New format** (`.fz/models/Moret.json`):
```json
{
    "varprefix": "$",
    "delim": "()",
    "formulaprefix": "@",
    "commentline": "*"
}
```

### 2. Output Extraction

**Old format** used custom DSL:
```
output.mean_keff.get=grep("(.*).listing","(FAIBLE|LOWEST) SIGMA") >> get(1) >> cut("SIGMA",2) >> replace("ESTI.","") >> substring("ZZZ","+/-") >> asNumeric()
```

**New format** uses shell commands directly:
```json
{
    "output": {
        "mean_keff": "grep -E '(FAIBLE|LOWEST) SIGMA' *.listing | head -1 | awk '{for(i=1;i<=NF;i++) if($i ~ /^[0-9]+\\.[0-9]+$/ && $(i+1) ~ /^\\+\\/\\-$/) {print $i; exit}}'"
    }
}
```

### 3. Calculator Script

**Old format**:
```bash
#!/bin/bash
/opt/MORET/scripts/moret.py $*
```

**New format**: Enhanced with input validation, error handling, and fz compatibility:
```bash
#!/bin/bash
# Moret calculator script for fz
# Input validation and file discovery
# Run MORET with proper error handling
# Verify output generation
```

### 4. Calculator Configuration

**New addition** - Calculator alias (`.fz/calculators/Localhost_Moret.json`):
```json
{
    "uri": "sh://",
    "n": 2,
    "models": {
        "Moret": "bash .fz/calculators/Moret.sh"
    }
}
```

This allows using the calculator by name: `calculators="Localhost_Moret"`

## Key Differences

1. **Simpler syntax**: The new format uses standard JSON and shell commands instead of custom DSL
2. **More flexible**: Output extraction uses any shell command, not just predefined functions
3. **Better organized**: Separate files for model definition and calculator configuration
4. **Calculator aliases**: Can define named calculator configurations for easy reuse
5. **Python integration**: Designed to work seamlessly with the fz Python API

## Output Variables

Both old and new plugins extract the same output variables:
- `mean_keff` - Mean k-effective value
- `sigma_keff` - Standard deviation of k-effective
- `dkeff_pertu` - Delta k-effective for perturbation (if PERTU in input)
- `sigma_dkeff_pertu` - Standard deviation of delta k-effective (if PERTU in input)

## Usage Comparison

### Old Plugin (Java-based Funz)

```java
// Java API usage
Run r = new Run("MORET", "godiva.m5");
r.setInputVariable("radius", "8.0");
r.run();
```

### New Plugin (Python-based fz)

```python
# Python API usage
import fz
results = fz.fzr(
    "godiva.m5",
    {"radius": 8.0},
    "Moret",
    calculators="Localhost_Moret"
)
```

## Additional Features

The new plugin includes:
- `example_usage.py` - Comprehensive usage examples
- `validate_plugin.py` - Plugin structure validation
- `.gitignore` - Git ignore patterns for temporary files
- Enhanced README with detailed documentation

## Testing

Run the validation script to verify the plugin structure:
```bash
python validate_plugin.py
```

All validations should pass, confirming the plugin is correctly configured.
