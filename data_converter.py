import argparse, sys
import pathlib
import pandas as pd
import numpy as np
import csv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def calculate_percentile(df):
    # Calcualte high and low
    percent_low = df.MW.quantile(0.1, interpolation='midpoint')
    percent_high = df.MW.quantile(0.9, interpolation='midpoint')

    # Filter data by each percentile
    low_df = df[df['MW'] <= percent_low]
    high_df = df[df['MW'] >= percent_high]

    # Return the average of each filtered dataset
    return {'min': float(low_df.MW.mean()), 'max': float(high_df.MW.mean())}

def merge_two_dicts(x, y):
    # Combine two dictionaries together
    z = x.copy()
    z.update(y)
    return z

def is_leap_year(year):
    """Determine whether a year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def test_data(df,year):
    error_log = []

    rows_count = df[df.columns[0]].count()

    # Detect if leap year or not
    if year is None: # Set year based on number of rows
        if rows_count == 8784:
            print('Warning! Leap year detected! Calculation will continue using 8784 hours instead of 8760!')
            year = 2004 # example leap year
        elif rows_count == 8760:
            year = 2005 # not a leap year
        else: # Abnormal number or rows
            error_log.append(f'Incorrect number of rows in the input file!\n- Passed: {rows_count}\n- Expected: 8760 or 8784 (leap year)')

    if is_leap_year(year):
        annual_hours = 8784
    else:
        annual_hours = 8760

    if rows_count != annual_hours:
        error_log.append(f'Incorrect number of rows in the input file!\n- Passed: {rows_count}\n- Expected: {annual_hours}')
    if 'MW' not in list(df.columns):
        error_log.append(f"Could not find column 'MW' in input file!\nColumns: {', '.join(list(df.columns))}")
    if 'Hour' not in list(df.columns):
        error_log.append(f"Could not find column 'Hour' in input file!\nColumns: {', '.join(list(df.columns))}")

    if error_log: # Errors occured
        print('\n\n'.join(error_log))
        return False, year

    return True, year

def iterate_months(df,year):
    # Loop through each month/hour permutation, pass values to calculate_percentile, return results
    result = []
    month_range = [datetime(year,1,1) + relativedelta(months=month) for month in range(0,13)]

    # Iterate through each month
    for i, this_month in enumerate(month_range):
        if i+1 == len(month_range):
            break
        next_month = month_range[i+1]

        mon_df = df[ (df['datetime']>=this_month) & (df['datetime']<next_month) ]
        # Iterate through each hour
        for i_hour in range(0,24):
            # Filter month dataframe by each hour
            hour_mon_df = mon_df[mon_df['day_hour']==i_hour]

            # Calcualte the percentiles of the filtered df
            percentile_results = calculate_percentile(hour_mon_df)

            # Add month and hour values to the percentile results
            results_dict = merge_two_dicts({'month': int(this_month.strftime('%m')), 'hour': int(i_hour)}, percentile_results)

            result.append(results_dict)

    return pd.DataFrame(result)

def create_576(df,year):
    df['datetime'] = df['Hour'].apply(lambda hour: datetime(year,1,1) + timedelta(hours=hour-1))
    df['day_hour'] = df['datetime'].dt.hour
    df['month'] = df['datetime'].apply(lambda datetime: int(datetime.strftime('%m')))

    return iterate_months(df,year)

def write_to_csv(df,filepath):
    df.to_csv(filepath,
              index=False,
              quoting=csv.QUOTE_NONNUMERIC)
    print('Wrote output as csv to', filepath)

def config_args():
    parser=argparse.ArgumentParser()

    parser.add_argument('-i','--input',type=pathlib.Path,help='Set input file path',required=False)
    parser.add_argument('-o','--output',type=pathlib.Path,help='Set output file path',required=False)
    parser.add_argument('-y','--year',help='Specify the year, useful for leap years',required=False)
    parser.add_argument('-d','--debug',help='Enable debug printing',action=argparse.BooleanOptionalAction)

    if len(sys.argv)==1: # Print help if no args passed
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()

def main():
    args = config_args()

    if args.input is None: # Create sample dataset
        print('No Input file passed. Using sample dataset!')
        np.random.seed(2024)
        data = {'Hour': range(1, 8760 + 1),
                'MW': np.random.randint(500, 3000, size=(8760,))}
        source_df = pd.DataFrame(data)
    else:
        source_df = pd.read_csv(args.input.resolve())

    calc_year = args.year

    # Test df for proper format
    test_passed, calc_year = test_data(source_df, calc_year)
    if not test_passed:
        print('Dataframe failed test')
        sys.exit(1)

    result_df = create_576(source_df,calc_year)

    if args.debug is not None: print(result_df)

    if args.output is not None:
        pd.options.display.max_rows = 300
        write_to_csv(result_df,args.output.resolve())
    else:
        print('\nNo output file passed!')

if __name__ == "__main__":
    main()

