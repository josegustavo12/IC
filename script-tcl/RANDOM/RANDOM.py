import itertools
import random

# Gerar vetores RANDOM
def generate_random_vectors(num_vectors, num_inputs):
    return [[random.randint(0, 1) for _ in range(num_inputs)] for _ in range(num_vectors)]

# Salvar os vetores em arquivo
def save_vectors(vectors, filename):
    with open(filename, "w") as f:
        for vector in vectors:
            f.write(" ".join(map(str, vector)) + "\n")

if __name__ == "__main__":
    # Configurações do circuito C17
    NUM_INPUTS = 5  # C17 tem 5 entradas
    NUM_RANDOM_VECTORS = 20  # N�mero de vetores RANDOM

    # Geração de vetores RANDOM
    random_vectors = generate_random_vectors(NUM_RANDOM_VECTORS, NUM_INPUTS)
    save_vectors(random_vectors, "random_vectors.txt")

    print(f"Gerados {NUM_RANDOM_VECTORS} vetores RANDOM.")
