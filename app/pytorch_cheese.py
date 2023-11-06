import torch
import torch.nn as nn
from torchvision.models import resnet18
from PIL import Image
import numpy as np
from torchvision.transforms import transforms
from torch.nn import Linear


tfm = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(degrees=10),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class IsItCheese(nn.Module):
    def __init__(self, num_classes):
        super(IsItCheese, self).__init__()
        self.features = resnet18(pretrained=True)
        num_ftrs = self.features.fc.in_features
        self.features.fc = nn.Linear(num_ftrs, num_classes)

    def forward(self, x):
        return self.features(x)
    
    def predict(self, image_path):
        img = Image.open(image_path)
        img = img.convert('RGB')
        img_tensor = tfm(img)
        img_tensor = img_tensor[np.newaxis, :]
        img_tensor = img_tensor.to(device)
        pred_prob = self(img_tensor)
        pred = torch.max(pred_prob, 1).indices
        pred = pred.item()
        if pred == 1:
            return f"Model prediction: {pred}, hence NOT cheese!"
        else:
            return f"Model prediction: {pred}, hence cheese!"
    
is_it_cheese = IsItCheese(num_classes=2)
is_it_cheese = is_it_cheese.to(device)
is_it_cheese.fc = Linear(in_features=512, out_features=2)

is_it_cheese.load_state_dict(torch.load('app/models/is_it_cheese.pth'))

is_it_cheese.eval()
