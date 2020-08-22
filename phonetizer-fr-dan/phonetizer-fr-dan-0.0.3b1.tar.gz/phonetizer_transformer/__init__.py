import math
import random
import time
import os
import numpy as np
import torch
import torch.nn as nn
from .datastore import build_iterators
from .model import build_model
from .utils import initialize_weights, epoch_time, device

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(MODULE_DIR, '..', 'data/')
SEED = 1234

def build_weights():
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.cuda.manual_seed(SEED)
    torch.backends.cudnn.deterministic = True
    train_iterator, valid_iterator, test_iterator, src, trg = build_iterators()
    model = build_model(src, trg)
    model.apply(initialize_weights)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0005)
    criterion = nn.CrossEntropyLoss(ignore_index=trg.vocab.stoi[trg.pad_token])
    n_epochs = 10
    clip = 1
    best_valid_loss = float('inf')
    for epoch in range(n_epochs):
        start_time = time.time()
        train_loss = train(model, train_iterator, optimizer, criterion, clip)
        valid_loss = evaluate(model, valid_iterator, criterion)
        end_time = time.time()
        epoch_mins, epoch_secs = epoch_time(start_time, end_time)
        if valid_loss < best_valid_loss:
            best_valid_loss = valid_loss
            torch.save(model.state_dict(), os.path.join(DATA_PATH, 'weights.pt'))
        print(f"Epoch: {epoch+1:02} | Time: {epoch_mins}m {epoch_secs}s")
        print(f"\tTrain Loss: {train_loss:.3f} | Train PPL: {math.exp(train_loss):7.3f}")
        print(f"\t Val. Loss: {valid_loss:.3f} |  Val. PPL: {math.exp(valid_loss):7.3f}")

def train(model, iterator, optimizer, criterion, clip):

    model.train()

    epoch_loss = 0

    for i, batch in enumerate(iterator):

        src = batch.ortho
        trg = batch.phon

        optimizer.zero_grad()

        output, _ = model(src, trg[:,:-1])

        #output = [batch size, trg len - 1, output dim]
        #trg = [batch size, trg len]

        output_dim = output.shape[-1]

        output = output.contiguous().view(-1, output_dim)
        trg = trg[:,1:].contiguous().view(-1)

        #output = [batch size * trg len - 1, output dim]
        #trg = [batch size * trg len - 1]

        loss = criterion(output, trg)

        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), clip)

        optimizer.step()

        epoch_loss += loss.item()

    return epoch_loss / len(iterator)

def evaluate(model, iterator, criterion):

    model.eval()

    epoch_loss = 0

    with torch.no_grad():

        for i, batch in enumerate(iterator):

            src = batch.ortho
            trg = batch.phon

            output, _ = model(src, trg[:,:-1])

            #output = [batch size, trg len - 1, output dim]
            #trg = [batch size, trg len]

            output_dim = output.shape[-1]

            output = output.contiguous().view(-1, output_dim)
            trg = trg[:,1:].contiguous().view(-1)

            #output = [batch size * trg len - 1, output dim]
            #trg = [batch size * trg len - 1]

            loss = criterion(output, trg)

            epoch_loss += loss.item()

    return epoch_loss / len(iterator)

def infer(word):
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.cuda.manual_seed(SEED)
    torch.backends.cudnn.deterministic = True
    train_iterator, valid_iterator, test_iterator, src, trg = build_iterators()
    model = build_model(src, trg)
    model.apply(initialize_weights)
    weights_path = os.path.join(DATA_PATH, 'weights.pt')
    model.load_state_dict(torch.load(weights_path, map_location=device()))
    model.eval()
    word = word.lower()
    tokens = list(word)
    tokens = [src.init_token] + tokens + [src.eos_token]

    src_indexes = [src.vocab.stoi[token] for token in tokens]

    src_tensor = torch.LongTensor(src_indexes).unsqueeze(0).to(device())

    src_mask = model.make_src_mask(src_tensor)

    with torch.no_grad():
        enc_src = model.encoder(src_tensor, src_mask)

    trg_indexes = [trg.vocab.stoi[trg.init_token]]

    # 50 is max length for seq
    for i in range(50):

        trg_tensor = torch.LongTensor(trg_indexes).unsqueeze(0).to(device())

        trg_mask = model.make_trg_mask(trg_tensor)

        with torch.no_grad():
            output, attention = model.decoder(trg_tensor, enc_src, trg_mask, src_mask)

        pred_token = output.argmax(2)[:,-1].item()

        trg_indexes.append(pred_token)

        if pred_token == trg.vocab.stoi[trg.eos_token]:
            break

    trg_tokens = [trg.vocab.itos[i] for i in trg_indexes]

    return trg_tokens[1:], attention
