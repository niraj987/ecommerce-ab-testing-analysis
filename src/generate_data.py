import os
import numpy as np
import pandas as pd

def generate_experiment_data(output_path, seed=42):
    """
    Simulates A/B testing data for an e-commerce website.
    
    Parameters:
    - output_path (str): File path to save the simulated CSV.
    - seed (int): Random seed for reproducibility.
    """
    np.random.seed(seed)
    
    # 1. Define experiment parameters
    n_control = 10000
    n_treatment = 10000
    total_users = n_control + n_treatment
    
    # Target conversion counts matching business problem statement:
    # Lift of +2.52% on 10k users approx +252 extra conversions
    # Control conversion rate = 5.0% -> 500 conversions
    # Treatment conversion rate = 7.52% -> 752 conversions
    conversions_control = 500
    conversions_treatment = 752
    
    # 2. Generate conversion arrays
    converted_control = np.zeros(n_control, dtype=int)
    converted_control[:conversions_control] = 1
    
    converted_treatment = np.zeros(n_treatment, dtype=int)
    converted_treatment[:conversions_treatment] = 1
    
    # Shuffle conversions within groups
    np.random.shuffle(converted_control)
    np.random.shuffle(converted_treatment)
    
    # 3. Create DataFrames for each group
    df_control = pd.DataFrame({
        'group': ['control'] * n_control,
        'converted': converted_control
    })
    
    df_treatment = pd.DataFrame({
        'group': ['treatment'] * n_treatment,
        'converted': converted_treatment
    })
    
    # Combine groups
    df = pd.concat([df_control, df_treatment], ignore_index=True)
    
    # 4. Generate unique user IDs
    # Shuffle user IDs to mix them across groups
    user_ids = [f"USR_{i:05d}" for i in range(1, total_users + 1)]
    np.random.shuffle(user_ids)
    df['user_id'] = user_ids
    
    # 5. Generate random timestamps over a 14-day period
    # Let's assume the experiment ran from 2026-06-01 to 2026-06-14
    start_time = pd.Timestamp('2026-06-01 00:00:00')
    end_time = pd.Timestamp('2026-06-14 23:59:59')
    
    # Generate random seconds offset
    max_seconds = int((end_time - start_time).total_seconds())
    random_seconds = np.random.randint(0, max_seconds, size=total_users)
    
    df['timestamp'] = start_time + pd.to_timedelta(random_seconds, unit='s')
    
    # 6. Sort chronologically to represent real-world log flow
    df = df.sort_values(by='timestamp').reset_index(drop=True)
    
    # Reorder columns for clean presentation
    df = df[['user_id', 'timestamp', 'group', 'converted']]
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Successfully generated dataset at: {output_path}")
    print(f"Total Rows: {len(df)}")
    print(df['group'].value_counts())
    print("\nConversion Counts & Rates by Group:")
    summary = df.groupby('group')['converted'].agg(['sum', 'count', 'mean'])
    summary.columns = ['Conversions', 'Total Users', 'Conversion Rate']
    print(summary)

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(script_dir)
    data_file_path = os.path.join(workspace_dir, 'data', 'ab_data.csv')
    generate_experiment_data(data_file_path)
