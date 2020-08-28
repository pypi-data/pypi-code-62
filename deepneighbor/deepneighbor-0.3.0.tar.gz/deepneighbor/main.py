import pandas as pd
import embed
from embed import Embed

if __name__ == "__main__":
    data_path = 'datasets/processed_data.csv'
    emb = Embed(data_path,model = 'gat',)
    emb.train(epochs=1)
    print("Trained")
    #print(emb.sentences)
    #emb.get_embeddings().shape
    print(emb.search('7443',k=10))
    print(len(emb.get_embeddings()['7443']))

    print("Found!")
    #return embed.get_embeddings()
