import hashlib
import sys


inputlink=input("file pass please\n")
inputlink2=input("2nd file pass please\n")
# 関数定義
def tryinput(inputlinklocal):
    try:
        
        link=open(inputlinklocal,mode="rb")
        
    except OSError as e:
        print(e)
    else:
        data=link.read()
        
        hashout=hashlib.sha256(data).hexdigest()
        link.close()
        return hashout

hashout=tryinput(inputlink)
hashout2=tryinput(inputlink2)
print(hashout,"\n")
print(hashout2,"\n")

if hashout==hashout2:
    print("ファイルは正常です。")
else:
    print("ファイルは異常です。")


