= Results
#figure(
  placement: none,
  image("../figures/3d_overview.png"),
  caption: [Time taken for each ISA on each of the benchmarks plotted as a function of Cache Miss Rate and Memory Energy consumed.]
) <fig:landscape>

In @fig:landscape you can see an overall performance trend of ARM being faster than RISC-V, which is faster than x86.
You can also observe the RISC ISAs (ARM and RISC-V) as having higher cache miss rates, which is due to the more 
complex instruction decoding requirements of x86 when compared to the fixed-length instruction decoders required for ARM and RISC-V in the general-computing sense.
The RISC ISAs (ARM and RISC-V) are also observed as having lower energy consumption on average when compared to the CISC ISA (x86).

#figure(
  placement: none,
  image("../figures/code_density.png"),
  caption: [Amount of instructions in each binary for each ISA in millions of instructions]
) <fig:code_density>
In @fig:code_density, you can see another overall trend with ARM having the lowest dynamic instruction count, RISC-V coming in second, and x86 coming in third.
While this may seem counter-intuitive for the CISC instruction set to have the most amount of instructions due to its wide selection of very specialized and niche instructions, 
I believe that this difference comes down to the difference in compilers (more compiler optimizations typically leads to more instructions, especially-so with x86's register-memory architecture as compared to ARM and RISC-V's load-store architecture), 
and possibly due to the effect of register pressure because of x86's 16 defined registers and ARM and RISC-V's 32 general-purpose registers.

#figure(
  placement: none,
  image("../figures/absolute_time.png"),
  caption: [Amount of time taken for each benchmark and ISA combination]
) <fig:absolute_time>
In @fig:absolute_time, we again see that the RISC ISAs lead in performance over the CISC x86 CPU core, possibly because of GAPBS's highly memory-intensive nature.

#figure(
  placement: none,
  image("../figures/ipc_miss_rate_scatter.png"),
  caption: [Number of Instructions Per Cycle (IPC) plotted as a function of the L1 Data Cache (L1D) miss rate]
) <fig:ipc_miss>
In @fig:ipc_miss, ARM stands out as a clear leader in both instructions per clock (IPC) as well as in the L1 Data Cache (L1D) miss rate.
This is due to ARM's high reliance on prefetching, which increases performance in the IPC sense, but leads to a less efficient use of memory because of cache thrashing which is caused by an inefficient filling/clearing of cache.
Here we can see an trend of high L1D miss rates for RISC ISAs because of their load-store architecture, which requires a larger volume of individual memory access instructions for the same task (1 instruction to load data, x instructions to perform operations on that data, 1 instruction to store that data).

= Discussion
