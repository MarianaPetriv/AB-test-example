import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load data from the CSV file
df = pd.read_csv('ab_test_data.csv')

# Group the data by test groups and output descriptive statistics
df.groupby('test_group').describe()

# Count the number of conversions in groups A and B
conversions_a = df[(df['test_group'] == 'a') & (df['conversion'] == 1)].shape[0]
conversions_b = df[(df['test_group'] == 'b') & (df['conversion'] == 1)].shape[0]

# Print the number of conversions for each group
print("Number of conversions in group A:", conversions_a)
print("Number of conversions in group B:", conversions_b)

# Convert the 'timestamp' column to datetime and calculate the duration of the test
start_date = pd.to_datetime(df['timestamp']).min()
end_date = pd.to_datetime(df['timestamp']).max()
duration = (end_date - start_date).days

# Print the start date, end date, and duration of the test
print("Test start date:", start_date)
print("Test end date:", end_date)
print("Test duration in days:", duration)

# Conduct a t-test to check the statistical significance of the difference between groups A and B
alpha = 0.05  # Significance level
statistic, pvalue = stats.ttest_ind(df[df['test_group'] == 'a']['conversion'],
                                    df[df['test_group'] == 'b']['conversion'], 
                                    alternative='less')

# Print the t-test results
print(f't-statistic: {round(statistic, 2)}, p-value: {round(pvalue, 2)}')
if pvalue < alpha:
    print('The difference is statistically significant, null hypothesis rejected (t-test).')
else:
    print('The difference is not significant, cannot reject the null hypothesis (t-test).')

# Visualize the mean conversion rates for groups A and B using a bar plot
plt.figure(figsize=(8, 6))
sns.barplot(x='test_group', y='conversion', hue='test_group', data=df, errorbar=('ci', 95), palette='Set2', legend=False)

plt.title('A/B Test Results')
plt.xlabel('Group')
plt.ylabel('Mean')
plt.show()

# Convert the 'timestamp' column to datetime format for working with time series
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Group the data by date and test group, calculate daily conversions
daily_data = df.groupby([df['timestamp'], 'test_group'])['conversion'].agg(['sum', 'count']).reset_index()

# Add a column for conversion rate
daily_data['conversion_rate'] = daily_data['sum'] / daily_data['count']
daily_data['date'] = pd.to_datetime(daily_data['timestamp']).dt.date

# Split the data into groups A and B for easier plotting
daily_data_A = daily_data[daily_data['test_group'] == 'a']
daily_data_B = daily_data[daily_data['test_group'] == 'b']

# Plot the daily conversion rate over time for both groups A and B
plt.figure(figsize=(10, 7))

sns.lineplot(x='date', y='conversion_rate', data=daily_data_A, label='A', color='green', marker='o')
sns.lineplot(x='date', y='conversion_rate', data=daily_data_B, label='B', color='orange', marker='o')

plt.xlabel('Date')
plt.ylabel('Daily Conversion Rate')
plt.title('Daily Conversion Rate Over Time')
plt.legend(title='Group')
plt.show()