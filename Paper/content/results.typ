= Results
#figure(
  placement: none,
  image("../figures/analysis_2d_ipc_comparison.png"),
  caption: [Instructions Per Clock (IPC) compared between the ISAs as well as their CPU Type (In-Order vs Out-of-Order)]
) <fig:ipc>

#figure(
  placement: none,
  image("../figures/analysis_2d_cache_vs_ipc.png"),
  caption: [Instructions Per Clock (IPC) plotted as a function of L1 Data Cache (L1D) Miss Rate between x86, ARM, and RISC-V.]
) <fig:cache_vs_ipc>

#figure(
  placement: none,
  image("../figures/analysis_2d_instruction_tax.png"),
  caption: [Instruction Count comparison in final binary between x86, ARM, and RISC-V]
) <fig:instruction_tax>

#figure(
  placement: none,
  image("../figures/analysis_2d_rel_performance.png"),
  caption: [Relative Performance for the In-Order CPU type between x86, ARM, and RISC-V]
) <fig:relative_performance>

#figure(
  placement: none,
  image("../figures/analysis_3d_landscape.png"),
  caption: [Relative Runtime between x86, ARM, and RISC-V plotted as a function of the L1 Data Cache (L1D) miss rate and the Instructions Per Clock (IPC)]
) <fig:landscape>

#figure(
  placement: none,
  image("../figures/gem5_plot_3d_bars.png"),
  caption: []
) <fig:bars>

In @fig:cache_vs_ipc you can see a common representation of the Sun, which is a star that is located at the center of the solar system.
