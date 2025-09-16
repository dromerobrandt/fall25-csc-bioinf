#!/bin/bash
set -euo pipefail

# Create header for the output table
echo -e "Dataset \tLanguage\tRuntime \tN50"
echo "-------------------------------------------------------------------------------------------------------"

# Directory containing the code
CODE_DIR="../code"

# Loop through datasets data1 to data4
for dataset in data1 data2 data3 data4; do
    # Test Python version
    start_time=$(date +%s)
    cd "$CODE_DIR"
    echo "works1"
    python_output=$(python main.py "$dataset" 2>&1)
    echo "works2"
    end_time=$(date +%s)
    cd - > /dev/null
    echo "works3"
    # Calculate runtime for Python
    python_runtime=$((end_time - start_time))
    python_minutes=$((python_runtime / 60))
    python_seconds=$((python_runtime % 60))
    python_time_str=$(printf "%02d:%02d" $python_minutes $python_seconds)
    
    # Extract contig lengths and calculate N50 for Python
    python_lengths=$(echo "$python_output" | grep -E "^[0-9]+ [0-9]+$" | awk '{print $2}' | sort -nr)
    python_total_length=$(echo "$python_lengths" | awk '{sum += $1} END {print sum}')
    python_half_length=$((python_total_length / 2))
    echo "works4"
    python_n50=0
    python_current_length=0
    for length in $python_lengths; do
        python_current_length=$((python_current_length + length))
        if [ $python_current_length -ge $python_half_length ]; then
            python_n50=$length
            break
        fi
    done
    echo "works5"
    # Test Codon version
    start_time=$(date +%s)
    cd "$CODE_DIR"
    echo "works6"
    codon_output=$(./main "$dataset" 2>&1)
    end_time=$(date +%s)
    cd - > /dev/null
    echo "works7"
    # Calculate runtime for Codon
    codon_runtime=$((end_time - start_time))
    codon_minutes=$((codon_runtime / 60))
    codon_seconds=$((codon_runtime % 60))
    codon_time_str=$(printf "%02d:%02d" $codon_minutes $codon_seconds)
    
    # Extract contig lengths and calculate N50 for Codon
    codon_lengths=$(echo "$codon_output" | grep -E "^[0-9]+ [0-9]+$" | awk '{print $2}' | sort -nr)
    codon_total_length=$(echo "$codon_lengths" | awk '{sum += $1} END {print sum}')
    codon_half_length=$((codon_total_length / 2))
    
    codon_n50=0
    codon_current_length=0
    for length in $codon_lengths; do
        codon_current_length=$((codon_current_length + length))
        if [ $codon_current_length -ge $codon_half_length ]; then
            codon_n50=$length
            break
        fi
    done
    
    # Print results for this dataset
    echo -e "$dataset \t \tpython \t\t$python_time_str \t\t$python_n50"
    echo -e "$dataset \t \tcodon \t\t$codon_time_str \t\t$codon_n50"
done