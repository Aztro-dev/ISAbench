= Introduction

An Instruction Set Architecture (ISA) defines how Central Processing Units (CPUs) interact with software through “instructions,” the lowest level steps that programs execute.
Some instructions are simple and ubiquitous, such as an ADD (add two registers) or LOAD (load data) instruction, but ISAs can include more complex instructions that aren’t shared across ISAs.
These complex instructions are more frequently found in “Complex” Instruction Sets, and are used significantly less than the “simple” instructions.
Complex Instruction Set Computer (CISC) architectures, such as x86, and Motorola 68k, are characterized by hundreds or thousands of base instructions, with many of those instructions taking longer than the traditional one-cycle instruction, and having many different memory operations.
CISC ISAs were dominant in the “early” days of computing where efficient memory usage and small code sizes were paramount.
The main CISC ISA still dominant today is x86_64–the 64-bit “modern” version of the x86 ISA–and is primarily used in high-performance environments such as data centers and high-end desktop computers.
Unlike the CISC ISAs pioneered by x86, Reduced Instruction Set Computer (RISC) ISAs were hitting the market in the 1980s and 1990s, characterized by fixed-width instructions, a low instruction count, and larger binary (executable file) sizes due to the reduced efficiency compression with fixed-width instructions.
Over time, RISC ISAs such as ARM, PowerPC, RISC-V, and MIPS have been focused in the embedded (low power, low cost) market, with ARM having had the greatest reach in the low-power (embedded) and mobile (smartphone + laptop) markets @blem2015isa.

Ever since the invention of ISAs, debates between which ISAs give “better” performance have raged on.
Some say that the ISA has a negligible impact on the performance of the CPU and that the microarchitecture (the low-level implementation of the CPU itself) has a larger impact on performance and efficiency.
Others say that the features of some ISAs can affect microcode efficiency, processor area, and performance.
This debate is easily categorized into the debate between CISC and RISC ISAs.
CISC ISAs still dominate the high-performance computing market with x86, although RISC ISAs (ARM and RISC-V) are gaining traction, even if at a slow rate.
The debate between whether CISC ISAs are slower/faster than RISC ISAs, or are more/less efficient, is important to supercomputer and datacenter builders, who value raw performance and low operating costs.
This research study will examine if and how ISA differences can result in real-world performance.
