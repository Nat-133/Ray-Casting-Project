import pickle

with open("last_played_level.txt","wb") as f:
    pickle.dump(1,f)
with open("last_played_level.txt","rb") as f:
    print(pickle.load(f))
