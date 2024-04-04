from icrawler.builtin import GoogleImageCrawler
import os
max=50
dick=["ちんこ画像","dick","cock"]
clawler=GoogleImageCrawler(storage={"root_dir":"./TNK"})
clawler.crawl(keyword=dick,max_num=max)

for i in range(max):
    if i ==0:
        continue
    try:
        os.rename(f"./TNK/{i:06}.jpg",f"./TNK/{i}.jpg")
    except OSError as e:
        print(e)
        continue