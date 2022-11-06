import torch
import numpy as np
from torch import nn


class FarePredictor(nn.Module):
    
    def __init__(self, numeric_features, embedding_in_channels, embedding_out_channels, hidden_layers):
        super(FarePredictor, self).__init__()
        self.numeric_features = numeric_features
        self.embedding_in_channels = embedding_in_channels
        self.embedding_out_channels = embedding_out_channels
        
        self.embedding_layers = nn.ModuleList([nn.Embedding(in_channel, out_channel) for in_channel, out_channel
                                               in zip(embedding_in_channels, embedding_out_channels)])
        
        in_channel = len(numeric_features) + np.sum(embedding_out_channels)
        self.layers = []
        for out_channel in hidden_layers:
            self.layers.append(nn.Linear(in_channel, out_channel))
            self.layers.append(nn.BatchNorm1d(out_channel))
            self.layers.append(nn.ReLU())
            in_channel = out_channel
        self.layers.append(nn.Linear(out_channel, 1))
        self.layers = nn.Sequential(*self.layers)
    
    def forward(self, numeric_features, cat_features):
        cat_features = torch.cat([embedding_layer(cat_feature.squeeze(1)) for embedding_layer, cat_feature in
                                  zip(self.embedding_layers, cat_features.split(1, dim=1))], dim=1)
        features = torch.cat([numeric_features, cat_features], dim=1).float()
        return self.layers(features)