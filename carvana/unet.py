import torch.nn.functional as F

from torch import nn

class conv_block(nn.Module):
    def __init__(self, in_size, out_size, kernel_size = 3, padding = 1, stride = 1):
        super(conv_block, self).__init__()
        self.conv = nn.Conv2d(in_size, out_size, kernel_size, padding = padding, stride = stride)
        self.bn = nn.BatchNorm2d(out_size)
        self.relu = nn.ReLU(inplace = True)

    def forward(self, x):
        return self.relu(self.bn(self.conv(x)))

class unet_256(nn.Module):
    '''Input 256 x 256 image'''
    def __init__(self):
        super(unet_256, self).__init__()

        self.down_1 = nn.Sequential(
            conv_block(3, 16),
            conv_block(16, 32, stride = 2, padding = 1)
        )

        self.down_2 = nn.Sequential(
            conv_block(32, 64),
            conv_block(64, 128)
        )
        
        self.down_3 = nn.Sequential(
            conv_block(128, 256),
            conv_block(256, 512)
        )

        self.down_4 = nn.Sequential(
            conv_block(512, 512),
            conv_block(512, 512)
        )

        self.middle = conv_block(512, 512, kernel_size = 1, padding = 0)

        self.up_4 = nn.Sequential(
            conv_block(1024, 512),
            conv_block(512, 512)
        )

        self.up_3 = nn.Sequential(
            conv_block(1024, 512),
            conv_block(512, 128)
        )

        self.up_2 = nn.Sequential(
            conv_block(256, 128),
            conv_block(128, 32)
        )

        self.up_1 = nn.Sequential(
            conv_block(64, 64),
            conv_block(64, 32)
        )

        self.output = nn.Sequential(
            conv_block(32, 16),
            conv_block(16, 1, kernel_size = 1, padding = 0)
        )

    def forward(self, x):
        down1 = self.down_1(x)
        out = F.max_pool2d(down1, kernel_size = 2, stride = 2)

        down2 = self.down_2(out)
        out = F.max_pool2d(down2, kernel_size = 2, stride = 2)

        down3 = self.down_3(out)
        out = F.max_pool2d(down3, kernel_size = 2, stride = 2)

        down4 = self.down_4(out)
        out = F.max_pool2d(down4, kernel_size = 2, stride = 2)

        out = self.middle(out)

        out = F.upsample(out, scale_factor = 2)
        out = toch.cat([down4, out], 1)
        out = self.up4(out)

        out = F.upsample(out, scale_factor = 2)
        out = torch.cat([down3, out], 1)
        out = self.up_3(out)

        out = F.upsample(out, scale_factor = 2)
        out = torch.cat([down2, out], 1)
        out = self.up_2(out)

        out = F.upsample(out, scale_factor = 2)
        out = torch.cat([down1, out], 1)
        out = self.up_1(out)

        out = F.upsample(out, scale_factor = 2)
        return self.output(out)