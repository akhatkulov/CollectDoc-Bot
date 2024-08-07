import zipfile
import os

def zip_files(file_paths, zip_name):
    if not os.path.exists('zips'):
        os.makedirs('zips')

    zip_path = os.path.join('zips', zip_name)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in file_paths:

            if os.path.exists(file):
                zipf.write(file, os.path.basename(file))
            else:
                print(f"Fayl mavjud emas: {file}")
    print(f"Zip fayl yaratildi: {zip_path}")
    return zip_path

# # Misol uchun foydalanish
# files = ['file1.txt', 'file2.txt', 'file3.txt']
# zip_path = zip_files(files, 'my_archive.zip')
# print(f"Zip faylning to'liq yo'li: {zip_path}")
