import torch
from torch import nn as nn
import torch.nn.functional as F
from torch import optim as optim
from torch.distributions.kl import kl_divergence
from torch.distributions.normal import Normal


class LinearRegression(nn.Module):
    def __init__(self, in_dim, out_dim):
        super(LinearRegression, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(in_dim, out_dim),
            nn.Sigmoid()
        )

        self.loss_function = nn.NLLLoss()

    def forward(self, x):
        return self.fc(x)


# ========================================================
# Multilayer VAE
# ========================================================
class VAEMNIST(nn.Module):
    def __init__(self, x_dim, h_dim1, h_dim2, z_dim):
        super(VAEMNIST, self).__init__()

        # encoder part
        self.fc1 = nn.Linear(x_dim, h_dim1)
        self.fc2 = nn.Linear(h_dim1, h_dim2)
        self.fc31 = nn.Linear(h_dim2, z_dim)
        self.fc32 = nn.Linear(h_dim2, z_dim)
        # decoder part
        self.fc4 = nn.Linear(z_dim, h_dim2)
        self.fc5 = nn.Linear(h_dim2, h_dim1)
        self.fc6 = nn.Linear(h_dim1, x_dim)

    def encoder(self, x):
        h = F.relu(self.fc1(x))
        h = F.relu(self.fc2(h))
        return self.fc31(h), self.fc32(h)  # mu, log_var

    def sampling(self, mu, log_var):
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        return eps.mul(std).add_(mu)  # return z sample

    def decoder(self, z):
        h = F.relu(self.fc4(z))
        h = F.relu(self.fc5(h))
        return F.sigmoid(self.fc6(h))

    def forward(self, x):
        mu, log_var = self.encoder(x)
        z = self.sampling(mu, log_var)
        return self.decoder(z), mu, log_var

    @staticmethod
    def loss_function(prediction, x):
        recon_x, mu, log_var = prediction
        BCE = F.binary_cross_entropy(recon_x, x.view(-1, 784), reduction='sum')
        KLD = -0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp())
        return BCE + KLD


# ========================================================
# Linear VAE
# ========================================================
class VAE(nn.Module):
    """ Variational autoencoder (Single Layer)"""

    def __init__(self, in_dim, z_dim):
        super(VAE, self).__init__()

        # Encoder
        self.mu_enc = nn.Linear(in_dim, z_dim)
        self.logvar_enc = nn.Linear(in_dim, z_dim)

        # Decoder
        self.mu_dec = nn.Linear(z_dim, in_dim)
        self.logvar_dec = nn.Parameter(torch.rand(in_dim))

    def encode(self, x):
        # Standardization
        mu = self.mu_enc(x)
        std = self.logvar_enc(x).exp().pow(0.5)
        return Normal(loc=mu, scale=std)

    def decode(self, z):
        mu = self.mu_dec(z)
        std = self.logvar_dec.exp().pow(0.5)
        return Normal(loc=mu, scale=std)

    def generate(self, z):
        return self.decode(z)

    def reconstruct(self, x):
        q = self.encode(x)
        z = q.rsample()
        recon = self.mu_dec(z)
        return recon

    def forward(self, x):
        q = self.encode(x)
        z = q.rsample()
        p = self.decode(z)  # Reconstruction

        return p, q

    @staticmethod
    def loss_function(prediction, target):
        """
        Loss function for VAE.
        :param prediction: Reconstruction distribution (p) and latent space distribution (q)
        :param torch.Tensor target: Input distribution
        :return: Reconstruction loss + KL Divergence
        """
        p, q = prediction

        # Compute Log-likelihood
        ll = p.log_prob(target).sum(-1).mean()

        # Compute KL
        prior = Normal(0, 1)
        kl = kl_divergence(q, prior).sum(-1).mean()

        return kl - ll


class ModelPipeline(nn.Module):
    def __init__(self, in_dim, out_dim, z_dim=2, model_name='linear_regression', **kwargs):
        super(ModelPipeline, self).__init__()

        self.model = self.get_model(in_dim, out_dim, model_name, z_dim, **kwargs)

        # Historic
        self.train_loss = []

    def get_model(self, in_dim, out_dim, model_name, z_dim, **kwargs):
        model_name = model_name.lower()  # A bit of robustness
        if model_name == 'linear_regression':
            return LinearRegression(in_dim=in_dim, out_dim=out_dim)
        elif model_name == 'vae':
            return VAE(in_dim=in_dim, z_dim=z_dim)
        elif model_name == 'vae_mnist':
            return VAEMNIST(x_dim=in_dim, z_dim=z_dim, **kwargs)
        else:
            raise NotImplementedError(f'Model {model_name} is not implemented in this version.')

    def log_loss(self, loss):
        self.train_loss.append(loss.item())

    def forward(self, x):
        return self.model(x)

    def fit(self, data_loader, epochs, lr=1e-4):
        optimizer = optim.Adam(self.model.parameters(), lr=lr)

        for epoch in range(epochs):
            for data, target in data_loader:
                optimizer.zero_grad()

                pred = self.model(data)
                loss = self.model.loss_function(pred, target)
                loss.backward()

                self.log_loss(loss)
                optimizer.step()
