import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# --- Configuration ---
INPUT_CSV = "gem5_gapbs_results.csv"
SAVE_PREFIX = "analysis_"
# Setting the baseline for normalization
BASELINE_ISA = "x86"
BASELINE_CPU = "in-order" 

def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)
    # Ensure numeric types
    cols = ["Sim_Seconds", "Sim_Insts", "IPC", "L1D_Miss_Rate", "L2_Miss_Rate", "Branch_Mispred"]
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def normalize_to_baseline(df):
    """Normalizes performance metrics to the x86 In-Order configuration."""
    normalized_list = []
    for binary in df['Binary'].unique():
        bin_subset = df[df['Binary'] == binary].copy()
        # Find the baseline value for this specific benchmark
        base_row = bin_subset[(bin_subset['ISA'] == BASELINE_ISA) & 
                              (bin_subset['CPU_Type'] == BASELINE_CPU)]
        
        if not base_row.empty:
            base_time = base_row['Sim_Seconds'].values[0]
            base_insts = base_row['Sim_Insts'].values[0]
            
            bin_subset['Rel_Runtime'] = bin_subset['Sim_Seconds'] / base_time
            bin_subset['Rel_Inst_Count'] = bin_subset['Sim_Insts'] / base_insts
            normalized_list.append(bin_subset)
    
    return pd.concat(normalized_list) if normalized_list else df

def main():
    df_raw = load_and_clean_data(INPUT_CSV)
    df = normalize_to_baseline(df_raw)
    sns.set_theme(style="whitegrid", palette="muted")

    # ==========================================
    # 1. 2D GRAPH SUITE: THE "DIFFERENCE" VIEWS
    # ==========================================

    # GRAPH A: Normalized Execution Time (The Big Picture)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df[df['CPU_Type'] == 'in-order'], x="Binary", y="Rel_Runtime", hue="ISA")
    plt.axhline(1, color='black', linestyle='--', label=f'{BASELINE_ISA} {BASELINE_CPU} Baseline')
    plt.title(f"In-Order Performance Relative to {BASELINE_ISA} (Lower is Better)")
    plt.ylabel("Relative Runtime")
    plt.legend(title="ISA", bbox_to_anchor=(1, 1))
    plt.savefig(f"{SAVE_PREFIX}2d_rel_performance.png")

    # GRAPH B: The Instruction "Tax" (CISC vs RISC)
    # Shows if an ISA needs more instructions to do the same work
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df[df['CPU_Type'] == 'in-order'], x="Binary", y="Rel_Inst_Count", hue="ISA")
    plt.title("Instruction Count Comparison (Normalized to x86)")
    plt.ylabel("Relative Number of Instructions")
    plt.savefig(f"{SAVE_PREFIX}2d_instruction_tax.png")

    # GRAPH C: IPC Comparison
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x="ISA", y="IPC", hue="CPU_Type")
    plt.title("IPC Distribution: In-Order vs. O3 across all Benchmarks")
    plt.savefig(f"{SAVE_PREFIX}2d_ipc_comparison.png")

    # GRAPH D: Cache Bottleneck Analysis
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="L1D_Miss_Rate", y="IPC", hue="ISA", style="CPU_Type", s=100)
    plt.title("Efficiency: How Cache Misses Impact Throughput (IPC)")
    plt.savefig(f"{SAVE_PREFIX}2d_cache_vs_ipc.png")

    # ==========================================
    # 2. 3D GRAPH SUITE: MULTI-VARIABLE TRENDS
    # ==========================================

    # 3D SCATTER: Runtime, IPC, and Cache Misses
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Mapping ISAs to specific colors for consistency
    colors = {'x86': 'blue', 'arm': 'green', 'riscv': 'red', 'sparc': 'orange', 'power': 'purple', 'mips': 'brown'}
    
    for isa in df['ISA'].unique():
        sub = df[(df['ISA'] == isa) & (df['CPU_Type'] == 'in-order')]
        ax.scatter(sub['L1D_Miss_Rate'], sub['IPC'], sub['Rel_Runtime'], 
                   label=isa, s=80, edgecolors='w', color=colors.get(isa, 'grey'))

    ax.set_xlabel('L1D Miss Rate')
    ax.set_ylabel('IPC')
    ax.set_zlabel('Relative Runtime')
    plt.title("3D Efficiency Landscape (In-Order Only)")
    plt.legend()
    plt.savefig(f"{SAVE_PREFIX}3d_landscape.png")

    print("All 2D and 3D graphs have been generated.")

if __name__ == "__main__":
    main()
