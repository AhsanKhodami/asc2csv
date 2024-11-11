
# EyeLink ASC to CSV Conversion Script
**Author**: [M. Ahsan Khodami](https://khodami.site)  
**Google Scholar**: [Profile](https://scholar.google.com/citations?user=WCqPnS4AAAAJ&hl=en)  
**Related Technology**: [EyeLink by SR Research](https://www.sr-research.com/)

# Purpose of this code

Converting EyeLink eye-tracker data from [ASC (ASCII) format](https://www.sr-research.com/support/thread-7675.html) to CSV (Comma-Separated Values) format offers several advantages that enhance data analysis and integration:

**1. Enhanced Compatibility with Data Analysis Tools**

While ASC files are plain text, their structure can be complex and inconsistent, making them less straightforward to process. CSV files, on the other hand, are widely supported by various data analysis software, including Python, R, MATLAB, and Excel <font color='red'>, which is highly not recommended </font>. This compatibility facilitates efficient data manipulation, statistical analysis, and visualization.

![Screenshot of an ASCII file](https://github.com/AhsanKhodami/eyelink-eyetracker-ascii-convert-to-csv-code/blob/main/asc%20file%20format%20screen.png?raw=true)

**2. Streamlined Data Processing**

CSV files provide a tabular format that simplifies data parsing and processing. This structure allows for easier implementation of automated scripts and pipelines, reducing the potential for errors and increasing the reproducibility of analyses.

**3. Improved Data Integration**

In research involving multimodal data—such as combining eye-tracking with EEG or behavioral data—CSV files serve as a common format that simplifies the merging and synchronization of datasets from different sources. This integration is crucial for comprehensive analyses and interpretations. Also, the CSV format is free to change, while using libraries, e.g., MNE or other software, does not freely guarantee accessing data due to internal processing rather than explicit processing.

## Purpose of this script

This script is designed to convert EyeLink eye-tracker data from ASC to CSV, which is more suitable for further data analysis. It processes the ASC file to extract trial data, including events such as blinks, saccades, and fixations and exports the organized data to a CSV file.

## Code Overview and Explanation

### Importing Libraries

```python
import pandas as pd
```

This section ensures using the `pandas` library, which is essential for handling data structures and operations like reading, merging, and exporting data in DataFrame format.

### Utility Function: `safe_float`

```python
def safe_float(value):
    try:
        return 0.0 if value == '.' else float(value)
    except ValueError:
        return 0.0
```

**Explanation**:  
This function safely converts a value to a float. If the value is `'.'`, which can appear in eye-tracking data as a placeholder for missing or unrecorded values, it returns `0.0`. This function helps in cleaning and normalizing data.

### Main Function: `process_asc_file`

#### Reading the ASC File

```python
def process_asc_file(file_path, output_csv_path):
    with open(file_path, 'r') as file:
        file_content = file.readlines()
```

**Explanation**:  
This section reads the content of the ASC file and stores each line in a list called `file_content` for processing. This approach enables efficient iteration over each line to parse and extract relevant data.

#### Initializing Variables for Data Collection

```python
    all_samples = []
    all_events = []
    trial_start_time = None
    current_trial = None
    recording_data = False
    current_message = ''
```

**Explanation**:  
The variables `all_samples` and `all_events` are initialized to collect sample and event data. Other variables like `trial_start_time`, `current_trial`, `recording_data`, and `current_message` help track the state of trial processing and manage data within a trial.

### Processing Lines from the ASC File

#### Detecting the Start of a Trial

```python
    for line in file_content:
        line = line.strip()
        if 'MSG' in line and 'TRIALID' in line:
            try:
                current_trial = int(line.split()[-1])
                trial_start_time = float(line.split()[1])
                recording_data = True
            except ValueError:
                continue
            continue
```

**Explanation**:  
This section detects the start of a trial by searching for lines with `'MSG'` and `'TRIALID'`. It extracts the trial number and start time to signal that data recording should begin.

#### Handling Message Lines

```python
        if 'MSG' in line:
            parts = line.split()
            msg_timestamp = float(parts[1])
            current_message = ' '.join(parts[2:])
            relative_time = max(0.0, msg_timestamp - trial_start_time) if trial_start_time is not None else 0.0
            all_events.append([current_trial, msg_timestamp, relative_time, '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Message', current_message])
            continue
```

**Explanation**:  
This block processes message lines, extracts timestamps and message content, calculates the relative time based on the trial start, and appends this data to `all_events`.

#### Extracting Sample Data

```python
        if recording_data and current_trial is not None:
            if len(line.split()) >= 6 and '.' in line.split()[0]:
                line_data = line.split()
                timestamp = float(line_data[0])
                relative_time = max(0.0, timestamp - trial_start_time) if trial_start_time else 0.0
                gaze_x = safe_float(line_data[1])
                gaze_y = safe_float(line_data[2])
                pupil_size = safe_float(line_data[3])
                veloc_x = safe_float(line_data[4])
                veloc_y = safe_float(line_data[5])
                all_samples.append([current_trial, timestamp, relative_time, gaze_x, gaze_y, pupil_size, veloc_x, veloc_y, '', '', '', '', '', '', '', '', '', current_message])
```

**Explanation**:  
This section processes continuous sample data lines, extracting timestamp, gaze coordinates, pupil size, and velocities. It calculates the relative time and appends this data to `all_samples`.

### Handling Specific Events

#### Blink Events (`EBLINK`)

```python
            elif line.startswith('EBLINK'):
                line_data = line.split()
                eye = line_data[1]
                start_time = float(line_data[2])
                end_time = float(line_data[3])
                duration = float(line_data[4])
                relative_time = max(0.0, start_time - trial_start_time) if trial_start_time else 0.0
                all_events.append([current_trial, start_time, relative_time, eye, start_time, end_time, duration, '', '', '', '', '', '', '', '', '', '', 'Blink', current_message])
```

**Explanation**:  
This block detects and processes `EBLINK` events, extracting information such as the eye involved, start and end times, and duration. It appends the data to `all_events`.

#### Saccade Events (`ESACC`)

```python
            elif line.startswith('ESACC'):
                line_data = line.split()
                eye = line_data[1]
                start_time = float(line_data[2])
                end_time = float(line_data[3])
                duration = float(line_data[4])
                start_x = safe_float(line_data[5])
                start_y = safe_float(line_data[6])
                end_x = safe_float(line_data[7])
                end_y = safe_float(line_data[8])
                amplitude = safe_float(line_data[9])
                peak_velocity = safe_float(line_data[10])
                avg_velocity = (peak_velocity + safe_float(line_data[4])) / 2 if peak_velocity else 0.0
                relative_time = max(0.0, start_time - trial_start_time) if trial_start_time else 0.0
                all_events.append([current_trial, start_time, relative_time, eye, start_time, end_time, duration, start_x, start_y, end_x, end_y, '', '', '', amplitude, peak_velocity, avg_velocity, 'Saccade', current_message])
```

**Explanation**:  
The script identifies `ESACC` events, extracts detailed information (e.g., eye involved, start and end times, coordinates, amplitude, and velocities), and appends this to `all_events`.

#### Fixation Events (`EFIX`)

```python
            elif line.startswith('EFIX'):
                line_data = line.split()
                eye = line_data[1]
                start_time = float(line_data[2])
                end_time = float(line_data[3])
                duration = float(line_data[4])
                avg_x = safe_float(line_data[5])
                avg_y = safe_float(line_data[6])
                avg_pupil = safe_float(line_data[7])
                relative_time = max(0.0, start_time - trial_start_time) if trial_start_time else 0.0
                all_events.append([current_trial, start_time, relative_time, eye, start_time, end_time, duration, '', '', '', '', avg_x, avg_y, avg_pupil, '', '', '', 'Fixation', current_message])
```

**Explanation**:  
This section processes `EFIX` events to capture fixation details, including the average gaze position and pupil size, and appends this data to `all_events`.

### Creating and Merging DataFrames

#### DataFrame Creation

```python
    df_samples = pd.DataFrame(all_samples, columns=['Trial', 'Timestamp', 'Trial Time', 'Gaze X', 'Gaze Y', 'Pupil Size', 'Veloc X', 'Veloc Y', 'Eye', 'Start Time', 'End Time', 'Duration', 'Start X', 'Start Y', 'End X', 'End Y', 'Event Type', 'Message'])
    df_events = pd.DataFrame(all_events, columns=['Trial', 'Timestamp', 'Trial Time', 'Eye', 'Start Time', 'End Time', 'Duration', 'Start X', 'Start Y', 'End X', 'End Y', 'Avg X','Avg Y', 'Mean Pupil Size', 'Amplitude', 'Peak Velocity', 'Average Velocity', 'Event Type', 'Message'])
```

**Explanation**:  
Two pandas DataFrames, `df_samples` and `df_events`, are created with appropriate column names to organize the sample and event data collected earlier.

#### Merging and Cleaning Data

```python
    df_combined = pd.merge(df_samples, df_events, on=['Trial', 'Timestamp', 'Trial Time'], how='outer', suffixes=('_sample', '_event'))
    for col in ['Eye', 'Start Time', 'End Time', 'Duration', 'Start X', 'Start Y', 'End X', 'End Y', 'Avg X', 'Avg Y', 'Mean Pupil Size', 'Amplitude', 'Peak Velocity', 'Average Velocity', 'Event Type', 'Message']:
        if col + '_event' in df_combined.columns:
            df_combined[col] = df_combined[col + '_event'].combine_first(df_combined[col + '_sample'])
            df_combined.drop([col + '_sample', col + '_event'], axis=1, inplace=True)
    df_combined.sort_values(by=['Trial', 'Timestamp'], inplace=True)
    df_combined.to_csv(output_csv_path, index=False)
```

**Explanation**:  
The script merges `df_samples` and `df_events` using an outer join, ensuring all data is included. It fills missing event details in sample rows with corresponding event data and sorts the combined DataFrame by `Trial` and `Timestamp`. Finally, it exports the processed data to a CSV file.

### Example Usage

```python
file_path = 'obtained_data.asc'  # Replace with the path to your ASC file
output_csv_path = 'obtained_data.csv'  # Replace with your desired output file path
process_asc_file(file_path, output_csv_path)
```
