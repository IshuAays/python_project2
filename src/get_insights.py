"""
reading 2 csv files merging them on ItemId,
filtering on dates and then calculating AvgCost,
writing the data into new csv file
"""
import pandas as pd

def get_insights(first_file , second_file):
    Items_df = pd.read_csv(first_file)
    Sales_df = pd.read_csv(second_file)


    merged_df = pd.merge(Items_df , Sales_df , on="ItemId")


    merged_df['StartDate'] = pd.to_datetime(merged_df["StartDate"])
    merged_df['EndDate'] = pd.to_datetime(merged_df['EndDate'])
    merged_df['SalesDate'] = pd.to_datetime(merged_df['SalesDate'])


    print(merged_df)

    filter_df = merged_df[
        (merged_df['SalesDate'] >= merged_df['StartDate'])
        &
        (merged_df['SalesDate'] <= merged_df['EndDate'])
        ]

    filter_df['TotalCost'] = filter_df['NumSales'] * filter_df['Price']
    print(filter_df)

    result_df = filter_df.groupby('ItemId').agg(
        TotalSales=('NumSales', 'sum'),
        TotalRevenue=('TotalCost', 'sum')
    ).reset_index()

    print(result_df)

    result_df['AvgCost'] = result_df['TotalRevenue'] / result_df['TotalSales']

    print(result_df)

    result_df.to_csv('result.csv' , index = False)
    print("Result saved to result.csv")



if __name__ == "__main__":
    file1 = input("Enter first file path here: ").strip('"')
    file2 = input("Enter second file path here: ").strip('"')

    get_insights(file1 , file2)