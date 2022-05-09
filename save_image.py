import os
import requests
import matplotlib.pyplot as plt

def download_images(save_dir,name, urls):
  start_index = 0
  image_names = []
  i = 0
  while i < len(urls):
    try:
        image_name = f'{name}_{str(i)}.jpg'
        image_path = os.path.join(save_dir, image_name)
        result = requests.get(urls[i], timeout=60)

        with open(image_path, 'wb') as f:
            f.write(result.content)
            f.close()
        try:
            plt.imread(image_path)
            image_names.append(image_name)
            start_index += 1
            i += 1
        except:
            # print('[DELETE] Image has no contents -', image_name)
            os.remove(image_path)
            urls.remove(urls[i])
    except:
        # print('[ERROR] Failed to request -', image_name, '-', urls[i])
        urls.remove(urls[i])