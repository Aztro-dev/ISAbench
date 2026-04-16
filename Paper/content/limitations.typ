= Limitations

Since microarchitectures can change a significant amount between CPUs even within the same product line, a large amount of work was done to ensure that results were as comparable as possible using gem5’s great level of customization.
One limitation of the microarchitectural differences between CPUs is that ISAs can define certain features that make large impacts in the underlying microarchitecture, and it is difficult to pinpoint the exact cause for overall performance differences due to these effects.
For example, RISC-V has fixed-length instructions, making decoding instructions very simple, but x86 has variable-length instructions, making decoding instructions a complex and area-consuming part of the final processor design.
Another limitation of the experiment is that the results are also largely dependent on compilers/tooling, meaning that unoptimized or unsupported compiler features can affect the results also.
RISC-V is likely to be the ISA with the largest negative (if any) effect due to this, with x86 and ARM having decades of compiler support and corporate backing compared to RISC-V’s relatively new compiler collections and industry support.
This is also reflected in the ISAs chosen for the benchmarks, as the MIPS, SPARC, and PowerPC ISA compiler collections did not support some of the instructions and syscalls required by the GAPBS Benchmark Suite, making them unsuitable for testing, but this is likely due to their lack of real use in Linux systems in recent years.
