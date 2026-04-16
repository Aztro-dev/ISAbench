= Literature Review

The earliest computers were tailored to very specific applications, resulting in programs that were not portable.
This meant that a program written for one computer was not easily able to be shared from one lab to another, and such a transfer would necessitate an almost entire rewrite if the computers used did not match exactly.
Through IBM’s System/360 family of computers, the concept of an “architecture” became separate from the “implementation” @amdahl1964architecture.
This was the first (true) system that featured multiple implementations with different performance specs, but compatible architectures, meaning programs could be run across the entire family without having to write for one specific system.
This resulted in a few innovations, namely a “storage approach”, which allowed for more capacities and hierarchies of speed of memory; A new approach for Input/Output (have processors do IO, not the CPU); better data exchange because of specified data formats; and the concept of a device “family”, where there were multiple “tiers” of product, so everyone from the small business to large scientific institutions could use these products @amdahl1964architecture.

In the 1980s, David Patterson and David Ditzel analyzed existing CISC architecture to find instruction frequency distributions, compiler behavior, and microarchitecture complexity.
They found that in IBM 360 compilers, only 10 instructions accounted for 80% of executed instructions, 16 for 90%, 21 for 95%, and 30 for 99% @patterson1980case.
They argued that CISC's complex instructions increased cycle time, complicated pipelining, and consumed silicon area that could be better used for registers and cache.
They proposed a simplified instruction set with uniform instruction formats, a load-store architecture (having explicit instructions for storing and loading data, simplifying execution), and large register files optimized for compiler use.
They used the IBM 801 minicomputer as an example of a great RISC machine, one of the first times that the idea of a reduced instruction set alone could result in better performance @patterson1980case.
Many companies did research into the performance and efficiency of their processors, notably Intel found that as their processors got more complex, the performance would increase but energy efficiency fell sharply @grochowski2006energy.
In Intel’s testing, the Pentium 4 (Cedarmill) processor was 8x faster than the i486 processor, but consumed 38x the power @grochowski2006energy.

The vast majority of researchers–including the Intel researchers doing the Pentium study–use the SPEC CPU benchmarks, a benchmark suite designed to compare CPU performance across different ISAs fairly and in a way that is reproducible.
Compute-intensive workloads are divided into integer (SPECint) and floating-point (SPECfp) categories.
The benchmarks measure both speed (single-task performance) and rate (throughput with multiple cores/copies).
SPEC defines specific compilation flags, memory requirements, and reporting requirements to ensure reproducible results @dixit1991spec.
At the time of its introduction in 1989, the SPEC CPU benchmarks were meant to run on real hardware, requiring millions of dollars upfront and a lot of time to fabricate the chips themselves.
Nowadays, most researchers do some kind of simulation, typically with the gem5 simulator @lowepower2020gem5.
Gem5 allows researchers to model hardware at the cycle level, with enough fidelity to boot Linux-based operating systems and run full applications for multiple architectures @lowepower2020gem5.
Some researchers, when estimating the final size of their chip design, use McPAT, a Power Area and Timing framework for power draw and area analysis of different implementations of different ISAs.
It supports processor configurations for under 22nm for manycore and multicore, including models for Out-of-Order processor cores, shared caches, and multiple-domain clocking.
These configurations are incredibly useful when comparing the performance, cost, and efficiency of different CPU implementations @li2009mcpat.

Much lab research has been done to evaluate the performance and efficiency differences between ISAs using either simulations or real-world processors, though they typically target a specific field such as High-Performance Computing or low-energy environments.
A study comparing the differences between many different ISA extensions found that SIMD speedups over compiled C code ranged from a 2x to 5x improvement on average, with some kernels achieving much higher speedups (up to 36.
6x for the DCT kernel on Motorola G4).
Motorola's 128-bit AltiVec extension (PowerPC) performed best overall (23.
7% better than average), followed by AMD Athlon (19.
1% better than average) and Intel Pentium III (10.
9% better than average) @slingerland2001performance.
Another study done on the differences between x86_64, ARM, and Alpha found that, while ISAs did have a measurable impact on performance, there was no significant performance difference for In-Order cores, and there was a reduced performance difference for Out-of-Order cores.
This study emphasized that microarchitectural differences were more significant than just ISA changes @akram2019study.

In an analysis of ARM and RISC-V SoCs however, RISC-V CPUs were found to be 1/4th as energy-hungry as ARM CPUs, but were significantly slower (6x) than the ARM CPUs @suarez2024comprehensive.
This could in part be explained by a 2019 study testing many different CPUs with many different ISAs that found that microarchitecture had a vastly greater impact on performance and efficiency than ISA alone @akram2017impact.
This gives credibility to the idea that ISAs don’t inherently give CPUs their performance, it’s the industry requirements that give CPUs their performance.
For example, a CPU design company aiming for mass-produced and cheap processors might opt for the most energy-efficient design, so CPUs are naturally going to be more energy-efficiency oriented regardless of ISA.
Vector Instruction Extensions are another argument however, as when they are tested in limited thermal situations, the differences between the extensions follow a clear decrease in energy efficiency and clock speed for every new extension generation.
For x86_64 specifically, many different CPU benchmarks were run on SSE, AVX, AVX2, and AVX512 vector extensions, finding that while AVX512 had the best performance in ideal scenarios, thermal limitations caused the CPU to perform worse due to decreased clock speeds and energy efficiency ratings @guermouche2019experimental.

While smart decisions while designing ISAs and their extensions have been shown to affect performance, the microarchitecture of the CPU still has a large effect on the performance and energy efficiency of a chip.
This is demonstrated by the Forward Slice Core Microarchitecture design, which was simulated to be 64% better than an In-Order core, and a couple dozen percentage points around other microarchitectures @lakshminarasimhan2020forward.
This shows that CPUs with the same ISA can still vary in performance significantly, and this must be controlled for in the experiment.
The effect of other parts of the CPU have been shown to also have massive impacts on energy efficiency, especially with register files.
Register files are the most frequently used form of memory and are implemented in the silicon of the chip itself.
The size of the register file can be, in part, determined by the ISA of the overall CPU, as ISAs that call for more registers in their specifications will naturally result in more registers in the physical register file.
A 3.6% increase in the size of a register file has been shown to have a 24% reduction in dynamic energy and 54% reduction in static energy consumption @tavana2015dynamically.
Part of the reason the register file is so important is that it is used in almost every single operation, due to their crucial role as the most accessible form of memory in the CPU.
The register file isn’t always needed however, as a 4-level register hierarchy with a bypass network could avoid 25-40% of the register file reads through clever instruction result mapping @asanovic2014energy.
This means that instead of storing data directly into the register file after every operation, the results of some operations could bypass the register file entirely and be fed into the next operation.
Using the register file less is a great optimization for energy efficiency since a register file access can take 50x the energy of an arithmetic operation @asanovic2014energy.
While the register file uses a large amount of energy relative to an arithmetic operation, the register file is estimated to use 10x less energy than an off-chip memory access, meaning decreasing these off-chip memory accesses is also a point of optimization.
The issue with just increasing the size of the register file is that, with an energy-aware compiler (encc) and a low-power ARM configuration, an increase from 3 to 8 registers saves 22% of the energy, but there are diminishing returns after the 7-19 register range @wehmeyer2001analysis.
While the number of registers in a register file has a significant impact on the energy efficiency of a CPU, the number of ports (inputs and outputs of the register file) can quadratically increase the amount of energy used in a processor.
Additionally, split register file microarchitectures have shown promise over traditional, monolithic register files.
A split register file configuration can result in a decrease of 9-10% for input data switching activity (selecting which registers to read from), and a decrease of 12-14% for output data switching activity (selecting which registers to write to).
This solution not only reduces the energy consumption for each local register file by 17%, but it also decreases the area required for a register file, increasing processor manufacturing yield and decreasing costs @zyuban1998energy.

While microarchitectural improvements can be made, there have been many architectural improvements suggested to increase performance.
By accelerating frequently used sequences of instructions, an architecture framework for Transparent Instruction Set Customization was estimated to gain over 2.
2x the average performance of traditional general Configurable Compute Accelerator (CCA) designs @clark2005architecture.
This framework is especially promising since it reduces not only the area (and therefore cost) of the accelerators, but it also reduces the time spent designing and verifying chips.
By modifying a general-purpose ISA to interface nicely with this framework, one general purpose processor can be accelerated by any number of accelerator chips, reducing verification costs, decreasing development time, and increasing performance and energy efficiency.
Another promising solution is with Composite-ISA cores.
A common configuration for a CPU in the embedded space is to have a CPU with multiple ISAs, typically one that targets efficiency and one that targets performance.
Composite-ISA cores are different from traditional cross-ISA processors since Composite-ISA cores implement many different versions of the same base ISA across the processor, while a traditional cross-ISA processor implements different ISAs across cores.
With Composite-ISA cores, results have shown a performance increase of 19% and an energy-savings of 30% over previous single-ISA heterogeneous designs @venkat2019composite.
These composite-ISA cores can also significantly decrease licensing costs and eliminate the need for cross-ISA binary translation.
While RISC ISAs are generally identified in part by their constant-width instructions (meaning each instruction takes up the same amount of bits), an extension to RISC ISAs to give variable-length instructions has been shown to save 15% of data and memory path energy, as well as up to 23% of the execution time of the instruction fetch stage specifically @collin2003low.

Previous research has traditionally focused only on a few ISAs, or only measured performance and not efficiency.
With this research, I measured both the performance and efficiency of many different ISAs in many different configurations with the most up-to-date specifications possible.
