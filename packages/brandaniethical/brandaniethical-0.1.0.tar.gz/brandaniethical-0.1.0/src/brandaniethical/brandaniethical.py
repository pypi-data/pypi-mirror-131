import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.exceptions import HTTPError
import requests.auth
import os
# function 1: get fashion brands' animal ethical info 
def brandaniethical(brandlist):
    
    """
    Get fashion brands' animal ethical usage information. provide information of whether the brand use fur, angora, down feather, shearling, karakul, exotic animal skin and hair, wool use including ‘mulesing’, and leather 
    Also check whether brands use these material align with standards.
    
    Parameters
    ----------
    brandlist : list
      A list of brands name that consumers want to know their condition of animal usage
    
    Returns
    -------
    pandas.dataframe
      The dataframe of brands ethical consumption of animal material which include usage of fur, angora, down feather, shearling, karakul, exotic animal skin and hair, wool use including ‘mulesing’, and leather. Also check whether brands use these material align with standards.
      
    Examples
    --------
    >>> from brandaniethical import brandaniethical 
    >>> brandaniethical.brandaniethical(['cos','theory','lululemon','nike', 'skechers'])
	company	animal_score	update	fur	angora	leather	wool	shearling	karakul	down	feather	exotic animal hair	exotic animal skin	down_RDS	wool_mulesing
0	cos	3/5	July 2020	0	0	1	1	0	0	1	0	1	0	1	1
1	theory	2/5	December 2019	0	0	1	1	0	0	1	0	1	0	0	0
2	lululemon	2/5	July 2020	0	0	1	1	0	0	1	0	1	0	1	0
3	nike	2/5	July 2020	0	0	1	1	0	0	1	0	1	0	0	0
4	skechers	2/5	August 2020	0	0	1	1	0	0	0	0	0	0	0	0
    """
    assert isinstance(brandlist, list), f"This function only works on list but brandlist={brandlist}."
    for b in brandlist:
        assert isinstance(b, str), f"This function only works on string but brand={b}."
    brandlist = [b.lower() for b in brandlist]
    ani_reg = r'[^.]* animal [^.]*\.'
    use_reg = r'[^.]* (uses) [^.]*\.'
    date_reg = r'(Last Updated: )(\w*\s\d...)'
    web = 'https://directory.goodonyou.eco/'
    animal_score = []
    ani_rate= []
    company = []
    update = []
    def brandani(brandlist):
        df_gfy=pd.DataFrame()
        for brand in brandlist:
            goypage = requests.get(web +'brand/'+ brand)
            soup = BeautifulSoup(goypage.content, 'html.parser')
            try:
                animal_score.append(str(soup.find_all("span", {"class": "StyledText-sc-1sadyjn-0 ccIhDL"})[2].string))
                ani_rate.append([string for string in soup.stripped_strings if re.search(ani_reg, string)][0])
                update.append([string for string in soup.stripped_strings if re.search(date_reg, string)][0]) 
            except (IndexError, TypeError, NameError, KeyError):
                print(f'please check company name of {brand}')
                pass
            else:
                df_gfy['company'] = pd.Series(brandlist)
                df_gfy['animal_score'] = pd.Series(animal_score)
                df_gfy['ani_rate'] = pd.Series(ani_rate)
                df_gfy['update'] = pd.Series(update)
                pd.set_option('display.max_colwidth', None)
        return df_gfy
    global dfydf
    dfydf = brandani(brandlist)
    #check animal material usage
    #data wrangling
    try:
        
        dfydf['ani_material'] = [re.search(use_reg, i).group(0) for i in dfydf['ani_rate']]

    except (IndexError, TypeError, NameError, KeyError):
        print(f'no animal material information')
        

    else:
        dfydf['update'] = [re.search(r'\w*\s\d...', i).group(0) for i in dfydf['update']]
        dfydf['animal_score'] = [re.sub(r' out of ', '/', i) for i in dfydf['animal_score']]
        fabric = ['fur','angora', 'leather', 'wool', 'shearling', 'karakul', 'down', 'feather', 'exotic animal hair', 'exotic animal skin']
        for f in fabric:
            dfydf[f]=dfydf['ani_material'].str.contains(f)
        #check if use down whether down accredited by the Responsible Down Standar
        RDS_reg = 'It uses down accredited by the Responsible Down Standar'
        dfydf['down_RDS'] = dfydf['ani_rate'].str.contains(RDS_reg)
        dfydf.loc[dfydf['down_RDS']==True,'down'] = True
        #check if use wool whether wool includes mulesing
        dfydf['wool_mulesing'] = dfydf['ani_rate'].str.contains('mules')
        dfydf.loc[dfydf['wool_mulesing']==True,'wool'] = True
        df_aniusage = dfydf.loc[:,dfydf.columns!='ani_material']
        df_material = df_aniusage.replace(True,1)
        df_material = df_material.replace(False,0)
        
        return df_material.loc[:,df_material.columns!='ani_rate']
       
       
    
# function 2: get region trendytickers esg score       
import requests
from requests.exceptions import HTTPError
import requests.auth
import re
import pandas as pd
import os
regionlist = ['US', 'BR', 'AU', 'CA', 'FR', 'DE', 'HK', 'IN', 'IT', 'ES', 'GB', 'SG']
YAHOOF_KEY = os.getenv('YAHOOF_KEY')
app_key = os.getenv('ESG_KEY')

def trendyesg(region, start=5):
    """
    Get region's trendy tickers' esg score based on given region and regular rank of market price.

    Parameters
    ----------
    region : string
      A string that limit the region of market consumers are interested in, which include US, BR, AU, CA, FR, DE, HK, IN, IT, ES, GB, and SG.
    start : int
      A int that indicate the ranking place to start from.

    Returns
    -------
    pandas.dataframe
      The dataframe of trendy tickers' esg, environmental, social,governance score, and its ticker based on consumers interested region and the lowest ranking consumers want to start to look at

    Examples
    --------
    >>> from brandaniethical import trendyesg 
    >>> trendyesg(region='US',start =8)
	company_name	env_score	soc_score	gov_score	total	ticker
0	Medtronic plc	500	304	310	1114	MDT
1	Pfizer Inc.	510	300	305	1115	PFE
2	Roblox Corporation	245	304	220	769	RBLX
3	Lemonade, Inc.	520	303	300	1123	LMND
4	Nucor Corporation	251	326	210	787	NUE
    """
    assert region in regionlist, f"This function only works on {regionlist} but region={region}."
    assert isinstance(start, int), f"This function only works on int but start={start}."
    def get_trendycom(region, start=5):
        url = "https://yh-finance.p.rapidapi.com/market/get-trending-tickers"
        def trendytick(region):
            querystring = {"region":region}
            try:
                headers = {
                    'x-rapidapi-host': "yh-finance.p.rapidapi.com",
                    'x-rapidapi-key': YAHOOF_KEY
                            }
                response = requests.request("GET", url, headers=headers, params=querystring)
                response.raise_for_status()

            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err: 
                print(f'Other error occurred: {err}')
            return response.json()

        cominfolist = trendytick(region)

        region = []
        shortName = []
        regularMarketPrice = []
        symbol=[]
        trendtick_df = pd.DataFrame()
    
        for i in cominfolist['finance']['result'][0]['quotes']:   
            shortName.append(i['shortName'])
            regularMarketPrice.append(i['regularMarketPrice'])
            symbol.append(i['symbol'])

        trendtick_df['shortName'] = pd.Series(shortName)
        trendtick_df['regularMarketPrice'] = pd.Series(regularMarketPrice)
        trendtick_df['symbol'] = pd.Series(symbol)
        trendtick_df['maxprice_rank'] = trendtick_df['regularMarketPrice'].rank(method='max')

        return trendtick_df.sort_values(by=['maxprice_rank']).iloc[start:start+5]
    
    #get trendy tickers outcome
    tdf = get_trendycom(region=region, start=5)
    assert tdf.empty == False, f'there is no search results of {region} market'
    def ticktrans(tdf):
        #make fuzzy search of ticker e.g.
        ttlist = [i for i in tdf['symbol']]
        if region == 'US':
            reg_tick = '(^.+?)-|(^.*)'
            for tick in ttlist:
                try:
                    ticklist = [re.match(reg_tick,tick).group(1) for tick in ttlist]
                    ticklist.extend([re.match(reg_tick,tick).group(2) for tick in ttlist])
                    ticklist = list(filter(None, ticklist))
                    return ticklist
                except TypeError as e:
                    print(f'{e}: the ticker is not supported')
        else:
            return ttlist
    ticktransl = ticktrans(tdf)
    
    base_url = 'https://tf689y3hbj.execute-api.us-east-1.amazonaws.com/prod/authorization/'
    df = pd.DataFrame()
    company_name=[]
    env_score=[]
    soc_score=[]
    gov_score=[]
    total=[]
    region=[]
    ticker=[]
    for brand_tick in ticktransl:
        try:
            response_esg = requests.get(base_url+'search?',params={'q':brand_tick,'token':app_key})
            response_esg.raise_for_status()
            company_name.append(response_esg.json()[0]['company_name'])
            env_score.append(response_esg.json()[0]['environment_score'])
            soc_score.append(response_esg.json()[0]['social_score'])
            gov_score.append(response_esg.json()[0]['governance_score'])
            total.append(response_esg.json()[0]['total'])
            ticker.append(brand_tick)
        except (IndexError, TypeError) as error:
            company_name.append(brand_tick)
            env_score.append('NA')
            soc_score.append('NA')
            gov_score.append('NA')
            total.append('NA')
            ticker.append(brand_tick)
            print(f"{brand_tick}'s esg not in database")
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err: 
            print(f'Other error occurred: {err}')
    df['company_name'] = pd.Series(company_name)
    df['env_score'] = pd.Series(env_score)
    df['soc_score'] = pd.Series(soc_score)
    df['gov_score'] = pd.Series(gov_score)
    df['total'] = pd.Series(total)
    df['ticker'] = pd.Series(ticker)
    return df

