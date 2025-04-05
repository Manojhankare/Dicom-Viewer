import matplotlib.pyplot as plt
import pydicom

# Load the DICOM file
ds = pydicom.dcmread('0003.dcm')

# Extract pixel data and metadata
pixel_data = ds.pixel_array
patient_name = ds.PatientName

# Display the image
plt.imshow(pixel_data, cmap='gray')

plt.show()
