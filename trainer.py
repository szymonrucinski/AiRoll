### Section 1 - First, let's import everything we will be needing.

from __future__ import print_function, division
import torch
import torch.utils.data
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from torchvision import models, transforms
import time
import copy
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
DECAY_WEIGHT = 0.1
NUM_CLASSES = 8
### SECTION 2 - data loading and shuffling/augmentation/normalization : all handled by torch automatically.

# This is a little hard to understand initially, so I'll explain in detail here!

# For training, the data gets transformed by undergoing augmentation and normalization.
# The RandomSizedCrop basically takes a crop of an image at various scales between 0.01 to 0.8 times the size of the image and resizes it to given number
# Horizontal flip is a common technique in computer vision to augment the size of your data set. Firstly, it increases the number of times the network gets
# to see the same thing, and secondly it adds rotational invariance to your networks learning.


# Just normalization for validation, no augmentation.

# You might be curious where these numbers came from? For the most part, they were used in popular architectures like the AlexNet paper.
# It is important to normalize your dataset by calculating the mean and standard deviation of your dataset images and making your data unit normed. However,
# it takes a lot of computation to do so, and some papers have shown that it doesn't matter too much if they are slightly off. So, people just use imagenet
# dataset's mean and standard deviation to normalize their dataset approximately. These numbers are imagenet mean and standard deviation!

# If you want to read more, transforms is a function from torchvision, and you can go read more here - http://pytorch.org/docs/master/torchvision/transforms.html
data_transforms = {
    "train": transforms.Compose(
        [
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    ),
    "val": transforms.Compose(
        [
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    ),
}


# Enter the absolute path of the dataset folder below. Keep in mind that this code expects data to be in same format as Imagenet. I encourage you to
# use your own dataset. In that case you need to organize your data such that your dataset folder has EXACTLY two folders. Name these 'train' and 'val'
# Yes, this is case sensitive. The 'train' folder contains training set and 'val' fodler contains validation set on which accuracy is measured.

# The structure within 'train' and 'val' folders will be the same. They both contain one folder per class. All the images of that class are inside the
# folder named by class name.

# So basically, if your dataset has 3 classes and you're trying to classify between pictures of 1) dogs 2) cats and 3) humans,
# say you name your dataset folder 'data_directory'. Then inside 'data_directory' will be 'train' and 'test'. Further, Inside 'train' will be
# 3 folders - 'dogs', 'cats', 'humans'. All training images for dogs will be inside this 'dogs'. Similarly, within 'val' as well there will be the same
# 3 folders.

## So, the structure looks like this :
# data_dar
#      |- train
#            |- dogs
#                 |- dog_image_1
#                 |- dog_image_2
#                        .....

#            |- cats
#                 |- cat_image_1
#                 |- cat_image_1
#                        .....
#            |- humans
#      |- val
#            |- dogs
#            |- cats
#            |- humans


from datasets import load_dataset


dataset = load_dataset("szymonrucinski/types-of-film-shots")
dataset = dataset.with_format("torch")
# train_dset_loader = torch.utils.data.DataLoader(dataset["train"], batch_size=32)
# valid_dset_loader = torch.utils.data.DataLoader(dataset["train"], batch_size=32)
# dset_loaders = {"train": train_dset_loader, "val": valid_dset_loader}
# transforms.RandomResizedCrop(224)
from prepare_data import prepare_data

prepare_data()
### SECTION 3 : Writing the functions that do training and validation phase.

# These functions basically do forward propogation, back propogation, loss calculation, update weights of model, and save best model!


## The below function will train the model. Here's a short basic outline -

# For the number of specified epoch's, the function goes through a train and a validation phase. Hence the nested for loop.

# In both train and validation phase, the loaded data is forward propogated through the model (architecture defined ahead).
# In PyTorch, the data loader is basically an iterator. so basically there's a get_element function which gets called everytime
# the program iterates over data loader. So, basically, get_item on dset_loader below gives data, which contains 2 tensors - input and target.
# target is the class number. Class numbers are assigned by going through the train/val folder and reading folder names in alphabetical order.
# So in our case cats would be first, dogs second and humans third class.

# Forward prop is as simple as calling model() function and passing in the input.

# Variables are basically wrappers on top of PyTorch tensors and all that they do is keep a track of every process that tensor goes through.
# The benefit of this is, that you don't need to write the equations for backpropogation, because the history of computations has been tracked
# and pytorch can automatically differentiate it! Thus, 2 things are SUPER important. ALWAYS check for these 2 things.
# 1) NEVER overwrite a pytorch variable, as all previous history will be lost and autograd won't work.
# 2) Variables can only undergo operations that are differentiable.


def train_model(model, criterion, optimizer, lr_scheduler, num_epochs=100):
    time.time()

    best_model = model
    best_acc = 0.0

    for epoch in range(num_epochs):
        print("Epoch {}/{}".format(epoch, num_epochs - 1))
        print("-" * 10)

        # Each epoch has a training and validation phase
        for phase in ["train", "val"]:
            if phase == "train":
                optimizer = lr_scheduler(optimizer, epoch)
                model.train()  # Set model to training mode
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            counter = 0
            # Iterate over data.
            for data in dset_loaders[phase]:
                inputs, labels = data
                print(inputs.shape, labels.shape)
                # wrap them in Variable
                inputs, labels = (Variable(inputs.float().cuda()),)
                Variable(labels.long().cuda())
                print(inputs, labels)

                # Set gradient to zero to delete history of computations in previous epoch. Track operations so that differentiation can be done automatically.
                optimizer.zero_grad()
                outputs = model(inputs)
                _, preds = torch.max(outputs.data, 1)

                loss = criterion(outputs, labels)
                # print('loss done')
                # Just so that you can keep track that something's happening and don't feel like the program isn't running.
                # if counter%10==0:
                #     print("Reached iteration ",counter)
                counter += 1

                # backward + optimize only if in training phase
                if phase == "train":
                    # print('loss backward')
                    loss.backward()
                    # print('done loss backward')
                    optimizer.step()
                    # print('done optim')
                # print evaluation statistics
                try:
                    # running_loss += loss.data[0]
                    running_loss += loss.item()
                    # print(labels.data)
                    # print(preds)
                    running_corrects += torch.sum(preds == labels.data)
                    # print('running correct =',running_corrects)
                except:
                    print("unexpected error, could not calculate loss or do a sum.")
            print("trying epoch loss")
            epoch_loss = running_loss / dset_sizes[phase]
            epoch_acc = running_corrects.item() / float(dset_sizes[phase])
            print("{} Loss: {:.4f} Acc: {:.4f}".format(phase, epoch_loss, epoch_acc))

            # deep copy the model
            if phase == "val":
                if USE_TENSORBOARD:
                    foo.add_scalar_value("epoch_loss", epoch_loss, step=epoch)
                    foo.add_scalar_value("epoch_acc", epoch_acc, step=epoch)
                if epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model = copy.deepcopy(model)
                    print("new best accuracy = ", best_acc)
    print("Best val Acc: {:4f}".format(best_acc))
    print("returning and looping back")
    return best_model


# This function changes the learning rate over the training model.
def exp_lr_scheduler(optimizer, epoch, init_lr=0.001, lr_decay_epoch=30):
    """Decay learning rate by a factor of DECAY_WEIGHT every lr_decay_epoch epochs."""
    lr = init_lr * (DECAY_WEIGHT ** (epoch // lr_decay_epoch))

    if epoch % lr_decay_epoch == 0:
        print("LR is set to {}".format(lr))

    for param_group in optimizer.param_groups:
        param_group["lr"] = lr

    return optimizer


### SECTION 4 : DEFINING MODEL ARCHITECTURE.

# We use Resnet18 here. If you have more computational power, feel free to swap it with Resnet50, Resnet100 or Resnet152.
# Since we are doing fine-tuning, or transfer learning we will use the pretrained net weights. In the last line, the number of classes has been specified.
# Set the number of classes in the config file by setting the right value for NUM_CLASSES.

model_ft = models.resnet18(pretrained=True)
num_ftrs = model_ft.fc.in_features
model_ft.fc = nn.Linear(num_ftrs, NUM_CLASSES)


criterion = nn.CrossEntropyLoss()
criterion.cuda()
model_ft.cuda()
optimizer_ft = optim.RMSprop(model_ft.parameters(), lr=0.0001)

# Run the functions and save the best model in the function model_ft.
model_ft = train_model(
    model_ft, criterion, optimizer_ft, exp_lr_scheduler, num_epochs=100
)

# Save model
model_ft.save_state_dict("fine_tuned_best_model.pt")
