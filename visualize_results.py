import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# --- Configuration ---
INPUT_CSV = "gem5_gapbs_results.csv"
SAVE_PREFIX = "gem5_plot_"


def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)
    # Convert N/A to NaN and ensure numeric columns are floats
    numeric_cols = [
        "Sim_Seconds",
        "Sim_Insts",
        "IPC",
        "L1D_Miss_Rate",
        "L1D_Avg_Miss_Lat",
        "Branch_Mispred",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def normalize_data(df, baseline_isa="x86", baseline_cpu="o3"):
    """Normalizes Sim_Seconds relative to the baseline for each Binary."""
    normalized_dfs = []

    for binary in df["Binary"].unique():
        bin_df = df[df["Binary"] == binary].copy()
        # Find the baseline value for this binary
        baseline_val = bin_df[
            (bin_df["ISA"] == baseline_isa) & (bin_df["CPU_Type"] == baseline_cpu)
        ]["Sim_Seconds"]

        if not baseline_val.empty:
            base = baseline_val.values[0]
            bin_df["Normalized_Runtime"] = bin_df["Sim_Seconds"] / base
            # Speedup is 1/Runtime, but normalized runtime is usually better for bottlenecks
            normalized_dfs.append(bin_df)

    return pd.concat(normalized_dfs) if normalized_dfs else df


def main():
    try:
        df = load_and_clean_data(INPUT_CSV)
    except FileNotFoundError:
        print(f"Error: {INPUT_CSV} not found. Please run the extraction script first.")
        return

    df = normalize_data(df)
    sns.set_theme(style="whitegrid")

    # --- Plot 1: Normalized Execution Time (Grouped Bar) ---
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="Binary", y="Normalized_Runtime", hue="ISA")
    plt.axhline(1, color="red", linestyle="--", label="x86 Baseline")
    plt.title("Execution Time Normalized to x86 (Lower is Better)")
    plt.ylabel("Relative Execution Time")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(f"{SAVE_PREFIX}normalized_runtime.png")
    print(f"Saved: {SAVE_PREFIX}normalized_runtime.png")

    # --- Plot 2: IPC vs Memory Efficiency (Scatter) ---
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df, x="L1D_Miss_Rate", y="IPC", hue="ISA", style="CPU_Type", s=100
    )
    plt.title("Performance vs. Cache Efficiency")
    plt.xlabel("L1 Data Cache Miss Rate")
    plt.ylabel("Instructions Per Cycle (IPC)")
    plt.savefig(f"{SAVE_PREFIX}ipc_vs_cache.png")
    print(f"Saved: {SAVE_PREFIX}ipc_vs_cache.png")

    # --- Plot 3: 3D Scatter Plot (IPC, Miss Rate, Runtime) ---
    # This helps visualize how these three variables interact across ISAs
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    colors = {
        "x86": "blue",
        "arm": "green",
        "riscv": "red",
        "sparc": "orange",
        "power": "purple",
        "mips": "brown",
    }

    for isa in df["ISA"].unique():
        subset = df[df["ISA"] == isa]
        ax.scatter(
            subset["L1D_Miss_Rate"],
            subset["IPC"],
            subset["Sim_Seconds"],
            label=isa,
            s=60,
            color=colors.get(isa, "black"),
        )

    ax.set_xlabel("L1D Miss Rate")
    ax.set_ylabel("IPC")
    ax.set_zlabel("Sim Seconds")
    ax.set_title("3D Performance Landscape")
    plt.legend()
    plt.savefig(f"{SAVE_PREFIX}3d_landscape.png")
    print(f"Saved: {SAVE_PREFIX}3d_landscape.png")

    # --- Plot 4: 3D Bar Chart (ISA vs Binary vs Runtime) ---
    # This provides a cool "cityscape" view of your results
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Mapping categories to numbers for the 3D axes
    isas = df["ISA"].unique()
    bins = df["Binary"].unique()
    isa_map = {name: i for i, name in enumerate(isas)}
    bin_map = {name: i for i, name in enumerate(bins)}

    for _, row in df.iterrows():
        x = isa_map[row["ISA"]]
        y = bin_map[row["Binary"]]
        z = 0
        dx = dy = 0.5
        dz = row["Normalized_Runtime"]
        ax.bar3d(x, y, z, dx, dy, dz, color=colors.get(row["ISA"], "blue"), alpha=0.8)

    ax.set_xticks(np.arange(len(isas)) + 0.25)
    ax.set_xticklabels(isas)
    ax.set_yticks(np.arange(len(bins)) + 0.25)
    ax.set_yticklabels(bins)
    ax.set_zlabel("Normalized Runtime")
    ax.set_title("ISA Performance Overview (3D Bar)")
    plt.savefig(f"{SAVE_PREFIX}3d_bars.png")
    print(f"Saved: {SAVE_PREFIX}3d_bars.png")


if __name__ == "__main__":
    main()
