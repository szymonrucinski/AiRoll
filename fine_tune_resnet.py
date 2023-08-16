import torchvision.models as models
import torch.nn as nn
from trainer import train_model
import torch.optim as optim
import torch
from torch.optim import lr_scheduler
from prepare_data import prepare_data

# Parameters of newly constructed modules have requires_grad=True by default


# Create a config class
class Config:
    def __init__(self):
        self.num_epochs = 10
        self.model = models.resnet34(pretrained=True)
        self.loss = nn.CrossEntropyLoss()
        self.num_ftrs = self.model.fc.in_features
        self.optimizer = optim.SGD(self.model.fc.parameters(), lr=0.001, momentum=0.9)
        self.scheduler = lr_scheduler.StepLR(self.optimizer, step_size=7, gamma=0.1)
        self.dataloaders = prepare_data()
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


## convert class cpnfig to dictionary
# config_dict = vars(config)


config = Config()
# add fully connected layer
config.model.fc = nn.Linear(config.model.fc.in_features, 8)
## freeze all layers except the fully connected
for param in config.model.parameters():
    param.requires_grad = False
print(config.model)
model_conv = train_model(config)
