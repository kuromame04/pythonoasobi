import zipfile
import os
# 0.zipってフォルダ作ってその中に重りをぶち込む
kaisuu=input("回数を入力してください:")
for i in range(int(kaisuu)):
    with zipfile.ZipFile(f"{i+1}.zip","w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zip:
        for x in range(i+1):
            zip.write(f"{x}.zip")
    print(i)
    
for i in range(int(kaisuu)):
    if not i==0:
        try:
            os.remove(f"{i}.zip")
        except:
            continue
