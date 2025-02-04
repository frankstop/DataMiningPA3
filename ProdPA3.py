import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.stats as stats

st.title("Salary Analysis for Data Mining - PA3")
st.markdown("""
### Overview
In this app, we explore salary distributions through a histogram, boxplots, scatter plots, quantile plots, and a Q-Q plot. We also compare two salary datasets.
""")

# --- Load the Data ---
data1 = [45, 50, 52, 55, 60, 62, 65, 67, 70, 72, 75, 78, 80, 85, 88, 90, 95, 100, 105, 110, 120, 125, 130, 140, 150, 160, 170, 180, 200, 220, 400, 500]
data2 = [48, 53, 55, 58, 62, 65, 68, 71, 74, 76, 79, 82, 85, 90, 93, 96, 100, 105, 110, 115, 125, 132, 138, 145, 155, 165, 175, 185, 210, 230, 380, 450]

# --- Histogram with Animation ---
st.header("Histogram of Salary Data (Dataset 1)")

# Use a slider to let the user adjust the number of bins.
bins = st.slider("Select number of bins:", min_value=5, max_value=30, value=10)

# Create an empty container for animation
hist_container = st.empty()

# Animate the histogram: gradually increase the number of bins from a small value to the selected value.
for b in range(5, bins + 1):
    fig, ax = plt.subplots()
    ax.hist(data1, bins=b, color='skyblue', edgecolor='black')
    ax.set_title(f"Histogram with {b} bins")
    ax.set_xlabel("Salary")
    ax.set_ylabel("Frequency")
    hist_container.pyplot(fig)
    time.sleep(0.2)  # Pause to create an animation effect

st.markdown("""
**Interpretation:**  
The histogram shows a concentration of salaries at the lower end with a long tail towards the higher salaries. This suggests that while most salaries are modest, a few high values (possibly outliers) create a heavy tail.
""")

# --- Boxplot and Outlier Analysis ---
st.header("Boxplot and Outlier Analysis (Dataset 1)")
fig_box, ax_box = plt.subplots(1, 2, figsize=(12, 5))

# Plot the original boxplot
ax_box[0].boxplot(data1, vert=True, patch_artist=True, boxprops=dict(facecolor="lightgreen"))
ax_box[0].set_title("Original Boxplot")

# Calculate Q1, median, Q3
q1 = np.percentile(data1, 25)
median = np.percentile(data1, 50)
q3 = np.percentile(data1, 75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

# Identify outliers
outliers = [x for x in data1 if (x < lower_bound or x > upper_bound)]
st.markdown(f"**Original Statistics:**  \n- Q1: {q1}  \n- Median: {median}  \n- Q3: {q3}  \n- Outliers: {outliers}")

# Remove outliers and recalculate
data1_no_out = [x for x in data1 if lower_bound <= x <= upper_bound]
q1_new = np.percentile(data1_no_out, 25)
median_new = np.percentile(data1_no_out, 50)
q3_new = np.percentile(data1_no_out, 75)
st.markdown(f"**After Removing Outliers:**  \n- Q1: {q1_new}  \n- Median: {median_new}  \n- Q3: {q3_new}")

# Plot the updated boxplot
ax_box[1].boxplot(data1_no_out, vert=True, patch_artist=True, boxprops=dict(facecolor="salmon"))
ax_box[1].set_title("Boxplot without Outliers")

st.pyplot(fig_box)

st.markdown("""
**Discussion:**  
Removing the outliers reduces the spread of the data and provides a clearer view of the central tendency. The updated boxplot shows a more compact distribution with adjusted quartiles.
""")

# --- Compare Two Distributions ---
st.header("Comparison of Two Salary Distributions")

# Scatter Plot Comparison
st.subheader("Scatter Plot Comparison")
fig_scatter, ax_scatter = plt.subplots()
# Using index positions for the x-axis
indices = list(range(1, len(data1) + 1))
ax_scatter.scatter(indices, data1, color='blue', label='Dataset 1', s=50)
ax_scatter.scatter(indices, data2, color='red', label='Dataset 2', s=50, marker='x')
ax_scatter.set_xlabel("Data Index")
ax_scatter.set_ylabel("Salary")
ax_scatter.set_title("Scatter Plot of Two Datasets")
ax_scatter.legend()
st.pyplot(fig_scatter)

# Side-by-Side Boxplot Comparison
st.subheader("Boxplot Comparison")
fig_box_comp, ax_box_comp = plt.subplots()
ax_box_comp.boxplot([data1, data2], labels=["Dataset 1", "Dataset 2"], patch_artist=True,
                    boxprops=dict(facecolor="lightblue"))
ax_box_comp.set_title("Boxplot Comparison")
st.pyplot(fig_box_comp)

st.markdown("""
**Comparison Interpretation:**  
The scatter plot and boxplots show that while both datasets cover a similar range, their distributions differ slightly. These differences are visible in their central tendencies and spread.
""")

# --- Quantile Plots for Each Dataset with Q1, Q2, Q3 Markers and an Interactive Marker ---
st.header("Quantile Plots for Each Dataset")

# New option: Marker Orientation (Vertical or Horizontal)
marker_orientation = st.radio("Select marker orientation:", options=["Vertical", "Horizontal"], index=0)

fig_quant, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Dataset 1 Quantile Plot
n1 = len(data1)
percentiles1 = np.linspace(0, 100, n1)
sorted_data1 = np.sort(data1)
ax1.plot(percentiles1, sorted_data1, marker='o', linestyle='-', label='Data Points')

# For vertical markers, we use the percentile positions directly.
if marker_orientation == "Vertical":
    ax1.axvline(25, color='orange', linestyle='--', label='Q1 (25th)')
    ax1.axvline(50, color='green', linestyle='--', label='Q2 (50th)')
    ax1.axvline(75, color='red', linestyle='--', label='Q3 (75th)')
else:
    # For horizontal markers, use the salary values at these percentiles.
    q1_val = np.percentile(data1, 25)
    q2_val = np.percentile(data1, 50)
    q3_val = np.percentile(data1, 75)
    ax1.axhline(q1_val, color='orange', linestyle='--', label='Q1 (25th)')
    ax1.axhline(q2_val, color='green', linestyle='--', label='Q2 (50th)')
    ax1.axhline(q3_val, color='red', linestyle='--', label='Q3 (75th)')

ax1.set_title("Quantile Plot: Dataset 1")
ax1.set_xlabel("Percentile")
ax1.set_ylabel("Salary")
ax1.legend()

# Dataset 2 Quantile Plot
n2 = len(data2)
percentiles2 = np.linspace(0, 100, n2)
sorted_data2 = np.sort(data2)
ax2.plot(percentiles2, sorted_data2, marker='o', linestyle='-', label='Data Points')

if marker_orientation == "Vertical":
    ax2.axvline(25, color='orange', linestyle='--', label='Q1 (25th)')
    ax2.axvline(50, color='green', linestyle='--', label='Q2 (50th)')
    ax2.axvline(75, color='red', linestyle='--', label='Q3 (75th)')
else:
    q1_val2 = np.percentile(data2, 25)
    q2_val2 = np.percentile(data2, 50)
    q3_val2 = np.percentile(data2, 75)
    ax2.axhline(q1_val2, color='orange', linestyle='--', label='Q1 (25th)')
    ax2.axhline(q2_val2, color='green', linestyle='--', label='Q2 (50th)')
    ax2.axhline(q3_val2, color='red', linestyle='--', label='Q3 (75th)')

ax2.set_title("Quantile Plot: Dataset 2")
ax2.set_xlabel("Percentile")
ax2.set_ylabel("Salary")
ax2.legend()

# --- Interactive Marker Option ---
show_interactive = st.checkbox("Show Interactive Marker", value=False)
if show_interactive:
    marker_percent = st.slider("Select percentile for interactive marker", 0, 100, 50)
    
    # For each dataset, calculate the corresponding salary value.
    interactive_val1 = np.percentile(data1, marker_percent)
    interactive_val2 = np.percentile(data2, marker_percent)
    
    if marker_orientation == "Vertical":
        # Plot vertical marker at the chosen percentile.
        ax1.axvline(marker_percent, color='black', linestyle='-', linewidth=2,
                    label=f"{marker_percent}th Percentile")
        ax2.axvline(marker_percent, color='black', linestyle='-', linewidth=2,
                    label=f"{marker_percent}th Percentile")
    else:
        # Plot horizontal marker at the corresponding salary value.
        ax1.axhline(interactive_val1, color='black', linestyle='-', linewidth=2,
                    label=f"{marker_percent}th Percentile")
        ax2.axhline(interactive_val2, color='black', linestyle='-', linewidth=2,
                    label=f"{marker_percent}th Percentile")
    
    # Update legends to include the interactive marker.
    ax1.legend()
    ax2.legend()

st.pyplot(fig_quant)

st.markdown("""
**Observations on the Quantile Plots:**  
The quantile plots display how the salary values progress across percentiles for each dataset.  
- Vertical markers (default) are drawn at the 25th, 50th, and 75th percentiles.  
- Horizontal markers show the salary values corresponding to these percentiles.  
The interactive marker allows you to select any percentile to further explore the data.
""")

# --- Q-Q Plot ---
st.header("Q-Q Plot Between Datasets")

# For a two-sample Q-Q plot, we sort both datasets and plot quantiles against each other.
data1_sorted = np.sort(data1)
data2_sorted = np.sort(data2)

# Since both datasets have the same number of data points (32), we can plot them directly.
fig_qq, ax_qq = plt.subplots()
ax_qq.scatter(data1_sorted, data2_sorted, color='purple')
min_val = min(data1_sorted[0], data2_sorted[0])
max_val = max(data1_sorted[-1], data2_sorted[-1])
ax_qq.plot([min_val, max_val], [min_val, max_val], 'k--', lw=2)  # 45-degree reference line
ax_qq.set_title("Q-Q Plot: Dataset 1 vs. Dataset 2")
ax_qq.set_xlabel("Quantiles of Dataset 1")
ax_qq.set_ylabel("Quantiles of Dataset 2")
st.pyplot(fig_qq)

st.markdown("""
**Observation from the Q-Q Plot:**  
If the plotted points lie close to the 45-degree line, it indicates that the two datasets have similar distributional characteristics. Deviations from this line suggest differences such as heavier tails or shifts in the central location.
""")