import torch
import numpy as np
from net import Net

model_state_dict = torch.load("./model.pth")
net = Net()
net.load_state_dict(model_state_dict)
net.eval()

def test_values(x, y, z):
    coordinates = np.array([x, y, z])
    prediction = net(torch.tensor(coordinates, dtype=torch.float32) / 20.0)
    angles = prediction * 360.0
    output = angles.detach().numpy()
    output = output.astype(int)
    print(output)

test_values(8, 4, 6)
test_values(6, 0, 6)
test_values(4, 0, 8)
test_values(5, -2.5, 4)
test_values(3, -1, 2)
test_values(3, 0, 7)
test_values(7, 2, 6)
test_values(2, -3, 1)
test_values(3, 3, 3)
test_values(10, 5, 6)
