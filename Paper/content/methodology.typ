= Overview
When analyzing the performance of CPUs, it is impractical to test the performance of existing processors due to large amounts of variability in processor design philosophies and goals.
Existing RISC processors are typically aimed for energy efficiency, and existing CISC processors are typically aimed for performance.
While using existing processors could lead to bias, designing and fabricating laboratory processors is even more impractical due to the high costs and lead times (delays) that would be incurred.
Modern researchers, when evaluating the performance of different complexity ISAs, typically either look at a single product line that features evolutions of a single ISA, or the researchers simulate the performance and area of the processor using tools such as the gem5 simulator.
gem5 is a discrete-event computer architecture simulator that is useful for testing the designs of different CPU microarchitectures, but can be applied to keep the microarchitectures relatively the same and evaluate the performance of the ISAs instead.

= Methodology

Using gem5’s modular design, my models were controlled at a very fine level, simulating key hardware components such as caches, memory controllers, buses, I/O Devices, and most importantly, the ISA & type of core (In-Order vs Out-of-Order).
Of the many pre-built and industry-standard benchmark suites existing with gem5 out-of-the-box, this study used the GAPBS benchmark suite.

The Graph Algorithm Performance Benchmark Suite (GAPBS) was chosen due to how it heavily tests memory access efficiency across its suite of different graph algorithms, such as for Breadth First Search (BFS), PageRank, Betweenness Centrality, Triangle Counting, and Single-Source Shortest Paths (SSSP).
While not indicative of overall performance, the memory-intensiveness of the GAPBS benchmark suite is helpful for indicating which processors are going to be more energy efficient in high memory bandwidth applications.
It is important to note that two other benchmark suites that are considered industry standard were not used due to licensing issues, namely SPEC-CPU and PARSEC.

The process for benchmarking each ISA went as follows: a script written using the gem5 simulator framework tested gem5’s standard library implementation of base x86, ARM, and RISC-V 64-bit CPUs in configurations consisting of combinations of CPU type and binary type, so the In-Order and Out-of-Order CPU type configurations and the bc, bfs, cc, cc_sv, converter, pr, pr_spmv, sssp, and tc GAPBS benchmarks were tested.
All CPUs were tested with the same 4GiB of 4400 MT/s DDR5 RAM with 2 channels and an interleaving size of 64.
All CPUs had the amount of cache in an AMD Ryzen 9800x3d when normalizing for each core (32KiB L1 Data Cache, 32KiB L1 Instruction Cache, and 1 MiB of L2 Cache), which simulates a current high-end consumer desktop CPU.
The benchmark suite was run in Syscall Emulation mode and not Full System Emulation mode because Full System Emulation (including Linux Kernel bootup) was not needed.
All benchmarks were run with a single core to test single-core performance and efficiency.
