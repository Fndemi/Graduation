import pandas as pd

data = {
    "Name": ["  Felicia", "Huda", "Ashley", "Chris"],
    "Age": [22, 27, 19,32 ],
    "City": ["Mombasa", "Narok", "Kisumu", "Malindi"]
}

df = pd.DataFrame(data)
print(df)