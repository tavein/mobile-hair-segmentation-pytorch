import torch
from model.model import MobileHairNet
import os
from glob import glob
import matplotlib.pyplot as plt
from torchvision.utils import save_image


class Tester:
    def __init__(self, config, dataloader):
        self.batch_size = config.batch_size
        self.config = config
        self.model_path = config.checkpoint_dir
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.data_loader = dataloader
        self.num_classes = config.num_classes
        self.num_test = config.num_test
        self.test_dir = config.sample_image_dir
        self.epoch = config.epoch
        self.build_model()

    def build_model(self):
        self.net = MobileHairNet()
        self.net.to(self.device)
        self.load_model()

    def load_model(self):
        print("[*] Load checkpoint in ", str(self.model_path))
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)

        if not os.listdir(self.model_path):
            print("[!] No checkpoint in ", str(self.model_path))
            return

        model_path = os.path.join(self.model_path, f"MobileHairNet_epoch-{self.epoch-1}.pth")
        model = glob(model_path)
        model.sort()
        if not model:
            raise Exception(f"[!] No Checkpoint in {model_path}")

        self.net.load_state_dict(torch.load(model[-1], map_location=self.device))
        print(f"[*] Load Model from {model[-1]}: ")

    def test(self):
        fig = plt.figure()
        for epoch in range(int(self.num_test / self.batch_size)):
            for step, (image, mask) in enumerate(self.data_loader):
                image = image.to(self.device)
                mask = mask.to(self.device)
                criterion = self.net(image)

                subplot = fig.add_subplot(epoch + 1, 3, epoch + 1)
                subplot.imshow(
                    [image[0].cpu().numpy(), mask[0].cpu().numpy(), torch.argmax(criterion[0], 0).cpu().numpy()])
                subplot.set_xticks([])
                subplot.set_yticks([])
                print('[*] Saved sample images')
        dir_name = os.path.join(self.test_dir, "test.png")
        plt.savefig(dir_name)


