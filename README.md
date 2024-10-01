# Hourly Power Data to Standardized 576 Format Converter

## Overview

This program processes hourly power data and converts it into a standardized 576 format. It calculates statistical percentiles for each hour of each month based on input power data, ensuring that the results are reliable and formatted correctly for further analysis or reporting.

## Features

- **Input Data Handling**: Reads hourly power data from a CSV file or generates a sample dataset.
- **Leap Year Detection**: Automatically detects if the provided data corresponds to a leap year and adjusts calculations accordingly.
- **Statistical Calculation**: Computes the 10th and 90th percentiles of power data for each hour across all months.
- **Output Format**: Writes the processed data to a new CSV file in the standardized 576 format.

## Requirements

- Python 3.x
- Pandas
- NumPy
- Dateutil

You can install the required libraries using pip:

```bash
pip install -r requirements.txt
```

## Usage

To run the program, use the following command:
```bash
python convert_to_576.py -i <input_file.csv> -o <output_file.csv> -y <year> -d
```
### Arguments

- `-i`, `--input`: Specify the input CSV file path containing hourly power data. The file should have the columns `Hour` and `MW`.
- `-o`, `--output`: Specify the output file path for the converted data.
- `-y`, `--year`: **(Optional)** Specify the year of the data, which is useful for identifying leap years.
- `-d`, `--debug`: **(Optional)** Enable debug printing for troubleshooting purposes.

### Example

```bash
python convert_to_576.py -i power_8760_data.csv -o converted_576_data.csv -y 2023
```

If no input file is provided, the program will generate a sample dataset.

## Functionality

- **Data Validation**: The program checks for the correct number of rows (8760 for non-leap years and 8784 for leap years) and ensures that required columns (`MW` and `Hour`) are present.
- **Percentile Calculation**: It calculates the 10th and 90th percentiles for power values for each hour of each month.
- **Output Generation**: The results are saved in a CSV format, making it easy to import into other tools or systems.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

Feel free to modify any sections to better fit your project’s specifics!
