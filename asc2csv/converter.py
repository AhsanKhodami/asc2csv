import pandas as pd

def safe_float(value):
    """Converts a value to float, returns 0.0 if the value is a '.'"""
    try:
        return 0.0 if value == '.' else float(value)
    except ValueError:
        return 0.0

def process_asc_file(input_file_path, output_csv_path, header=True):
    """
    Processes an EyeLink .asc file and converts it to a .csv file format.

    This function reads an EyeLink .asc file containing trial data, including gaze samples,
    saccades, blinks, and fixation events, and converts it into a structured CSV file.
    It extracts relevant columns, handles various event types, and ensures data is
    well-organized with trial-relative timestamps.

    Parameters:
    ----------
    input_file_path : str
        The path to the input .asc file to be processed.
    output_csv_path : str
        The path to save the output .csv file.
    header : bool, optional (default=True)
        Whether to include a header row in the output CSV file.

    Returns:
    -------
    None
        The function saves the processed data directly to the specified output CSV path.

    Example:
    -------
    process_asc_file('example_input.asc', 'example_output.csv', header=True)
    
    Notes:
    -----
    - The function handles events like 'MSG', 'EBLINK', 'ESACC', and 'EFIX'.
    - It aligns timestamps relative to the start of each trial to facilitate temporal analysis.
    - Missing data is handled by combining columns from samples and event data where applicable.
    """
    with open(input_file_path, 'r') as file:
        file_content = file.readlines()

    # Initialize the final list to collect all trials' data
    all_samples = []
    all_events = []
    
    trial_start_time = None
    current_trial = None
    recording_data = False
    current_message = ''

    # Process file line-by-line
    for line in file_content:
        line = line.strip()

        # Detect the start of a new trial using TRIALID
        if 'MSG' in line and 'TRIALID' in line:
            try:
                current_trial = int(line.split()[-1])
                trial_start_time = float(line.split()[1])
                recording_data = True
            except ValueError:
                continue  # Skip this line if the trial number is invalid
            continue

        if 'MSG' in line:
            parts = line.split()
            msg_timestamp = float(parts[1])
            current_message = ' '.join(parts[2:])
            relative_time = max(0.0, msg_timestamp - trial_start_time) if trial_start_time else 0.0
            all_events.append([current_trial, msg_timestamp, relative_time, '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Message', current_message])
            continue

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

            elif line.startswith('EBLINK'):
                line_data = line.split()
                eye = line_data[1]
                start_time = float(line_data[2])
                end_time = float(line_data[3])
                duration = float(line_data[4])
                relative_time = max(0.0, start_time - trial_start_time) if trial_start_time else 0.0
                all_events.append([current_trial, start_time, relative_time, eye, start_time, end_time, duration, '', '', '', '', '', '', '', '', '', '', 'Blink', current_message])

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

    # Create DataFrames
    df_samples = pd.DataFrame(all_samples, columns=['Trial', 'Timestamp', 'Trial Time', 'Gaze X', 'Gaze Y', 'Pupil Size', 'Veloc X', 'Veloc Y', 'Eye', 'Start Time', 'End Time', 'Duration', 'Start X', 'Start Y', 'End X', 'End Y', 'Event Type', 'Message'])
    df_events = pd.DataFrame(all_events, columns=['Trial', 'Timestamp', 'Trial Time', 'Eye', 'Start Time', 'End Time', 'Duration', 'Start X', 'Start Y', 'End X', 'End Y', 'Avg X', 'Avg Y', 'Mean Pupil Size', 'Amplitude', 'Peak Velocity', 'Average Velocity', 'Event Type', 'Message'])

    # Merge events into samples
    df_combined = pd.merge(df_samples, df_events, on=['Trial', 'Timestamp', 'Trial Time'], how='outer', suffixes=('_sample', '_event'))

    for col in ['Eye', 'Start Time', 'End Time', 'Duration', 'Start X', 'Start Y', 'End X', 'End Y', 'Avg X', 'Avg Y', 'Mean Pupil Size', 'Amplitude', 'Peak Velocity', 'Average Velocity', 'Event Type', 'Message']:
        if col + '_event' in df_combined.columns:
            df_combined[col] = df_combined[col + '_event'].combine_first(df_combined[col + '_sample'])
            df_combined.drop([col + '_sample', col + '_event'], axis=1, inplace=True)

    df_combined.sort_values(by=['Trial', 'Timestamp'], inplace=True)
    df_combined.to_csv(output_csv_path, index=False, header=header)

    print(f"Conversion completed: {output_csv_path}")
