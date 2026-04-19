import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D

# Comprehensive visualization script for gem5 GAPBS results
INPUT_CSV = "gem5_gapbs_results.csv"


def run_comprehensive_analysis():
    if not os.path.exists(INPUT_CSV):
        print(f"Error: {INPUT_CSV} not found.")
        return

    df = pd.read_csv(INPUT_CSV).replace("N/A", np.nan)

    # Pre-processing and Scaling
    numeric_cols = [
        "Sim_Seconds",
        "Sim_Insts",
        "Host_Inst_Rate",
        "IPC",
        "L1D_Miss_Rate",
        "L1D_Avg_Miss_Lat",
        "Branch_Mispred",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Sim_Insts_M"] = df["Sim_Insts"] / 1e6
    df["Host_Inst_Rate_M"] = df["Host_Inst_Rate"] / 1e6

    # 1. Relative Speedup Calculation (Baseline: x86 In-Order)
    baselines = df[(df["ISA"] == "x86") & (df["CPU_Type"] == "in-order")].set_index(
        "Binary"
    )["Sim_Seconds"]
    df["Speedup"] = df.apply(
        lambda r: (
            baselines.get(r["Binary"]) / r["Sim_Seconds"]
            if baselines.get(r["Binary"])
            else np.nan
        ),
        axis=1,
    )

    # 2. Power Efficiency (if energy columns exist)
    if "Mem_Energy_0" in df.columns and "Mem_Energy_1" in df.columns:
        df["Total_Energy_mJ"] = (
            pd.to_numeric(df["Mem_Energy_0"], errors="coerce").fillna(0)
            + pd.to_numeric(df["Mem_Energy_1"], errors="coerce").fillna(0)
        ) / 1e9
        df["Power_Efficiency"] = df["Sim_Insts"] / df["Total_Energy_mJ"]

    # 3. Branch MPKI
    if "Branch_Mispred" in df.columns:
        df["Branch_MPKI"] = (df["Branch_Mispred"] / df["Sim_Insts"]) * 1000

    sns.set_theme(style="whitegrid", palette="muted")

    # GRAPH 1: Relative Speedup (Error bars enabled)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="Binary", y="Speedup", hue="ISA")
    plt.axhline(
        1, color="red", linestyle="--", alpha=0.5, label="x86 In-Order Baseline"
    )
    plt.title("Relative Speedup per ISA (Normalized to x86 In-Order)")
    plt.ylabel("Speedup (x)")
    plt.xticks(rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig("relative_speedup.png")

    # GRAPH 2: Absolute Time (Error bars enabled)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="Binary", y="Sim_Seconds", hue="ISA")
    plt.title("Absolute Simulated Execution Time")
    plt.ylabel("Simulated Seconds")
    plt.xticks(rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig("absolute_time.png")

    # GRAPH 3: Code Density (Millions)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="Binary", y="Sim_Insts_M", hue="ISA")
    plt.title("Dynamic Instruction Count (Millions)")
    plt.ylabel("Instructions (Millions)")
    plt.xticks(rotation=45)
    plt.savefig("code_density.png")

    # GRAPH 4: Simulation Speed (NO ERROR BARS)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="Binary", y="Host_Inst_Rate_M", hue="ISA", errorbar=None)
    plt.title("Simulator Performance (MIPS) - Error Bars Removed")
    plt.ylabel("Millions of Instructions / Sec")
    plt.xticks(rotation=45)
    plt.savefig("sim_speed_mips.png")

    # GRAPH 5: Efficiency (Inst/mJ)
    if "Power_Efficiency" in df.columns:
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x="Binary", y="Power_Efficiency", hue="ISA")
        plt.title("Power Efficiency: Performance per Memory Energy")
        plt.ylabel("Instructions per mJ")
        plt.xticks(rotation=45)
        plt.savefig("power_efficiency.png")

    # GRAPH 6: Scatter Trends (Miss Rate vs IPC)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df, x="L1D_Miss_Rate", y="IPC", hue="ISA", style="CPU_Type", s=100
    )
    plt.title("Architectural Trend: IPC vs. Cache Miss Rate")
    plt.savefig("ipc_miss_rate_scatter.png")

    # GRAPH 7: 3D System Overview
    if "Total_Energy_mJ" in df.columns:
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection="3d")
        for isa in df["ISA"].unique():
            sub = df[df["ISA"] == isa]
            ax.scatter(
                sub["L1D_Miss_Rate"],
                sub["Total_Energy_mJ"],
                sub["Sim_Seconds"],
                label=isa,
                s=80,
            )
        ax.set_xlabel("Cache Miss Rate")
        ax.set_ylabel("Energy (mJ)")
        ax.set_zlabel("Time (s)")
        plt.title("3D Multi-Metric Performance Overview")
        plt.legend()
        plt.tight_layout()
        plt.savefig("3d_overview.png")

    print("Comprehensive analysis complete. All graphs generated.")


if __name__ == "__main__":
    run_comprehensive_analysis()
