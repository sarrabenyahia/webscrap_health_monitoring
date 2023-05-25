import asyncio
import pandas as pd

from whocc import WHOCCAtcDddIndex


async def main(loop):
    atc_ddd = WHOCCAtcDddIndex(loop=loop)
    await atc_ddd.get_l5()

    pd.DataFrame(atc_ddd.l1, columns=["ATC code", "href", "name"]).to_excel('demo_atc_l1.xlsx', index=False)
    pd.DataFrame(atc_ddd.l2, columns=["ATC code", "href", "name"]).to_excel('demo_atc_l2.xlsx', index=False)
    pd.DataFrame(atc_ddd.l3, columns=["ATC code", "href", "name"]).to_excel('demo_atc_l3.xlsx', index=False)
    pd.DataFrame(atc_ddd.l4, columns=["ATC code", "href", "name"]).to_excel('demo_atc_l4.xlsx', index=False)
    pd.DataFrame(atc_ddd.l5).to_excel('demo_atc_l5.xlsx', index=False)

    # Add suffix to level dataframes
    data_l1 = pd.DataFrame(atc_ddd.l1, columns=["ATC code", "href", "name"]).add_suffix('_L1')
    data_l2 = pd.DataFrame(atc_ddd.l2, columns=["ATC code", "href", "name"]).add_suffix('_L2')
    data_l3 = pd.DataFrame(atc_ddd.l3, columns=["ATC code", "href", "name"]).add_suffix('_L3')
    data_l4 = pd.DataFrame(atc_ddd.l4, columns=["ATC code", "href", "name"]).add_suffix('_L4')
    data_l5 = pd.DataFrame(atc_ddd.l5).add_suffix('_L5')

    # Create a temporary column with the first character of the ATC code for each level
    data_l2['ATC code_temp2'] = data_l2['ATC code_L2'].str[:1]
    data_l3['ATC code_temp3'] = data_l3['ATC code_L3'].str[:3]
    data_l4['ATC code_temp4'] = data_l4['ATC code_L4'].str[:4]
    data_l5['ATC code_temp5'] = data_l5['ATC code_L5'].str[:5]

    # Merge level 1 and level 2 dataframes
    concatenated_data = pd.merge(data_l1, data_l2, left_on='ATC code_L1', right_on='ATC code_temp2', how='outer')

    # Merge level 1-2 and level 3 dataframe
    concatenated_data = pd.merge(concatenated_data, data_l3, left_on='ATC code_L2', right_on='ATC code_temp3', how='outer')

    # Merge level 1-2-3 and level 4 dataframe
    concatenated_data = pd.merge(concatenated_data, data_l4, left_on='ATC code_L3', right_on='ATC code_temp4', how='outer')

    # Merge level 1-2-3-4 and level 5 dataframe
    concatenated_data = pd.merge(concatenated_data, data_l5, left_on='ATC code_L4', right_on='ATC code_temp5', how='outer')

    # Drop temporary columns
    columns_to_drop = [col for col in concatenated_data.columns if col.startswith('ATC code_temp')]
    concatenated_data = concatenated_data.drop(columns=columns_to_drop)
    
    #Filling the NAs of L5 level 
    # Sort the DataFrame by 'ATC code_L5'
    concatenated_data.sort_values(by='ATC code_L5', inplace=True)

    # Forward fill the NaN values within each group of the same 'ATC code_L5'
    concatenated_data['Name_L5'] = concatenated_data.groupby('ATC code_L5')['Name_L5'].ffill()
    
    concatenated_data.sort_values(by='ATC code_L1', inplace=True)

    # Save the concatenated dataframe to an Excel file
    concatenated_data.to_excel('ATC_DDD_Index.xlsx', index=False)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
