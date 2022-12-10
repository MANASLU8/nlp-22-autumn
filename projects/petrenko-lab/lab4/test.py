import pickle


# with open("../assets/vectorized_train", "rb") as file:
#     vectorized_train = pickle.load(file)
# print(vectorized_train[50])
# print(len(vectorized_train[59]))

with open("../assets/vectorized_train_prev_stage", "rb") as file:
    matrix = pickle.load(file)
print(len(matrix))
