# %%
import json
import pandas as pd
import requests

#understand that some changes happen
# Pulling in high-level market data - unique to symbol:
response_API = requests.get('https://aave-api-v2.aave.com/data/markets-data')
markets_data = response_API.text
JsonPull = pd.DataFrame(json.loads(markets_data))
JsonPull

#parsing through the json DataFrame to get one whole correctly formatted DataFrame:
data=pd.DataFrame({"underlyingAsset":[],
                   "symbol":[],
                   "isActive":[],
                   "isFreezed":[],
                   "borrowingEnabled":[],
                   "stableBorrowRateEnabled":[],
                   "variableBorrowRate":[],
                   "stableBorrowRate":[],
                   "liquidityRate":[],
                   "totalLiquidity":[],
                   "lastUpdateTimestamp":[],
                   "totalBorrows":[],
                   "id":[],
                   "totalLiquidityUSD":[],
                   "totalBorrowsUSD":[],
                   "interestPerSecond":[]})

for i in range(len(JsonPull)):
    data=data.append(JsonPull.loc[i][0],ignore_index=True)


#gather all the time stamped data for the symbol's in the 'data' DataFrame:
#check for active/ freeze status, as well as, when the API request returns nothing:

#create empty dataframe to put all your API data in:
historicalRates = pd.DataFrame()

#Loop for each record in 'data'
for i in range(len(data)):
    if data['isActive'][i] == 1 and data['isFreezed'][i] != 1:
        exec("requestpull_1hr = requests.get('https://aave-api-v2.aave.com/data/rates-history?reserveId="+str(data['id'][i])+"&from=1623590748&resolutionInHours=1')")
        request_data = requestpull_1hr.text
        indiv_Rates = pd.DataFrame(json.loads(request_data))     
        if indiv_Rates.empty == True:
            print(data['symbol'][i]," = Set as Active, but Pulled No Data")
        else:
            indiv_Rates = pd.concat([indiv_Rates, indiv_Rates['x'].apply(pd.Series)], axis=1)
            indiv_Rates = indiv_Rates.drop(columns='x')
            indiv_Rates['symbol'] = data['symbol'][i]
            historicalRates = historicalRates.append(indiv_Rates, ignore_index=True)
            print(data['symbol'][i]," = Successful")
    elif data['isActive'][i] == 0 and data['isFreezed'][i] != 0:
        print(data['symbol'][i]," = Not Active")
    else:
        print(data['symbol'][i]," = Freezed")

# %%
