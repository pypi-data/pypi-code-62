from .encoder import Encoder
from .decoder import Decoder
from .sequence_to_sequence import Seq2Seq
from ..utils import device

HID_DIM = 256
ENC_LAYERS = 3
DEC_LAYERS = 3
ENC_HEADS = 4
DEC_HEADS = 4
ENC_PF_DIM = 512
DEC_PF_DIM = 512
ENC_DROPOUT = 0.2
DEC_DROPOUT = 0.2

def build_model(src, trg):
    input_dim = len(src.vocab)
    output_dim = len(trg.vocab)
    enc = Encoder(input_dim,
                HID_DIM,
                ENC_LAYERS,
                ENC_HEADS,
                ENC_PF_DIM,
                ENC_DROPOUT,
                device())

    dec = Decoder(output_dim,
                HID_DIM,
                DEC_LAYERS,
                DEC_HEADS,
                DEC_PF_DIM,
                DEC_DROPOUT,
                device())

    src_pad_idx = src.vocab.stoi[src.pad_token]
    trg_pad_idx = trg.vocab.stoi[trg.pad_token]

    model = Seq2Seq(enc, dec, src_pad_idx, trg_pad_idx, device()).to(device())

    return model
