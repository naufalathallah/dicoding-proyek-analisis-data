import pandas as pd

city_names = ['Jakarta', 'Bandung', 'Makassar', 'Surabaya', 'Medan', 'Yogyakarta', 'Malang']
population = [498044, 964254, 491918, 8398748, 653115, 883305, 744955]
num_airports = [2, 2, 8, 3, 1, 3, 2]

df = pd.DataFrame({
    'City Name': city_names,
    'Population': population,
    'Airports': num_airports,
})

print(df.describe(include="all"))
df.hist()
print(df[['Population', 'Airports']].corr())

body_measurement_df = pd.DataFrame.from_records((
    (2, 83.82, 8.4),
    (4, 99.31, 16.97),
    (3, 96.52, 14.41),
    (6, 114.3, 20.14),
    (4, 101.6, 16.91),
    (2, 86.36, 12.64),
    (3, 92.71, 14.23),
    (2, 85.09, 11.11),
    (2, 85.85, 14.18),
    (5, 106.68, 20.01),
    (4, 99.06, 13.17),
    (5, 109.22, 15.36),
    (4, 100.84, 14.78),
    (6, 115.06, 20.06),
    (2, 84.07, 10.02),
    (7, 121.67, 28.4),
    (3, 94.49, 14.05),
    (6, 116.59, 17.55),
    (7, 121.92, 22.96),
), columns=("age", "height_cm", "weight_kg"))

print(body_measurement_df.groupby(by="age").mean())

print(
body_measurement_df.groupby(by='age').agg({
    'height_cm': 'mean',
    'weight_kg': ['mean','max', 'min'],
})
)