import sys
sys.path.append(".")
from corona_library import *



print('running')
#todo: pull directly from github once algorithm is finished
#todo: publish charts to renaissance_man wordpress



#import US data
start_date = np.datetime64(r'2020-04-12') #first day of us data
end_date = np.datetime64(today) - np.timedelta64(1,'D')
dates_list = make_date_array(start_date,end_date,strftime_format='%m-%d-%Y')

dfs_list = []
for mydate in dates_list:
    try:
        df = pd.read_csv(r'C:\__YOUTUBE__\__POLITICS__\Coronavirus\rawdata\COVID-19-master\csse_covid_19_data\csse_covid_19_daily_reports_us\\' + mydate + '.csv')
        #add date column
        df['Date'] = mydate
        dfs_list.append(df)
    except:
        #download new data from github
        df = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'  + mydate + '.csv')
        #save in folder
        df.to_csv(r'C:\__YOUTUBE__\__POLITICS__\Coronavirus\rawdata\COVID-19-master\csse_covid_19_data\csse_covid_19_daily_reports_us\\' + mydate + '.csv',index=False)
        df['Date'] = mydate
        dfs_list.append(df)

us_df = pd.concat(dfs_list, ignore_index=True)


#Rename non-descriptive columns
rename_dict = {'Active':'Active_Cases',
'Incident_Rate':'Incidence_Rate',
'FIPS':'US_County_FIPS',
'Lat':'Latitude',
'Long_':'Longitude'}
us_df = us_df.rename(columns=rename_dict)

#column order
us_df = us_df[['Date','Last_Update','Country_Region','Province_State','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','Incidence_Rate','US_County_FIPS','Latitude','Longitude','People_Tested','People_Hospitalized','UID','ISO3','Testing_Rate','Hospitalization_Rate']]

#to_newexcel(us_df)


#check testing rate vs cases for ny, tx, fl













#import world data
start_date = np.datetime64(r'2020-01-22') #first day of world data
end_date = np.datetime64(today) - np.timedelta64(1,'D')
dates_list = make_date_array(start_date,end_date,strftime_format='%m-%d-%Y')

dfs_list = []
for mydate in dates_list:
    try:
        df = pd.read_csv(r'C:\__YOUTUBE__\__POLITICS__\Coronavirus\rawdata\COVID-19-master\csse_covid_19_data\csse_covid_19_daily_reports\\' + mydate + '.csv')
        #fix mismatching column names here so columns arent duplacted later
        df = df.rename(columns={r'Country/Region':'Country_Region','Last Update':'Last_Update','Lat':'Latitude',r'Long_':'Longitude',r'Province/State':'Province_State'})
        #add date column
        df['Date'] = mydate
        dfs_list.append(df)
    except:
        #download new data from github
        df = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'  + mydate + '.csv')
        #save in folder
        df.to_csv(r'C:\__YOUTUBE__\__POLITICS__\Coronavirus\rawdata\COVID-19-master\csse_covid_19_data\csse_covid_19_daily_reports\\' + mydate + '.csv',index=False)
        #fix mismatching column names here so columns arent duplacted later
        df = df.rename(columns={r'Country/Region':'Country_Region','Last Update':'Last_Update','Lat':'Latitude',r'Long_':'Longitude',r'Province/State':'Province_State'})
        df['Date'] = mydate
        dfs_list.append(df)

world_df = pd.concat(dfs_list, ignore_index=True)


print('imported data')
#Rename non-descriptive columns
rename_dict = {'Active':'Active_Cases',
'Admin2':'US_City',
'Combined_Key':'US_Combined_Key',
'FIPS':'US_County_FIPS',
'Case-Fatality_Ratio':'Mortality_Rate'}
world_df = world_df.rename(columns=rename_dict)


#todo:backfill lattitude and longitude and other missing data

#order columns
world_df = world_df[['Date','Last_Update','Country_Region','Province_State','US_City','US_Combined_Key','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','Incidence_Rate','US_County_FIPS','Latitude','Longitude']]


#to_newexcel(world_df)

###check integrity of data between datasets for the us
##us_df = us_df[['Date','Country_Region','Province_State','Confirmed','Deaths']]
##us_df['Date'] = pd.to_datetime(us_df['Date'])
##us_df = us_df.rename(columns={'Confirmed':'Confirmed_us_df','Deaths':'Deaths_us_df'})
##
##world_df_us = world_df[world_df['Country_Region']=='US']
###there are errors in the Province_State column before 4-12-2020
##world_df_us['Date'] = pd.to_datetime(world_df_us['Date'])
##world_df_us = world_df_us[world_df_us['Date'] > np.datetime64('2020-04-11')]
##world_df_us = world_df_us[['Date','Country_Region','Province_State','US_Combined_Key','Confirmed','Deaths']]
##
##world_df_us = safe_reset_index(world_df_us.groupby(['Date','Country_Region','Province_State']).sum())
##
##
##
##df = us_df.merge(world_df_us,on=['Date','Country_Region','Province_State'],how='outer')
##
##df['Confirmed_Equal'] = df['Confirmed'] == df['Confirmed_us_df']
##df['Deaths_Equal'] = df['Deaths'] == df['Deaths_us_df']
##
##df = df.sort_values(['Date','Country_Region','Province_State'],ascending=True)
##
##
##to_newexcel(df)
##
#note: (8/9/2020)checked the data integrity between the two datasets and they are largely in aggreeance except for:
##Date	Country_Region	Province_State	Confirmed_us_df	Deaths_us_df	Confirmed	Deaths	Confirmed_Equal	Deaths_Equal
##2020-06-07	US	Virginia	50681.0	1472.0	50679.0	1472.0	False	True
##2020-06-09	US	Michigan	64998.0	5948.0	64998.0	5943.0	True	False
##2020-06-18	US	North Carolina	48167.0	1188.0	48168.0	1194.0	False	False
##2020-06-19	US	North Carolina	49785.0	1202.0	50018.0	1203.0	False	False
##2020-06-22	US	Idaho	4256.0	89.0	4254.0	89.0	False	True


#recalculate mortality rate
world_df['Confirmed'] = world_df['Confirmed'].fillna(0.0)
world_df['Deaths'] = world_df['Deaths'].fillna(0.0)
world_df['Mortality_Rate'] = world_df.apply(lambda mydf: mydf['Deaths'] / mydf['Confirmed'] if mydf['Confirmed'] != 0.0 else 0.0,axis=1)



###temp
##world_df = world_df[world_df['Country_Region']=='Australia']








#create just a single row for each Date,Country

#drop all non-needed cols
country_df = world_df[['Date','Country_Region','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered']].copy()
country_df = safe_reset_index(country_df.groupby(['Date','Country_Region']).sum())


#create US without NY and NJ Country (also no territories)
no_nynj_df = us_df[['Date','Country_Region','Province_State','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','People_Tested']].copy()
no_nynj_df = no_nynj_df[~no_nynj_df['Province_State'].isin(['New York','New Jersey','Guam','Puerto Rico','American Samoa','Northern Mariana Islands','Virgin Islands'])]
no_nynj_df = safe_reset_index(no_nynj_df.groupby(['Date','Country_Region']).sum())
no_nynj_df = no_nynj_df[['Date','Country_Region','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','People_Tested']].copy() #drop Province_State/ avoid pandas slice issue
no_nynj_df['Country_Region'] = 'US Without NY NJ'

country_df = pd.concat([country_df,no_nynj_df],ignore_index=True)


#create US Only NY and NJ Country (also no territories)
nynj_df = us_df[['Date','Country_Region','Province_State','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','People_Tested']].copy()
nynj_df = nynj_df[~nynj_df['Province_State'].isin(['Guam','Puerto Rico','American Samoa','Northern Mariana Islands','Virgin Islands'])]
nynj_df = nynj_df[nynj_df['Province_State'].isin(['New York','New Jersey'])]
nynj_df = safe_reset_index(nynj_df.groupby(['Date','Country_Region']).sum())
nynj_df = nynj_df[['Date','Country_Region','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','People_Tested']].copy() #drop Province_State/ avoid pandas slice issue
nynj_df['Country_Region'] = 'US Only NY NJ'

country_df = pd.concat([country_df,nynj_df],ignore_index=True)


#create US Only FL TX Country (also no territories)
fltx_df = us_df[['Date','Country_Region','Province_State','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','People_Tested']].copy()
fltx_df = fltx_df[~fltx_df['Province_State'].isin(['Guam','Puerto Rico','American Samoa','Northern Mariana Islands','Virgin Islands'])]
fltx_df = fltx_df[fltx_df['Province_State'].isin(['Florida','Texas'])]
fltx_df = safe_reset_index(fltx_df.groupby(['Date','Country_Region']).sum())
fltx_df = fltx_df[['Date','Country_Region','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','People_Tested']].copy() #drop Province_State/ avoid pandas slice issue
fltx_df['Country_Region'] = 'US Only FL TX'

country_df = pd.concat([country_df,fltx_df],ignore_index=True)


#create US Only FL Country (also no territories)
df = us_df[['Date','Country_Region','Province_State','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','People_Tested']].copy()
df = df[~df['Province_State'].isin(['Guam','Puerto Rico','American Samoa','Northern Mariana Islands','Virgin Islands'])]
df = df[df['Province_State'].isin(['Florida'])]
df = safe_reset_index(df.groupby(['Date','Country_Region']).sum())
df = df[['Date','Country_Region','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','People_Tested']].copy() #drop Province_State/ avoid pandas slice issue
df['Country_Region'] = 'US Only FL'

country_df = pd.concat([country_df,df],ignore_index=True)



#create US Only TX Country (also no territories)
df = us_df[['Date','Country_Region','Province_State','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','People_Tested']].copy()
df = df[~df['Province_State'].isin(['Guam','Puerto Rico','American Samoa','Northern Mariana Islands','Virgin Islands'])]
df = df[df['Province_State'].isin(['Texas'])]
df = safe_reset_index(df.groupby(['Date','Country_Region']).sum())
df = df[['Date','Country_Region','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','People_Tested']].copy() #drop Province_State/ avoid pandas slice issue
df['Country_Region'] = 'US Only TX'

country_df = pd.concat([country_df,df],ignore_index=True)


#create US Only NY Country (also no territories)
df = us_df[['Date','Country_Region','Province_State','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','People_Tested']].copy()
df = df[~df['Province_State'].isin(['Guam','Puerto Rico','American Samoa','Northern Mariana Islands','Virgin Islands'])]
df = df[df['Province_State'].isin(['New York'])]
df = safe_reset_index(df.groupby(['Date','Country_Region']).sum())
df = df[['Date','Country_Region','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','People_Tested']].copy() #drop Province_State/ avoid pandas slice issue
df['Country_Region'] = 'US Only NY'

country_df = pd.concat([country_df,df],ignore_index=True)



#create US Only NY Country (also no territories)
df = us_df[['Date','Country_Region','Province_State','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','People_Tested']].copy()
df = df[~df['Province_State'].isin(['Guam','Puerto Rico','American Samoa','Northern Mariana Islands','Virgin Islands'])]
df = df[df['Province_State'].isin(['New Jersey'])]
df = safe_reset_index(df.groupby(['Date','Country_Region']).sum())
df = df[['Date','Country_Region','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','People_Tested']].copy() #drop Province_State/ avoid pandas slice issue
df['Country_Region'] = 'US Only NJ'

country_df = pd.concat([country_df,df],ignore_index=True)






country_df = country_df[['Date','Country_Region','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','People_Tested']] #reorder cols



#dont recalculate mortality rate here
#recalculate Mortality_Rate after filling in missing data and calculating daily rates




##to_newexcel(country_df)
##country_df.to_clipboard(index=False)






###normalize by population
###
###some work to get a name decoder
##population_df = pd.read_csv(r"C:\__YOUTUBE__\__POLITICS__\Coronavirus\rawdata\population_worldbank.csv",low_memory=False)
##population_df = population_df[['Country Name','2019']]
####population_df = population_df.rename(columns={'Country Name':'Country_Region'})
##
##
####df = us_df.merge(world_df_us,on=['Date','Country_Region','Province_State'],how='outer')
##country_df['Dummy'] = 1
##df1 = safe_reset_index(country_df[['Country_Region','Dummy']].drop_duplicates())
##df = df1.merge(population_df, left_on =['Country_Region'], right_on =['Country Name'],how='outer')
##
##
##df = safe_reset_index(df.sort_values(['Country_Region'],ascending=True))
##
##df = df[['Dummy','Country_Region','Country Name','2019']]
##
##df2 = df[pd.isnull(df['Country_Region'])]
##
##df3 = df[pd.isnull(df['Country Name'])]
##
##
##df2[['Country Name']].to_clipboard(index=False)
##df3[['Country_Region']].to_clipboard(index=False)








#Normalize by population (and fix Country naming errors)

#data from World Bank (Missing countries filled in with data from Wikipedia)
population_df = pd.read_csv(r"C:\__YOUTUBE__\__POLITICS__\Coronavirus\rawdata\population_worldbank_johns_hopkins_decoder.csv",low_memory=False)


#convert population into millions
population_df['Population'] = population_df['Population'] * 1000.0

#fix non-standardized names in johns hopkins dataset
rename1_df = population_df[['JH_Alternative_1','Johns_Hopkins_Country_Region']].copy()
rename1_df = rename1_df.dropna(how='any')
rename1_dict = make_dict_from_cols(rename1_df,'JH_Alternative_1','Johns_Hopkins_Country_Region')
country_df['Country_Region'] = country_df['Country_Region'].map(lambda x: replace_if_in_dict(x, rename1_dict))


rename2_df = population_df[['JH_Alternative_2','Johns_Hopkins_Country_Region']].copy()
rename2_df = rename2_df.dropna(how='any')
rename2_dict = make_dict_from_cols(rename2_df,'JH_Alternative_2','Johns_Hopkins_Country_Region')
country_df['Country_Region'] = country_df['Country_Region'].map(lambda x: replace_if_in_dict(x, rename2_dict))






#dont join population data here
#join population data after filling in missing days (that way we can reuse the generate
#      daily values function for the US and other datasets







print('filling in weekend data')



#create daily case count (note: sometimes numbers are only reported on the weekend

#groupby function to limit country/state/county/whatever
#create days since last report column
#divide latest real number over missing days
#manually create full daterange to be joined

def generate_daily_values_extrapolate_weekends(mygroup_df,mycol,dailycol):

##    mygroup_df = country_df[country_df['Country_Region']=='Sweden'].copy()
    if mygroup_df['Country_Region'].iloc[0]=='Australia':
        d=1
    #create daterange starting with first date to overcome missing value issue
    start_date = np.datetime64(pd.to_datetime(mygroup_df['Date'].iloc[0])) #first day of data
    end_date = np.datetime64(today) - np.timedelta64(1,'D')
    dates_list = make_date_array(start_date,end_date,strftime_format='%m-%d-%Y')
    daterange_df = pd.DataFrame(pd.Series(dates_list),columns=['Date'])

    mygroup_df = daterange_df.merge(mygroup_df, on= ['Date'], how='left')
    mygroup_df['Country_Region'] = mygroup_df['Country_Region'].iloc[0] #fill in country for missing days
    mygroup_df = mygroup_df.sort_values(['Date'],ascending=True)
    mygroup_df = safe_reset_index(mygroup_df)
    #use ffill to fill any nans from unreported dates
    #use temp ffill col because we will backfill with the extrapolated values later
    mygroup_df[mycol + '_temp_ffilled'] = mygroup_df[mycol].ffill()
    mygroup_df[dailycol] = mygroup_df[mycol + '_temp_ffilled'] - mygroup_df[mycol + '_temp_ffilled'].shift()
    del mygroup_df[mycol + '_temp_ffilled']

    #there is an issue with the US Without NY NJ dataset for cases/deaths on first day of reporting
    #just set to zero
    if mygroup_df['Country_Region'].iloc[0] in ['US Without NY NJ','US Only NY NJ','US Only TX','US Only FL','US Only NY','US Only NJ','US Only FL TX']:
        mygroup_df[dailycol].iloc[0] = 0.0
    else:
        mygroup_df[dailycol].iloc[0] = mygroup_df[mycol].iloc[0]#fill first value



    #note: there may be the rare case where 4 or less new deaths will be reported over a weekend
    #and the extrapolation will say its 1,1,2 for sat, sun mon when its really
    #0,0,4 for sat sun mon, etc. but we will just live with that minor error
    for i in range(mygroup_df.shape[0]):
        #dont check last row
        if i == 0 or i == mygroup_df.shape[0]:
            pass
        #dont extrapolate if there are zero cases
        elif mygroup_df[mycol].iloc[i-1] == 0.0 and pd.isnull(mygroup_df[mycol].iloc[i]):
            #fill in potential nan from joining days
            mygroup_df[mycol].iloc[i] = 0.0
        else:
            #check up to 4 days of missed reporting for holiday, etc
            #assume 5 days is just no new cases
            #work backward
            if i + 4 < mygroup_df.shape[0] and mygroup_df[dailycol].iloc[i] == 0 and mygroup_df[dailycol].iloc[i+1] == 0 and mygroup_df[dailycol].iloc[i+2] == 0 and mygroup_df[dailycol].iloc[i+3] == 0 and mygroup_df[dailycol].iloc[i+4] !=0:
                rounded_down_value = np.floor(mygroup_df[dailycol].iloc[i+4] / 5) #round down
                mygroup_df[dailycol].iloc[i] = rounded_down_value
                mygroup_df[dailycol].iloc[i+1] = rounded_down_value
                mygroup_df[dailycol].iloc[i+2] = rounded_down_value
                mygroup_df[dailycol].iloc[i+3] = rounded_down_value
                mygroup_df[dailycol].iloc[i+4] = mygroup_df[dailycol].iloc[i+4] - (rounded_down_value * 4.0)

                #fill in original column
                mygroup_df[mycol].iloc[i] = mygroup_df[mycol].iloc[i-1] + mygroup_df[dailycol].iloc[i]
                mygroup_df[mycol].iloc[i+1] = mygroup_df[mycol].iloc[i] + mygroup_df[dailycol].iloc[i+1]
                mygroup_df[mycol].iloc[i+2] = mygroup_df[mycol].iloc[i+1] + mygroup_df[dailycol].iloc[i+2]
                mygroup_df[mycol].iloc[i+3] = mygroup_df[mycol].iloc[i+2] + mygroup_df[dailycol].iloc[i+3] #only need first 4, 5th already has value

            elif i + 3 < mygroup_df.shape[0] and mygroup_df[dailycol].iloc[i] == 0 and mygroup_df[dailycol].iloc[i+1] == 0 and mygroup_df[dailycol].iloc[i+2] == 0 and mygroup_df[dailycol].iloc[i+3] !=0:
                rounded_down_value = np.floor(mygroup_df[dailycol].iloc[i+3] / 4) #round down
                mygroup_df[dailycol].iloc[i] = rounded_down_value
                mygroup_df[dailycol].iloc[i+1] = rounded_down_value
                mygroup_df[dailycol].iloc[i+2] = rounded_down_value
                mygroup_df[dailycol].iloc[i+3] = mygroup_df[dailycol].iloc[i+3] - (rounded_down_value * 3.0)

                #fill in original column
                mygroup_df[mycol].iloc[i] = mygroup_df[mycol].iloc[i-1] + mygroup_df[dailycol].iloc[i]
                mygroup_df[mycol].iloc[i+1] = mygroup_df[mycol].iloc[i] + mygroup_df[dailycol].iloc[i+1]
                mygroup_df[mycol].iloc[i+2] = mygroup_df[mycol].iloc[i+1] + mygroup_df[dailycol].iloc[i+2] #only need first ones,last already has value

            elif i + 2 < mygroup_df.shape[0] and mygroup_df[dailycol].iloc[i] == 0 and mygroup_df[dailycol].iloc[i+1] == 0 and mygroup_df[dailycol].iloc[i+2] !=0:
                rounded_down_value = np.floor(mygroup_df[dailycol].iloc[i+2] / 3) #round down
                mygroup_df[dailycol].iloc[i] = rounded_down_value
                mygroup_df[dailycol].iloc[i+1] = rounded_down_value
                mygroup_df[dailycol].iloc[i+2] = mygroup_df[dailycol].iloc[i+2] - (rounded_down_value * 2.0)

                #fill in original column
                mygroup_df[mycol].iloc[i] = mygroup_df[mycol].iloc[i-1] + mygroup_df[dailycol].iloc[i]
                mygroup_df[mycol].iloc[i+1] = mygroup_df[mycol].iloc[i] + mygroup_df[dailycol].iloc[i+1] #only need first ones,last already has value

            elif i + 1 < mygroup_df.shape[0] and mygroup_df[dailycol].iloc[i] == 0 and mygroup_df[dailycol].iloc[i+1] !=0:
                rounded_down_value = np.floor(mygroup_df[dailycol].iloc[i+1] / 2) #round down
                mygroup_df[dailycol].iloc[i] = rounded_down_value
                mygroup_df[dailycol].iloc[i+1] = mygroup_df[dailycol].iloc[i+1] - rounded_down_value

                #fill in original column
                mygroup_df[mycol].iloc[i] = mygroup_df[mycol].iloc[i-1] + mygroup_df[dailycol].iloc[i] #only need one, second already has value


        #ffill at the end so it doesnt interfere with calculations
        mygroup_df[mycol] = mygroup_df[mycol].ffill()


    return mygroup_df




#for some reason, this will work sometimes and error out others
for test1 in range(10):
    try:
        country_df['Country_Region_Temp'] = country_df['Country_Region'].copy() #create temp col to avoid index/label error
        country_df.index.name = None
        country_df = safe_reset_index(country_df.groupby(['Country_Region_Temp'],as_index=False).apply(lambda df: generate_daily_values_extrapolate_weekends(df, mycol='Confirmed',dailycol='Confirmed_Daily')))
        print("created groupby1")
        country_df = safe_reset_index(country_df.groupby(['Country_Region_Temp'],as_index=False).apply(lambda df: generate_daily_values_extrapolate_weekends(df, mycol='Deaths',dailycol='Deaths_Daily')))
        print("created groupby2")
        country_df = safe_reset_index(country_df.groupby(['Country_Region_Temp'],as_index=False).apply(lambda df: generate_daily_values_extrapolate_weekends(df, mycol='People_Tested',dailycol='People_Tested_Daily')))
        del country_df['Country_Region_Temp']
        break
    except:
        print("trying again, attempt " + str(test1))
        del country_df['Country_Region_Temp']

print("created groupby successfully")

##cols_list_minus_date = (country_df.columns)
##country_df = country_df.dropna(subset=) #get rid of new rows created in extrapolating weekend daily data






#Mortility_Rate souldnt be summed, recalculate
country_df['Mortality_Rate'] = country_df.apply(lambda mydf: mydf['Deaths'] / mydf['Confirmed'] if mydf['Confirmed'] != 0.0 else 0.0,axis=1)


#join population data
population_df = population_df.rename(columns={'Johns_Hopkins_Country_Region':'Country_Region'})
population_df = population_df[['Country_Region','Population']]
country_df = country_df.merge(population_df, on = 'Country_Region',how='left')

print('joined population')



#create Incidence rates
country_df['Confirmed_Per_Million'] = country_df.apply(lambda mydf: 1000000.0 * mydf['Confirmed'] / mydf['Population'] if not (pd.isnull(mydf['Confirmed'] or pd.isnull(mydf['Population']))) else 0.0, axis=1)
country_df['Deaths_Per_Million'] = country_df.apply(lambda mydf: 1000000.0 * mydf['Deaths'] / mydf['Population'] if not (pd.isnull(mydf['Deaths'] or pd.isnull(mydf['Population']))) else 0.0, axis=1)

country_df['Confirmed_Daily_Per_Million'] = country_df.apply(lambda mydf: 1000000.0 * mydf['Confirmed_Daily'] / mydf['Population'] if not (pd.isnull(mydf['Confirmed_Daily'] or pd.isnull(mydf['Population']))) else 0.0, axis=1)
country_df['Deaths_Daily_Per_Million'] = country_df.apply(lambda mydf: 1000000.0 * mydf['Deaths_Daily'] / mydf['Population'] if not (pd.isnull(mydf['Deaths_Daily'] or pd.isnull(mydf['Population']))) else 0.0, axis=1)

country_df['People_Tested_Per_Million'] = country_df.apply(lambda mydf: 1000000.0 * mydf['People_Tested'] / mydf['Population'] if not (pd.isnull(mydf['People_Tested'] or pd.isnull(mydf['Population']))) else 0.0, axis=1)
country_df['People_Tested_Daily_Per_Million'] = country_df.apply(lambda mydf: 1000000.0 * mydf['People_Tested_Daily'] / mydf['Population'] if not (pd.isnull(mydf['People_Tested_Daily'] or pd.isnull(mydf['Population']))) else 0.0, axis=1)




country_df['Confirmed_Per_Population'] = country_df.apply(lambda mydf: mydf['Confirmed'] / mydf['Population'] if not (pd.isnull(mydf['Confirmed'] or pd.isnull(mydf['Population']))) else 0.0, axis=1)
country_df['Deaths_Per_Population'] = country_df.apply(lambda mydf: mydf['Deaths'] / mydf['Population'] if not (pd.isnull(mydf['Deaths'] or pd.isnull(mydf['Population']))) else 0.0, axis=1)

country_df['Confirmed_Daily_Per_Population'] = country_df.apply(lambda mydf: mydf['Confirmed_Daily'] / mydf['Population'] if not (pd.isnull(mydf['Confirmed_Daily'] or pd.isnull(mydf['Population']))) else 0.0, axis=1)
country_df['Deaths_Daily_Per_Population'] = country_df.apply(lambda mydf: mydf['Deaths_Daily'] / mydf['Population'] if not (pd.isnull(mydf['Deaths_Daily'] or pd.isnull(mydf['Population']))) else 0.0, axis=1)

country_df['People_Tested_Per_Population'] = country_df.apply(lambda mydf: mydf['People_Tested'] / mydf['Population'] if not (pd.isnull(mydf['People_Tested'] or pd.isnull(mydf['Population']))) else 0.0, axis=1)
country_df['People_Tested_Daily_Per_Population'] = country_df.apply(lambda mydf: mydf['People_Tested_Daily'] / mydf['Population'] if not (pd.isnull(mydf['People_Tested_Daily'] or pd.isnull(mydf['Population']))) else 0.0, axis=1)





#todo:estimate death rate by taking rolling average of both cases and deaths then offset by 7 days


#calculate rolling averages
country_df['People_Tested_Daily_7_Day_Rolling_Average'] = country_df.groupby('Country_Region').rolling(7)['People_Tested_Daily'].mean().reset_index(drop=True)
country_df['People_Tested_Daily_Per_Million_7_Day_Rolling_Average'] = country_df.groupby('Country_Region').rolling(7)['People_Tested_Daily_Per_Million'].mean().reset_index(drop=True)
country_df['People_Tested_Daily_Per_Population_7_Day_Rolling_Average'] = country_df.groupby('Country_Region').rolling(7)['People_Tested_Daily_Per_Population'].mean().reset_index(drop=True)





#join suicide rates
suicide_rates_df = pd.read_csv(r"C:\__YOUTUBE__\__POLITICS__\Coronavirus\rawdata\us_suicide_rates.csv",low_memory=False)

rename_dict = {'STATE':'Country_Region',
                'DEATHS':'Deaths_Suicide'}
suicide_rates_df = suicide_rates_df.rename(columns=rename_dict)
suicide_rates_df = suicide_rates_df[suicide_rates_df['Country_Region'].isin(['NJ','NY','FL','TX'])]
rename_dict = {'NJ':'US Only NJ',
                'NY':'US Only NY',
                'FL':'US Only FL',
                'TX':'US Only TX'}
suicide_rates_df['Country_Region'] = suicide_rates_df['Country_Region'].map(lambda x: replace_if_in_dict(x,rename_dict))
country_df = country_df.merge(suicide_rates_df[['Country_Region','Deaths_Suicide']],on='Country_Region',how='left')
country_df['Deaths_Suicide_Per_Million'] = country_df.apply(lambda mydf: 1000000.0 * float(mydf['Deaths_Suicide']) / mydf['Population'] if not (pd.isnull(mydf['Deaths_Suicide'] or pd.isnull(mydf['Population']))) else 0.0, axis=1)
country_df['Deaths_Suicide_Daily_Per_Million'] = country_df['Deaths_Suicide_Per_Million'].map(lambda x:  x/365.0 if not pd.isnull(x) else np.nan)


country_df = country_df[['Date','Country_Region','Population','Confirmed','Deaths','Mortality_Rate','Active_Cases','Recovered','Confirmed_Per_Million','Deaths_Per_Million','Deaths_Per_Population','Confirmed_Per_Population','Confirmed_Daily','Deaths_Daily','Confirmed_Daily_Per_Million','Confirmed_Daily_Per_Population','Deaths_Daily_Per_Million','Deaths_Daily_Per_Population','People_Tested','People_Tested_Daily','People_Tested_Daily_7_Day_Rolling_Average','People_Tested_Per_Million','People_Tested_Per_Population','People_Tested_Daily_Per_Million','People_Tested_Daily_Per_Population','People_Tested_Daily_Per_Million_7_Day_Rolling_Average','People_Tested_Daily_Per_Population_7_Day_Rolling_Average','Deaths_Suicide','Deaths_Suicide_Per_Million','Deaths_Suicide_Daily_Per_Million']]
country_df.to_csv(r'C:\__YOUTUBE__\__POLITICS__\Coronavirus\outputdata\coronavirus_world.csv',index=False)
to_newexcel(country_df)
































