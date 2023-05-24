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

    # Concatenate the Excel files
    file_names = ["demo_atc_l1.xlsx", "demo_atc_l2.xlsx", "demo_atc_l3.xlsx", "demo_atc_l4.xlsx", "demo_atc_l5.xlsx"]
    data_frames = []

    for file_name in file_names:
        df = pd.read_excel(file_name)
        data_frames.append(df)

    concatenated_df = pd.concat(data_frames)
    concatenated_df.to_excel('concatenated_atc_data.xlsx', index=False)
    print("Concatenated data saved to concatenated_atc_data.xlsx")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
