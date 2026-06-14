import pandas as pd

df_a = pd.read_excel("sample_data/sample_data_A.xlsx")


df_b = pd.read_excel("sample_data/sample_data_B.xlsx")

print("DATA A:")
print(df_a.head())
print()
print(df_a.columns)

print()
print()

print("DATA B:")
print(df_b.head())
print()
print(df_b.columns)