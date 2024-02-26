"""Taller evaluable presencial"""

import pandas as pd


def load_data(input_file):
    """Lea el archivo usando pandas y devuelva un DataFrame"""
    data = pd.read_csv(input_file,sep="\t")
    return data


def create_key(df, n):
    """Cree una nueva columna en el DataFrame que contenga el key de la columna 'text'"""

    df = df.copy()

    # Copie la columna 'text' a la columna 'key'
    df["key"] = df["text"]
    # Remueva los espacios en blanco al principio y al final de la cadena
    # Convierta el texto a minúsculas
    # Transforme palabras que pueden (o no) contener guiones por su version sin guion.
    # Remueva puntuación y caracteres de control
    # Convierta el texto a una lista de tokens
    # Una el texto sin espacios en blanco
    # Convierta el texto a una lista de n-gramas
    # Ordene la lista de n-gramas y remueve duplicados
    # Convierta la lista de ngramas a una cadena
    df["key"] = (
        df["key"]
        .str.strip()
        .str.lower()
        .str.replace("-", "")
        .str.replace(".", "")
        .str.split()
        .str.join("")
        .apply(lambda x: [x[i:i+n] for i in range(len(x) - n + 1)])
        .apply(lambda x: "".join(sorted(set(x))))    
    )
    
    return df


def generate_cleaned_column(df):
    """Crea la columna 'cleaned' en el DataFrame"""

    df = df.copy()

    # Ordene el dataframe por 'key' y 'text'
    df = df.sort_values(by=["key", "text"])
    # Seleccione la primera fila de cada grupo de 'key'
    keys = df.groupby("key").first().reset_index()
    # Cree un diccionario con 'key' como clave y 'text' como valor
    keys = keys.set_index("key")["text"].to_dict()
    # Cree la columna 'cleaned' usando el diccionario
    df["cleaned"] = df["key"].map(keys)

    return df


def save_data(df, output_file):
    """Guarda el DataFrame en un archivo"""

    df = df.copy()
    df = df[["cleaned"]]
    df = df.rename(columns={"cleaned": "text"})
    df.to_csv(output_file, index=False)


def main(input_file, output_file, n=2):
    """Ejecuta la limpieza de datos"""

    df = load_data(input_file)
    df = create_key(df, n)
    df = generate_cleaned_column(df)
    df.to_csv("test.csv", index=False)
    save_data(df, output_file)


if __name__ == "__main__":
    main(
        input_file="input.txt",
        output_file="output.txt",
    )
