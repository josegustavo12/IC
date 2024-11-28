# Geração manual de vetores deterministicos (simulação de PODEM)
def generate_podem_vectors():
    return [
        [1, 0, 0, 0, 0],  # Vetor 1
        [0, 1, 1, 0, 0],  # Vetor 2
        [1, 1, 0, 1, 0],  # Vetor 3
        [0, 0, 1, 1, 1],  # Vetor 4
        [1, 1, 1, 1, 1]   # Vetor 5
    ]

# Salvar os vetores em arquivo
def save_vectors(vectors, filename):
    with open(filename, "w") as f:
        for vector in vectors:
            f.write(" ".join(map(str, vector)) + "\n")

if __name__ == "__main__":
    podem_vectors = generate_podem_vectors()
    save_vectors(podem_vectors, "podem_vectors.txt")

    print(f"Gerados {len(podem_vectors)} vetores PODEM.")
