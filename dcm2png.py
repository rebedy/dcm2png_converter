# coding: utf-8

import os
import shutil
from PIL import Image
import pandas as pd
import SimpleITK as sitk

# ### Making matching list ###
print("Start making Matching-List")
matching = pd.read_excel('matching.xlsx', index_col=None, header=None)

# Drop irrelevant columns
matching = matching.drop(matching.columns[0], axis=1)
matching = matching.drop(matching.columns[1:5], axis=1)
matching = matching[1:]
index_col = matching.columns[0]

# Make drop list to drop irrelevant rows except row named 'IVUS Frame'.
# drop list contains the index numbers to be dropped.
drop_list = []
for i in range(len(matching.index)):
    if matching.isnull()[index_col].tolist()[i]:
        drop_list.append(i + 1)

# Drop the rows in the drop_list.
for n in drop_list:
    matching = matching.drop(n)

# Column 'no' is set as index and fill NaN with 0.
matching = matching.set_index(index_col)
matching = matching.fillna(0)

# print(matching)
# exit()


# ### Extract matching list of images we want to see in excel file ###
def extract_matching_list(img_name):
    """
    img_name: str, name of the image file
    return: list, list of the matching list of the image
    """
    patient_id = img_name[:4]
    matching_list = matching.loc[patient_id].tolist()[1:]
    matching_list = [int(i) for i in matching_list]
    return matching_list


print("Done making Matching-LIst")


# #### Convert images in the matching list ###
dcm_path = './original_images/'
output_path = './png_images/'
dcms = os.listdir(dcm_path)

print("Start Extracting Dicom Files!\n\n")
for dcm_file in dcms:
    print("..... " + dcm_file + " working on")
    dicom = dcm_path + dcm_file
    patient_no = dcm_file[:-4]
    folder_name = patient_no[:4]

    dicom = sitk.ReadImage(dicom)
    dcm2Array = sitk.GetArrayFromImage(dicom)

    img_n = dcm2Array.shape[0]
    # Show progress.
    for i in range(img_n):
        if i % 700 == 0:
            print(str(int(i / img_n * 100)) + "% Done..")

        # Make folder for each patient.
        if not os.path.exists(output_path + folder_name):
            os.makedirs(output_path + folder_name)

        matching_list = extract_matching_list(patient_no)
        if i + 1 in matching_list:
            img_convert = dcm2Array[i]
            # Image save
            img = Image.fromarray(img_convert)
            img.save(output_path + folder_name + '/' + str(i + 1) + '_' + folder_name + ".png")


    print('....Converting is Done !!!')

    shutil.copy(dcm_path + dcm_file, output_path + folder_name + '/' + dcm_file)
    print('....And dicom file is IN !!!\n')

print('\n<<<<<<<<<<ALL DONE>>>>>>>>>>')
