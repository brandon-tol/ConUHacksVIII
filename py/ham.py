import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from CSVParser import parse, Day, Server, Platform, MatchmakingOutcome

# Specify the exact name of the dependent variable column
dependent_variable = 'QUEUE_DURATION_IN_SEC'  # Update with the correct column name

# Replace this line with a call to your CSV parser function
# df_entries = pd.read_csv('sampleData1.csv')  # Replace with your actual CSV file
df_entries = parse('/sampleData1.csv')  # Adjust the filename as needed

# Convert the list of Entry objects to a DataFrame
df = pd.DataFrame([vars(entry) for entry in df_entries])

# Select relevant columns for analysis
selected_columns = ['party_size', 'mmr', 'role', 'day_of_week', dependent_variable]

# Perform label encoding for categorical variables
label_encoder = LabelEncoder()
df['day_of_week'] = label_encoder.fit_transform(df['day_of_week'])

# Get the original column names and add them to the one-hot encoded columns
original_column_names = selected_columns[:-1]
df_selected = df[selected_columns]

# One-hot encode categorical columns
preprocessor = ColumnTransformer(
    transformers=[
        ('encoder', OneHotEncoder(), ['day_of_week'])
    ],
    remainder='passthrough'
)
df_encoded = pd.DataFrame(preprocessor.fit_transform(df_selected))

# Set the correct number of columns for the DataFrame
df_encoded.columns = original_column_names + preprocessor.get_feature_names_out(['day_of_week'])

# Calculate the correlation matrix using Pearson correlation coefficient
correlation_matrix = df_encoded.corr()

# Identify the variables with the strongest correlations to the dependent variable
strong_correlations = correlation_matrix[dependent_variable].abs().sort_values(ascending=False)

# Extract the names of the variables that don't have weights
unweighted_variables = [var for var in strong_correlations.index if var != dependent_variable]

# Normalize weights for unweighted variables using Min-Max scaling
scaler = MinMaxScaler()
normalized_weights = scaler.fit_transform(correlation_matrix.loc[unweighted_variables, dependent_variable].values.reshape(-1, 1))

# Assign the normalized weights to the corresponding variables
weights = dict(zip(unweighted_variables, normalized_weights.flatten()))

print("Final Weights:")
print(weights)