import numpy as np

# Đường dẫn đến tệp văn bản cần đọc
file_path = 'TTB.txt'

# Đọc nội dung của tệp và lưu vào một mảng NumPy
data = np.genfromtxt(file_path, delimiter=',', dtype=None, names=True, encoding=None)


# In ra nội dung đọc được
print("Nội dung của file:")
print(data[0])
