## Part 1: Data Loading and Cleaning
import pandas as pd
import numpy as np
import re
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Load raw log lines from file
def load_log_file(filepath):
    with open(filepath, 'r', encoding='latin1') as f:
        lines = f.readlines()
    return lines

# Provide the correct file path
log_lines = load_log_file("C:/Users/Dell/Downloads/calgary_access_log")

print(f"Total log entries: {len(log_lines)}")
print(log_lines[:3])

# Regex pattern to parse logs
log_pattern = re.compile(
    r'(?P<host>\S+) (?P<identity>\S+) (?P<user>\S+) \[(?P<time>.+?)\] '
    r'"(?P<request>.+?)" (?P<status>\d{3}) (?P<size>\S+)'
)

# Parse lines using regex
def parse_logs(log_lines):
    parsed_data = []
    for line in log_lines:
        match = log_pattern.match(line)
        if match:
            entry = match.groupdict()
            parsed_data.append(entry)
    return pd.DataFrame(parsed_data)

df = parse_logs(log_lines)
print("\nParsed DataFrame preview:")
print(df.head())

# Convert time column to datetime
df['datetime'] = pd.to_datetime(df['time'], format='%d/%b/%Y:%H:%M:%S %z', errors='coerce')

# Clean 'size' column
df['size'] = df['size'].replace('-', '0').astype(int)

# Extract method, endpoint, and protocol from request
df[['method', 'endpoint', 'protocol']] = df['request'].str.extract(r'(\w+)\s+([^\s]+)\s+(HTTP/\d\.\d)')

# Drop columns no longer needed
df.drop(columns=['time', 'request'], inplace=True)

print("\nCleaned DataFrame preview:")
print(df.head())

# Show missing values
print("\nMissing values per column:\n", df.isnull().sum())

# Show info
print("\nDataFrame info:")
print(df.info())

# Drop rows where method/endpoint/protocol are missing
df_cleaned = df.dropna(subset=['method', 'endpoint', 'protocol']).copy()

print(f"\n Cleaned DataFrame shape: {df_cleaned.shape}")

# Convert datetime again for cleaned data (with utc=True)
df_cleaned['datetime'] = pd.to_datetime(df_cleaned['datetime'], utc=True)

# Set datetime as index
df_cleaned.set_index('datetime', inplace=True)

# Save cleaned data to CSV
df_cleaned.to_csv('cleaned_log_data.csv')
print("\n Cleaned data saved to 'cleaned_log_data.csv'")

## Part 2: Analysis Questions
### Q1: Count of total log records
def total_log_records() -> int:
    """
    Q1: Count of total log records.

    Objective:
        Determine the total number of HTTP log entries in the dataset.
        Each line in the log file represents one HTTP request.

    Returns:
        int: Total number of log entries.
    """
    return len(df_cleaned)


# Test the function
answer1 = total_log_records()
print("Answer 1:")
print(answer1)

### Q2: Count of unique hosts
def unique_host_count() -> int:
    """
    Q2: Count of unique hosts.

    Objective:
        Determine how many distinct hosts accessed the server.

    Returns:
        int: Number of unique hosts.
    """

    # TODO: Implement logic to count unique hosts

    return df_cleaned['host'].nunique()


answer2 = unique_host_count()
print("Answer 2:")
print(answer2)

### Q3: Date-wise unique filename counts
def datewise_unique_filename_counts() -> dict[str, int]:
    """
    Q3: Date-wise unique filename counts.

    Objective:
        For each date, count the number of unique filenames that accessed the server.
        The date should be in 'dd-MMM-yyyy' format (e.g., '01-Jul-1995').

    Returns:
        dict: A dictionary mapping each date to its count of unique filenames.
              Example: {'01-Jul-1995': 123, '02-Jul-1995': 150}
    """

    # TODO: Implement logic for date-wise unique filename counts

    df_cleaned['date_str'] = df_cleaned.index.strftime('%d-%b-%Y')

    # Group by date and count unique endpoints (filenames)
    result = (
        df_cleaned.groupby('date_str')['endpoint']
        .nunique()
        .to_dict()
    )
    
    return result


answer3 = datewise_unique_filename_counts()
print("Answer 3:")
print(answer3)

### Q4: Number of 404 response codes
def count_404_errors() -> int:
    """
    Q4: Number of 404 response codes.

    Objective:
        Count how many times the HTTP 404 Not Found status appears in the logs.

    Returns:
        int: Number of 404 errors.
    """

    # TODO: Implement logic to count 404 errors

    return (df_cleaned['status'] == '404').sum()


answer4 = count_404_errors()
print("Answer 4:")
print(answer4)

### Q5: Top 15 filenames with 404 responses
def top_15_filenames_with_404() -> list[tuple[str, int]]:
    """
    Q5: Top 15 filenames with 404 responses.

    Objective:
        Identify which requested URLs most frequently resulted in a 404 error.
        Return the top 15 filenames sorted by frequency.

    Returns:
        list: A list of tuples (filename, count), sorted by count in descending order.
              Example: [('index.html', 200), ...]
    """

    # TODO: Implement logic to find top 15 filenames with 404

    error_404_df = df_cleaned[df_cleaned['status'] == '404']
    top_endpoints = (
        error_404_df['endpoint']
        .value_counts()
        .head(15)
        .items()
    )
    return list(top_endpoints)


answer5 = top_15_filenames_with_404()
print("Answer 5:")
print(answer5)

### Q6: Top 15 file extension with 404 responses
def top_15_ext_with_404() -> list[tuple[str, int]]:
    """
    Q6: Top 15 file extensions with 404 responses.

    Objective:
        Find which file extensions generated the most 404 errors.
        Return the top 15 sorted by number of 404s.

    Returns:
        list: A list of tuples (extension, count), sorted by count in descending order.
              Example: [('html', 45), ...]
    """

    # TODO: Implement logic to find top 15 extensions with 404

    error_404_df = df_cleaned[df_cleaned['status'] == '404']
    
    # Extract extensions from endpoints
    error_404_df['ext'] = error_404_df['endpoint'].str.extract(r'\.([a-zA-Z0-9]+)$')[0].str.lower()
    
    # Drop NaN and count
    top_ext = error_404_df['ext'].dropna().value_counts().head(15)
    
    return list(top_ext.items())


answer6 = top_15_ext_with_404()
print("Answer 6:")
print(answer6)

### Q7: Total bandwidth transferred per day for the month of July 1995
def total_bandwidth_per_day() -> dict[str, int]:
    """
    Q7: Total bandwidth transferred per day for the month of July 1995.

    Objective:
        Sum the number of bytes transferred per day.
        Skip entries where the byte field is missing or '-'.

    Returns:
        dict: A dictionary mapping each date to total bytes transferred.
              Example: {'01-Jul-1995': 123456789, ...}
    """

    # TODO: Implement logic to compute total bandwidth per day

    july_df = df_cleaned[
        (df_cleaned.index.month == 7) & (df_cleaned.index.year == 1995)
    ]
    
    bandwidth_by_date = july_df.groupby(july_df.index.strftime('%d-%b-%Y'))['size'].sum()
    
    return bandwidth_by_date.to_dict()

answer7 = total_bandwidth_per_day()
print("Answer 7:")
print(answer7)

### Q8: Hourly request distribution
def hourly_request_distribution() -> dict[int, int]:
    """
    Q8: Hourly request distribution.

    Objective:
        Count the number of requests made during each hour (00 to 23).
        Useful for understanding traffic peaks.

    Returns:
        dict: A dictionary mapping hour (int) to request count.
              Example: {0: 120, 1: 90, ..., 23: 80}
    """

    # TODO: Implement logic for hourly distribution

    hourly_counts = df_cleaned.groupby(df_cleaned.index.hour).size()
    
    return hourly_counts.to_dict()


answer8 = hourly_request_distribution()
print("Answer 8:")
print(answer8)

### Q9: Top 10 most requested filenames
def top_10_most_requested_filenames() -> list[tuple[str, int]]:
    """
    Q9: Top 10 most requested filenames.

    Objective:
        Identify the most commonly requested URLs (irrespective of status code).

    Returns:
        list: A list of tuples (filename, count), sorted by count in descending order.
                Example: [('index.html', 500), ...]
    """

    # TODO: Implement logic to find top 10 most requested filenames

    top_files = df_cleaned['endpoint'].value_counts().head(10)
    
    return list(top_files.items())


answer9 = top_10_most_requested_filenames()
print("Answer 9:")
print(answer9)

### Q10: HTTP response code distribution
def response_code_distribution() -> dict[int, int]:
    """
    Q10: HTTP response code distribution.

    Objective:
        Count how often each HTTP status code appears in the logs.

    Returns:
        dict: A dictionary mapping HTTP status codes (as int) to their frequency.
              Example: {200: 150000, 404: 3000}
    """

    # TODO: Implement logic for response code counts

    return df_cleaned['status'].astype(int).value_counts().sort_index().to_dict()


answer10 = response_code_distribution()
print("Answer 10:")
print(answer10)

