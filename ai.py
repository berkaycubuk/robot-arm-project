import torch
import pandas as pd
from net import Net

# Load data from CSV file
data = pd.read_csv('./data.csv')

# Extract servo angles and corresponding x y z coordinates
servo_angles = torch.tensor(data.iloc[:, :3].values, dtype=torch.float32)
coordinates = torch.tensor(data.iloc[:, 3:].values, dtype=torch.float32)

# Normalize servo angles to range [0, 1]
servo_angles = servo_angles / 360.0

# Normalize coordinates to range [-1, 1]
coordinates = coordinates / 20.0

# Instantiate neural network and optimizer
net = Net()
optimizer = torch.optim.Adam(net.parameters(), lr=0.01)

# Define loss function
loss_fn = torch.nn.MSELoss()

# Train neural network
for i in range(10000):
    optimizer.zero_grad()
    predicted_angles = net(coordinates)
    loss = loss_fn(predicted_angles, servo_angles)
    loss.backward()
    optimizer.step()

    if i % 1000 == 0:
        print(f'Epoch {i}, loss: {loss.item()}')

torch.save(net.state_dict(), "model.pth")
