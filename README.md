# mobile-hair-segmentation-pytorch
This repository is part of a program for previewing your own dyeing on mobile device.
To do this, you need to separate the hair from the head.
And we have to use as light model as MobileNet to use in mobile device in real time.
So we borrowed the model structure from the following article.  
  
[Real-time deep hair matting on mobile devices](https://arxiv.org/abs/1712.07168) 

## model architecture
![network_architecture](./image/network_architecture.PNG)   
This model is based on MobileNet.  
To do semantic segmentation they transform MobileNet like SegNet.
And add additional loss function to capture fine hair texture.
## preparing datsets
make directory like this
```
data
   |__ images
   |
   |__ masks
   
```
expected image name  
The name of the expected image pair is:  
```
 - data/images/1.jpg 
| 
 - data/masks/1.jpg  
```
## how to train
run main
```
python main.py
```
``` python
from src.train import Trainer
from data.dataloader import get_loader
from config.config import get_config

config = get_config()
data_loader = get_loader(config.data_path, config.batch_size, config.image_size,
                        shuffle=True, num_workers=int(config.workers))
trainer = Trainer(config, data_loader)
```

## Overall result
it use argmax function to get mask  

![network_architecture](./image/sample_image.PNG)
![network_architecture](./image/webcam.gif)
