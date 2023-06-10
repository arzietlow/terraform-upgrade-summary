# Terraform Upgrade Summary Script

This script generates a summary of important details from the changelogs of a Terraform upgrade. It provides an easily digestible output that includes bug fixes, enhancements, and new features implemented between two specified Terraform versions.

## Usage

To execute the script, run the following command:

```shell
python3 my_python_script.py <lower_version> <upper_version>
```

Replace `<lower_version>` and `<upper_version>` with the Terraform versions you want to compare. For example:

```shell
python3 my_python_script.py 0.13.4 1.4.6
```

## How It Works

1. The script first reads the "main" changelog from the Terraform GitHub repository (`https://github.com/hashicorp/terraform/blob/main/CHANGELOG.md`).
2. It extracts the list of all minor versions of Terraform from the main changelog.
3. Based on the input lower and upper versions, the script determines the changelogs that need to be parsed.
4. The script loads the required changelog files and compiles data for each release version within the specified upgrade.
5. It analyzes each changelog section to extract bug fixes, enhancements, new features, and other relevant information.
6. The script generates a summary report of each released version and an overall report of the Terraform upgrade as a whole.

## Output

The script generates a detailed and easily digestible summary of the Terraform upgrade. The output includes the following information:

- Total number of unique bug fixes, enhancements, and features implemented.
- Detailed breakdown of changes for each version, categorized by the area of Terraform they concern (e.g., core, config, cli, backend, provisioner, etc.).

## Example Changelog Section

Here's an example of a changelog section for a specific Terraform version:

```
## 1.2.8 (August 24, 2022)

BUG FIXES:

- config: The `flatten` function will no longer panic if given a null value that has been explicitly converted to or implicitly inferred as having a list, set, or tuple type. Previously Terraform would panic in such a situation because it tried to "flatten" the contents of the null value into the result, which is impossible. ([#31675](https://github.com/hashicorp/terraform/issues/31675))
- config: The `tolist`, `toset`, and `tomap` functions, and various automatic conversions that include similar logic, will no longer panic when asked to infer an element type that is convertable from both a tuple type and a list type whose element type is not yet known. ([#31675](https://github.com/hashicorp/terraform/issues/31675))
```

## Dependencies

The script requires the following dependencies:

- Python 3
- requests

To install the dependencies, run the following command:

```shell
pip install -r requirements.txt
```

## License

This project is licensed under the [MIT License](LICENSE).