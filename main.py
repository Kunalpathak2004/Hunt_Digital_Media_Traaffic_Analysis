import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data.csv')
df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

print(df.head())
print(df.info())
print(df.describe())
print(df.isna().sum())
print(df.drop_duplicates())
