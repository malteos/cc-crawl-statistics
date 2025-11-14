"""This is vibe coded with Claude code.

> Reproduce this plot (monthly.png from crawl-statistics) with matplotlib. Make sure that both plots are visually the same.

"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import re

input_path = "monthly.csv"
output_path = "monthly_new.png"
df = pd.read_csv(input_path)

print(df)

# Generate a plot and save it to output_path
def parse_crawl_date(crawl_name):
    """Parse date from crawl name like CC-MAIN-2024-46 or CC-MAIN-2008-2009"""
    if '2008-2009' in crawl_name:
        return datetime(2009, 6, 1)  # Mid-point
    elif '2009-2010' in crawl_name:
        return datetime(2010, 6, 1)  # Mid-point
    else:
        # Extract year and week/month number
        match = re.search(r'CC-MAIN-(\d{4})-(\d+)', crawl_name)
        if match:
            year = int(match.group(1))
            week_or_month = int(match.group(2))

            # Convert week number to approximate month
            if week_or_month <= 12:
                month = week_or_month
            else:
                month = max(1, min(12, int(week_or_month / 4.33)))

            return datetime(year, month, 15)  # Mid-month
    return datetime(2020, 1, 1)  # Fallback

# Parse dates and create datetime column
df['date'] = df['crawl'].apply(parse_crawl_date)
df = df.sort_values('date')

# Set up ggplot2-like minimal theme with larger fonts
plt.style.use('default')
plt.rcParams.update({
    'font.size': 18,  # Much larger base font size
    'axes.linewidth': 1.5,
    'axes.spines.left': True,
    'axes.spines.bottom': True,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.axisbelow': True,
    'axes.grid': True,
    'axes.grid.axis': 'both',
    'grid.linewidth': 1.0,
    'grid.color': '#E6E6E6',  # Gray grid lines
    'axes.facecolor': 'white',  # White background
    'figure.facecolor': 'white',
    'xtick.bottom': True,
    'xtick.top': False,
    'ytick.left': True,
    'ytick.right': False,
    'xtick.direction': 'out',
    'ytick.direction': 'out'
})

# Create the plot with exact dimensions to match original 2100x2100 resolution
# Calculate figsize to get 2100x2100 pixels at 150 DPI: 2100/150 = 14 inches
fig, ax = plt.subplots(figsize=(14, 14))

# ggplot2 default colors (hue scale)
colors = ['#F8766D', '#00BA38', '#619CFF']  # Red, Green, Blue from ggplot2

# Plot the three metrics with significantly larger line thickness and points
line_width = 2.5  # Much thicker lines to match original
marker_size = 8   # Much larger points to match original

ax.plot(df['date'], df['digest estim.'], 'o-', color=colors[0], label='digest estim.',
        linewidth=line_width, markersize=marker_size)
ax.plot(df['date'], df['page'], 'o-', color=colors[1], label='page',
        linewidth=line_width, markersize=marker_size)
ax.plot(df['date'], df['url'], 'o-', color=colors[2], label='url',
        linewidth=line_width, markersize=marker_size)

# Format the plot to match ggplot2 theme_minimal with larger fonts
ax.set_title('Crawl Size', fontsize=24, fontweight='normal', pad=30, loc='left')
ax.set_xlabel('')
ax.set_ylabel('Pages / Unique Items', fontsize=20)

# Set y-axis to scientific notation with ggplot2-style formatting
ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e9:.0f}e+09' if x != 0 else '0'))

# Set aspect ratio to match ggplot2 (ratio=0.9 from the original code)
ax.set_aspect(1/ax.get_data_ratio() * 0.9)

# Set y-axis limits and reduce number of ticks
ax.set_ylim(1e9, 4e9)

# Reduce the number of axis ticks to match original
from matplotlib.ticker import MaxNLocator, FixedLocator
from matplotlib.dates import YearLocator, DateFormatter
import numpy as np
ax.xaxis.set_major_locator(YearLocator(base=5))  # Show years every 5 years (2010, 2015, 2020, 2025)
ax.xaxis.set_major_formatter(DateFormatter('%Y'))  # Format as just the year
# Set specific y-axis ticks: 1e+09, 2e+09, 3e+09, 4e+09
ax.yaxis.set_major_locator(FixedLocator([1e9, 2e9, 3e9, 4e9]))

# ggplot2-style grid: gray lines on white background
ax.grid(True, linewidth=0.8, color='#E6E6E6', zorder=0)
ax.set_axisbelow(True)

# Remove top, right, and left spines, keep only bottom spine in gray
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)  # Hide y-axis line
ax.spines['bottom'].set_color('#E6E6E6')

# Set tick colors to gray and increase tick length
ax.tick_params(axis='both', colors='#E6E6E6', length=8, width=1.5)
# But keep the tick labels black
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_color('black')

# Position legend at bottom like ggplot2 with larger font
legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3,
                   frameon=False, fontsize=18)

# Adjust layout
plt.tight_layout()

# Save the plot with exact dimensions to match original 2100x2100
# Use bbox_inches=None to maintain exact figure size and set DPI to achieve 2100x2100
plt.savefig(output_path, dpi=150, bbox_inches=None, facecolor='white')
plt.close()

