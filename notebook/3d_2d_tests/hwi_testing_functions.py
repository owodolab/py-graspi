import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from collections import defaultdict
import os  # Added to extract file names


def format_number(value):
    """Format large numbers into readable strings (e.g., 1.2K, 3.4M)."""
    if value >= 1_000_000:
        return f'{value/1_000_000:.1f}M'
    elif value >= 1_000:
        return f'{value/1_000:.1f}K'
    return f'{value:.0f}'


def group_files_by_pattern(files):
    """Group file names by replacing numeric values with a placeholder (#)."""
    pattern_groups = defaultdict(list)
    for file in files:
        pattern = re.sub(r'\d+(?:\.\d+)?', '#', file)
        pattern_groups[pattern].append(file)
    return pattern_groups


def extract_numbers(filename):
    """Extract numbers from a filename for sorting."""
    return tuple(map(int, re.findall(r'\d+', filename)))


def plot_total_execution_and_memory_compare(csv_file1, csv_file2):
    """
    Compare total execution time and peak memory usage from two CSV files.
    Line plots are generated for each pattern group.
    """
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)

    label1 = os.path.basename(csv_file1)
    label2 = os.path.basename(csv_file2)

    for df in [df1, df2]:
        df['total_execution_time'] = df['descriptor_time'] + df['graph_time']
        df['peak_memory_usage'] = df[['graph_mem', 'descriptor_mem']].max(axis=1)

    pattern_groups = group_files_by_pattern(df1['Test File'])

    for pattern, files in pattern_groups.items():
        subset1 = df1[df1['Test File'].isin(files)].copy()
        subset2 = df2[df2['Test File'].isin(files)].copy()

        subset1['sort_key'] = subset1['Test File'].apply(extract_numbers)
        subset2['sort_key'] = subset2['Test File'].apply(extract_numbers)
        subset1.sort_values('sort_key', inplace=True)
        subset2.sort_values('sort_key', inplace=True)

        sorted_test_files = sorted(files, key=extract_numbers)

        plt.figure(figsize=(12, 10))

        # Execution time comparison
        ax1 = plt.subplot(2, 1, 1)
        ax1.plot(sorted_test_files, subset1['total_execution_time'], marker='o', linestyle='-', color='blue', label=label1)
        ax1.plot(sorted_test_files, subset2['total_execution_time'], marker='o', linestyle='-', color='red', label=label2)
        plt.xlabel('Test Files')
        plt.ylabel('Time (s)')
        plt.title(f'Total Execution Time Comparison - {pattern}')
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.grid(True)

        # Memory usage comparison
        ax2 = plt.subplot(2, 1, 2)
        ax2.plot(sorted_test_files, subset1['peak_memory_usage'], marker='s', linestyle='-', color='green', label=label1)
        ax2.plot(sorted_test_files, subset2['peak_memory_usage'], marker='s', linestyle='-', color='purple', label=label2)
        plt.xlabel('Test Files')
        plt.ylabel('Memory Usage (bytes)')
        plt.title(f'Peak Memory Usage Comparison - {pattern}')
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.grid(True)

        plt.tight_layout(pad=2.0)
        plt.show()


def plot_stepwise_execution_and_memory_compare(csv_file1, csv_file2):
    """
    Compare stepwise execution time and memory usage for Graph and Descriptor
    between two CSV files, using bar plots for each file.
    """
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)

    label1 = os.path.basename(csv_file1)
    label2 = os.path.basename(csv_file2)

    pattern_groups = group_files_by_pattern(df1['Test File'])

    for pattern, files in pattern_groups.items():
        subset1 = df1[df1['Test File'].isin(files)].copy()
        subset2 = df2[df2['Test File'].isin(files)].copy()

        subset1['size'] = subset1['Test File'].str.extract(r'(\d+)').astype(float)
        subset2['size'] = subset2['Test File'].str.extract(r'(\d+)').astype(float)

        subset1.sort_values('size', inplace=True)
        subset2.sort_values('size', inplace=True)

        num_files = len(subset1)
        fig, axes = plt.subplots(num_files, 2, figsize=(12, num_files * 4), squeeze=False)

        bar_width = 0.4
        x = np.array([0, 1])

        for i, ((_, row1), (_, row2)) in enumerate(zip(subset1.iterrows(), subset2.iterrows())):
            # Execution time comparison
            ax_time = axes[i, 0]
            times1 = [row1['graph_time'], row1['descriptor_time']]
            times2 = [row2['graph_time'], row2['descriptor_time']]
            ax_time.bar(x - 0.2, times1, bar_width, color=['blue', 'red'], label=label1)
            ax_time.bar(x + 0.2, times2, bar_width, color=['cyan', 'orange'], label=label2)
            ax_time.set_xticks(x)
            ax_time.set_xticklabels(['Graph', 'Descriptor'])
            ax_time.set_title(f'Time - {row1["Test File"]}')
            ax_time.set_ylabel('Time (s)')
            ax_time.legend()
            ax_time.grid(True)

            # Memory usage comparison
            ax_mem = axes[i, 1]
            mems1 = [row1['graph_mem'], row1['descriptor_mem']]
            mems2 = [row2['graph_mem'], row2['descriptor_mem']]
            ax_mem.bar(x - 0.2, mems1, bar_width, color=['green', 'purple'], label=label1)
            ax_mem.bar(x + 0.2, mems2, bar_width, color=['lightgreen', 'pink'], label=label2)
            ax_mem.set_xticks(x)
            ax_mem.set_xticklabels(['Graph', 'Descriptor'])
            ax_mem.set_title(f'Memory - {row1["Test File"]}')
            ax_mem.set_ylabel('Memory Usage (bytes)')
            ax_mem.legend()
            ax_mem.grid(True)

        plt.tight_layout()
        plt.show()