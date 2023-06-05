# Run this script from testing parent directory (PC_App)

import sys
from tabulate import tabulate
import os

# Import modules to test
sys.path.append('../PC_App')
from comp_img import compare_image
 
# Threshold to trigger succesful match
ACCEPTANCE_THRESHOLD = 0.6 

# Directories with refernce screens, camera-taken screens and
# altered screens for testing
reference_dir = 'Testing/screens'
sample_18cm_dir = 'Testing/screens_cam18'
sample_wrong18cm_dir = 'Testing/screens_cam_wrong18'
reference_dir_list = os.listdir(reference_dir)
sample_18cm_dir_list = os.listdir(sample_18cm_dir)
sample_wrong18cm_dir_list = os.listdir(sample_wrong18cm_dir)

# Dictionary to save similarity metrics for each reference image
comparisons = {k: [None, [None, None]] for k in reference_dir_list}

info = {
    'REF IMG': [f"T{i:02}.png" for i in range(1, len(reference_dir_list) + 1)],
    'TP': [],
    'TN_0': [],
    'TN_1': [],
    'FP_0': [],
    'FP_1': [],
    'FN': []
}

# Main function - entry point
def main():
    compare_similar_ims()
    compare_wrong_ims()
    print_table()

############################## HELPER FUNCTIONS ###############################

def compare_similar_ims():
    #Compare against similar images (expecting PASS)
    # Calculates True Positives and False Negatives
    for i in range(len(reference_dir_list)):
        ref_filename = os.fsdecode(reference_dir_list[i])
        if not ref_filename.endswith('.png'):
            continue
        
        # Look for sample img with matching number
        for j in range(len(sample_18cm_dir_list)):
            smp_file_name = os.fsdecode(sample_18cm_dir_list[j])
            if not smp_file_name.endswith('.png'):
                continue

            ref_num = int(ref_filename[1:3])
            smp_num = int(smp_file_name[1:3])

            if ref_num == smp_num:
                similarity = compare_image(os.path.join(sample_18cm_dir, smp_file_name), 
                                            os.path.join(reference_dir, ref_filename))
                comparisons[ref_filename][0] = similarity 

def compare_wrong_ims():
    #### Compare against dissimilar images (expecting FAIL) ####
    # Calculates True Negatives and False Positives
    for i in range(len(reference_dir_list)):
        ref_filename = os.fsdecode(reference_dir_list[i])
        if not ref_filename.endswith('.png'):
            continue
        
        # Look for sample img with matching number
        for j in range(len(sample_wrong18cm_dir_list)):
            smp_file_name = os.fsdecode(sample_wrong18cm_dir_list[j])
            if not smp_file_name.endswith('.png'):
                continue

            ref_num = int(ref_filename[1:3])
            smp_num = int(smp_file_name[1:3])

            if ref_num == smp_num:
                similarity = compare_image(os.path.join(sample_wrong18cm_dir, smp_file_name), 
                                            os.path.join(reference_dir, ref_filename))
                if smp_file_name.endswith('0.png'):
                    comparisons[ref_filename][1][0] = similarity 
                elif smp_file_name.endswith('1.png'):
                    comparisons[ref_filename][1][1] = similarity
                else: 
                    print(f"Unknown {smp_file_name}")

def print_table():
    # Initialize all confusion matrix categories to 0
    Total_TP = Total_TN = Total_FP = Total_FN = 0

    # Categorize metrics into corresponding categories
    for i in range(1, len(comparisons)+1):
        ref_name = f"T{i:02}.png"

        # Results with similar images (expecting PASS)
        if comparisons[ref_name][0] > ACCEPTANCE_THRESHOLD:
            Total_TP += 1
            table_append('TP', round(comparisons[ref_name][0], 2))
        else:
            Total_FN += 1
            table_append('FN', round(comparisons[ref_name][0], 2))

        # Results with dissimilar images (expecting FAIL)
        if comparisons[ref_name][1][0] < ACCEPTANCE_THRESHOLD:
            Total_TN += 1
            table_append('TN_0', round(comparisons[ref_name][1][0], 2))
        else: 
            Total_FP += 1
            table_append('FP_0', round(comparisons[ref_name][1][0], 2))
        if comparisons[ref_name][1][1] < ACCEPTANCE_THRESHOLD:
            Total_TN += 1
            table_append('TN_1', round(comparisons[ref_name][1][1], 2))
        else: 
            Total_FP += 1
            table_append('FP_1', round(comparisons[ref_name][1][1], 2))

    # Print results
    print(tabulate(info, headers='keys', tablefmt='fancy_grid'))
    print(f"\nPrecision: {Total_TP/(Total_TP+Total_FP):0.4f}")
    print(f"Recall: {Total_TP/(Total_TP+Total_FN):0.4f}")

# Helper function to append value to table
def table_append(key: str, val: float):
    if key == 'TP':
        info['TP'].append(val)
        info['FN'].append('')
    elif key == 'TN_0':
        info['TN_0'].append(val)
        info['FP_0'].append('')
    elif key == 'FP_0':
        info['TN_0'].append('')
        info['FP_0'].append(val)
    elif key == 'TN_1':
        info['TN_1'].append(val)
        info['FP_1'].append('')
    elif key == 'FP_1':
        info['TN_1'].append('')
        info['FP_1'].append(val)
    elif key == 'FN':
        info['TP'].append('')
        info['FN'].append(val)

if __name__ == '__main__':
    main()