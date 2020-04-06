import pandas as pd

def main():
	# Create empty dataframe
	df = pd.DataFrame()
	# Iterate list of companies
	companies = ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla"]
	for company in companies:
		# Read CSV file
		company_df = pd.read_csv(f"./processed_data/{company}_clf.csv")
		# Drop index and BERT sentiment score columns
		company_df.drop(columns=['Unnamed: 0', '1_day_bert_sentiment_score', '1_day_overall_bert_sentiment_score'], inplace=True, errors='ignore')
		# Append dataframe to aggregated dataframe
		df = df.append(company_df, ignore_index=True)
	# One hot encoding
	df = pd.concat([df, pd.get_dummies(df['company'], prefix='company')], axis=1)
	# Remove existing 'company' column
	df.drop(columns=['company'], inplace=True)
	# Write dataframe to CSV file
	df.to_csv(r'./processed_data/aggregated_clf.csv', index=False)

if __name__ == '__main__':
	main()

	