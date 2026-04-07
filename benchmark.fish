#!/usr/bin/fish

# Define colors
set color_header cyan
set color_success green
set color_warning yellow
set color_error red
set color_reset normal

set isas x86 arm riscv sparc power mips
set cpus o3 in-order
set binaries bc bfs cc cc_sv converter pr pr_spmv sssp tc

for isa in $isas
    set folder ""
    switch $isa
        case x86;   set folder "x86"
        case arm;   set folder "ARM"
        case riscv; set folder "RISCV"
        case sparc; set folder "SPARC"
        case power; set folder "PowerPC"
        case mips;  set folder "MIPS"
    end

    for cpu in $cpus
        for bin in $binaries
            set binary_path "GAPBS/$folder/$bin"
            
            if test -f $binary_path
                set_color $color_header --bold
                echo "Running: ISA=$isa | CPU=$cpu | Binary=$bin..."
                set_color $color_reset

                # --- SILENT RUN ---
                # &>/dev/null redirects both standard output and standard error to nothing
                gem5 main.py --isa $isa --mem ddr5 --cpu $cpu --binary $binary_path &>/dev/null

                # --- CHECK STATUS CODE ---
                if test $status -eq 0
                    set new_filename "gapbs_"$isa"_"$bin"_"$cpu"_ddr5_stats.txt"
                    
                    if test -f "m5out/stats.txt"
                        mv m5out/stats.txt "GAPBS/$folder/$new_filename"
                        set_color $color_success
                        echo "Simulation Successful: Saved to $new_filename"
                        set_color $color_reset
                    else
                        set_color $color_warning
                        echo "Warning: gem5 exited 0, but stats.txt is missing."
                        set_color $color_reset
                    end
                else
                    set_color $color_error --bold
                    echo "Error: gem5 crashed with exit code $status"
                    set_color $color_reset
                end
            end
        end
    end
end

set_color green --bold
echo "All simulations complete."
set_color $color_reset
