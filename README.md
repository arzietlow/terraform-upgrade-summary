# Terraform Upgrade Summarizer

This script generates a summary of important details from the changelogs of a Terraform upgrade. It provides an easily digestible output that includes bug fixes, enhancements, and new features implemented between two specified Terraform versions.

## Usage

To execute the script, run the following command:

```shell
python3 summarize_upgrade.py <lower_version> <upper_version>
```

Replace `<lower_version>` and `<upper_version>` with the Terraform versions you want to compare. For example:

```shell
python3 summarize_upgrade.py 0.13.4 1.4.6
```

Version format: Patch numbers are optional, but **major.minor** MUST be present.

## How it works

1. The script first reads the "main" changelog from [the Terraform GitHub repository](https://github.com/hashicorp/terraform/blob/main/CHANGELOG.md).
2. It extracts the list of all minor versions of Terraform from the main changelog.
3. Based on the input lower and upper versions, the script determines which minor version changelogs need to be parsed.
4. The script loads the required changelog files and compiles data for each release version that falls within the specified upgrade.
5. It analyzes each version's section to extract bug fixes, enhancements, new features, and other relevant information.
6. The results are used to create a summary report of each released version and an overall report of the Terraform upgrade.

## Output

The script generates a detailed and easily-digestible summary of the Terraform upgrade. The output includes the following information:

- Total number of unique bug fixes, enhancements, and features implemented.
- Detailed breakdown of changes for each version, categorized by the area of Terraform they concern (e.g., core, config, cli, backend, provisioner, etc.) when applicable.

## Dependencies

The script requires the following dependencies:

- Python 3
- Requests
- Semantic-version
- Pyfiglet
- Tabulate

## Limitations

The Terraform changelogs do not adhere to any strict formatting rules, so this project may stop working if Hashicorp changes their changelog format. The project also does not guarantee that no details will be missed by the scan.
Additionally, this project is NOT useful for summarizing upgrades that start from a version prior to 0.12.0, as the changelog format appears to have been standardized only from that release onwards.

## License

This project is licensed under the [MIT License](LICENSE).
