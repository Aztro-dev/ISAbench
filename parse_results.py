import os
import re
import csv

# --- Configuration ---
ROOT_DIR = "./GAPBS"
OUTPUT_CSV = "gem5_gapbs_results.csv"

ISA_FOLDER_MAP = {
    "x86": "x86",
    "arm": "ARM",
    "riscv": "RISCV",
    "sparc": "SPARC",
    "power": "PowerPC",
    "mips": "MIPS",
}

ISAS = ["x86", "arm", "riscv", "sparc", "power", "mips"]
CPUS = ["o3", "in-order"]
BINARIES = ["bc", "bfs", "cc", "cc_sv", "converter", "pr", "pr_spmv", "sssp", "tc"]

# Define the statistics keys we want to find in the stats.txt files.
# Note: Some keys might vary slightly between CPU models (O3 vs Minor/In-Order).
STATS_OF_INTEREST = {
    "Sim_Seconds": r"simSeconds\s+([\d\.]+)",
    "Sim_Insts": r"simInsts\s+(\d+)",
    "Host_Inst_Rate": r"hostInstRate\s+(\d+)",
    "IPC": r"board\.processor\.cores\.core\.ipc\s+([\d\.]+)",
    "L1D_Miss_Rate": r"board\.cache_hierarchy\.l1dcaches\.overallMissRate::total\s+([\d\.]+)",
    "L1D_Avg_Miss_Lat": r"board\.cache_hierarchy\.l1dcaches\.overallAvgMissLatency::total\s+([\d\.]+)",
    "L2_Miss_Rate": r"board\.cache_hierarchy\.l2caches\.overallMissRate::total\s+([\d\.]+)",
    "ROB_Reads": r"board\.processor\.cores\.core\.rob\.reads\s+(\d+)",
    "ROB_Writes": r"board\.processor\.cores\.core\.rob\.writes\s+(\d+)",
    "Branch_Mispred": r"board\.processor\.cores\.core\.branchPred\.condIncorrect\s+(\d+)",
}


def parse_stats_file(file_path):
    """Parses a single gem5 stats.txt file and returns a dictionary of values."""
    results = {}
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r") as f:
        content = f.read()
        for stat_name, pattern in STATS_OF_INTEREST.items():
            match = re.search(pattern, content)
            if match:
                results[stat_name] = match.group(1)
            else:
                results[stat_name] = "N/A"
    return results


def main():
    all_data = []

    for isa in ISAS:
        folder_name = ISA_FOLDER_MAP.get(isa)
        for binary in BINARIES:
            for cpu in CPUS:
                # Construct file name: gapbs_"$isa"_"$bin"_"$cpu"_ddr5_stats.txt
                filename = f"gapbs_{isa}_{binary}_{cpu}_ddr5_stats.txt"
                file_path = os.path.join(ROOT_DIR, folder_name, filename)

                print(f"Checking: {file_path}")
                stats = parse_stats_file(file_path)

                if stats:
                    # Add metadata to the results
                    row = {
                        "ISA": isa,
                        "Binary": binary,
                        "CPU_Type": cpu,
                    }
                    row.update(stats)
                    all_data.append(row)

    if not all_data:
        print("No stats files found. Please check your ROOT_DIR and file paths.")
        return

    # Write to CSV
    headers = ["ISA", "Binary", "CPU_Type"] + list(STATS_OF_INTEREST.keys())
    with open(OUTPUT_CSV, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(all_data)

    print(f"\nExtraction complete! Results saved to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
