import numpy
import cv2
f=open(r"./result.txt",mode="w")
path=r"rickroll.mp4"
array=cv2.VideoCapture(f"{path}")
framearray=[]
frame_spilit=15
x_split=20
y_split=20
if  array.isOpened():
    frame_count=0
    while True:
        frame_count+=1 # Numpy配列にしたけりゃ弄ってね
        ret,frames=array.read()
        try:
            frame=frames.tolist()
        except:
            break
        if ret==False:
            break
        if array.get(cv2.CAP_PROP_POS_FRAMES) %frame_spilit==0:
            dataarray=[]
            for i,data in enumerate(frame):
                if i %y_split==0:
                    pixelarray=[]
                    for r,datax in enumerate(data):
                        if r %x_split==0:
                            R,G,B=frame[i][r]
                            if R >=128 or G >=128 or B >=128:
                                frame[i][r]=[0,0,0]
                                pixelarray.append(frame[i][r])
                            elif R <=128 or G <=128 or B <=128:
                                frame[i][r]=[255,255,255]
                                pixelarray.append(frame[i][r])
                    dataarray.append(pixelarray); print(f"{(frame_count/15)}  {str(len(pixelarray))}") # framearray[frame]dataarray[y][pixel] | framearray[][][]
            framearray.append(dataarray)
    f.write(str(framearray))
    f.close()
            
else:
    print("error")
            
            
    
                    
                            
                                
                        
                                
                                




