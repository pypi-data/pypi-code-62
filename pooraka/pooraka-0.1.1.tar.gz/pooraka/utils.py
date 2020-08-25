import torch
import torch.utils
import torchvision.datasets as dset
import torchvision.transforms as transforms

def calculate_mean_std(input_path, input_size=256, input_crop=224, batch_size=64, num_workers=8):
    dataset = dset.ImageFolder(input_path, transform=transforms.Compose([transforms.Resize(input_size),
                                transforms.CenterCrop(input_crop),
                                transforms.ToTensor()]))

    loader = torch.utils.data.DataLoader(dataset,
                            batch_size=batch_size,
                            num_workers=num_workers,
                            shuffle=False)

    mean = 0.
    std = 0.
    for images, _ in loader:
        batch_samples = images.size(0)
        images = images.view(batch_samples, images.size(1), -1)
        mean += images.mean(2).sum(0)
        std += images.std(2).sum(0)

    mean /= len(loader.dataset)
    std /= len(loader.dataset)
    return mean, std