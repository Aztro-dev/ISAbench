import argparse
from gem5.isas import ISA
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import (
    PrivateL1SharedL2CacheHierarchy,
)
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator


def get_isa(isa_str):
    isa_map = {
        "x86": ISA.X86,
        "arm": ISA.ARM,
        "riscv": ISA.RISCV,
        "sparc": ISA.SPARC,
        "power": ISA.POWER,
        "mips": ISA.MIPS,
    }
    if isa_str.lower() not in isa_map:
        raise ValueError(f"Unsupported ISA: {isa_str}")
    return isa_map[isa_str.lower()]


def get_memory(mem_str):
    if mem_str.lower() == "ddr5":
        # Create a dual-channel DDR5 system
        from gem5.components.memory.memory import ChanneledMemory
        from gem5.components.memory.dram_interfaces.ddr5 import DDR5_4400_4x8

        return ChanneledMemory(
            DDR5_4400_4x8, num_channels=2, interleaving_size=64, size="4GiB"
        )
    elif mem_str.lower() == "hbm":
        # Create an HBM2 stack
        from gem5.components.memory.hbm import HBM2Stack

        return HBM2Stack(size="32GiB")
    else:
        raise ValueError(f"Unsupported memory type: {mem_str}")


def get_cpu(cpu_str):
    if cpu_str.lower() == "ooo" or cpu_str.lower() == "o3":
        return CPUTypes.O3
    elif cpu_str.lower() == "in-order" or cpu_str.lower() == "inorder":
        return CPUTypes.TIMING
    else:
        raise ValueError(f"Unsupported CPU type: {cpu_str}")


def get_workload(work_str):
    from gem5.resources.resource import obtain_resource

    # gem5 will download this binary for you automatically
    return obtain_resource("riscv-gapbs-bfs-run")


def main():
    parser = argparse.ArgumentParser(
        description="Cross-ISA Power and Performance Experiment"
    )
    parser.add_argument(
        "--isa", type=str, required=True, help="x86, arm, riscv, sparc, power, mips"
    )
    parser.add_argument(
        "--cpu",
        type=str,
        required=True,
        choices=["in-order", "o3"],
        help="in-order or o3",
    )
    parser.add_argument("--mem", type=str, required=False, help="ddr5 or hbm")
    parser.add_argument(
        "--binary",
        type=str,
        required=True,
        help="Path to your compiled benchmark binary",
    )
    args = parser.parse_args()

    # High-end Desktop L1/L2 cache hierarchy
    cache_hierarchy = PrivateL1SharedL2CacheHierarchy(
        l1d_size="32KiB", l1i_size="32KiB", l2_size="1MiB"
    )

    # Default do DDR5
    memory = get_memory("ddr5")
    if args.mem is not None:
        memory = get_memory(args.mem)

    # 1 core for now until we get fancy
    processor = SimpleProcessor(
        cpu_type=get_cpu(args.cpu), isa=get_isa(args.isa), num_cores=1
    )

    # 4.5 GHz for now until we get fancy
    board = SimpleBoard(
        clk_freq="4.5GHz",
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy,
    )

    binary_resource = BinaryResource(args.binary)
    # Arguments: 2^10 vertices, ran one time
    board.set_se_binary_workload(binary_resource, arguments=["-g", "10", "-n", "1"])

    # Run dat sim
    print("--- Starting Simulation ---")
    print(
        f"ISA: {args.isa.upper()} | Memory: {args.mem.upper()} | Benchmark: {args.binary}"
    )

    simulator = Simulator(board=board)
    simulator.run()

    print("--- Simulation Complete ---")
    print(f"Simulated ticks: {simulator.get_current_tick()}")


main()
