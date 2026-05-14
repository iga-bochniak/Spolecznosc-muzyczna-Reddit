import pandas as pd
import glob
import os
import numpy as np


# ścieżka do folderu
folder = r"C:\Users\Admin\Desktop\TSMASS\Spolecznosc-muzyczna-Reddit\jsonl files"

# kolumny które chcemy zostawić
kolumny = [
    "author",
    "over_18",
    "title",
    "body",
    "created_utc",
    "id",
    "link_id",
    "parent_id",
    "subreddit",
    "subreddit_id",
    "subreddit_type",
    "name",
    "ups",
    "downs",
    "score",
    "reddit_name_prefix",
    "link_flair_text"
]

# pobranie plików
pliki = glob.glob(os.path.join(folder, "*.jsonl"))

lista_df = []

for plik in pliki:
    temp_df = pd.read_json(plik, lines=True)

    # zostaw tylko wybrane kolumny
    temp_df = temp_df.reindex(columns=kolumny)

    # nazwa pliku bez rozszerzenia
    nazwa_pliku = os.path.splitext(os.path.basename(plik))[0]

    # dodaj kolumnę z pochodzeniem
    temp_df["plik"] = nazwa_pliku

    lista_df.append(temp_df)

# połącz wszystko
data = pd.concat(lista_df, ignore_index=True)


data["type"] = data["plik"].str.split("_").str[2]
data["subreddit"] = data["plik"].str.split("_").str[1]
del data["plik"]
data["created_date"] = pd.to_datetime(
    data["created_utc"],
    unit="s"
).dt.date
del data["created_utc"]

data["created_date"] = pd.to_datetime(data["created_date"])

cutoff = pd.to_datetime("2011-01-16")

data["postac"] = np.where(
    data["subreddit"].str.lower().eq("hannahmontana"),
    "HannahMontana",
    np.where(
        data["created_date"] < cutoff,
        "HannahMontana",
        "MileyCyrus"
    )
)


print(data.shape)
print(data.head())

# zapis
data.to_csv(r"C:\Users\Admin\Desktop\TSMASS\Spolecznosc-muzyczna-Reddit\jsonl files\polaczone_dane.csv", index=False)