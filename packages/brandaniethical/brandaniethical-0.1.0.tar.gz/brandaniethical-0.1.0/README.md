# brandaniethical

A package for green consumers and investors to quickly get a view of fashion brands’ animal policy, rate, and animal material usage. and check trendy tickers esg from yahoo finance and esg api

### Function1 - brandaniethical(brandlist)
The function provides a quick look at brandlists animal usage information, standards, and scores.
animal material ethical information include usage of fur, angora, down feather, shearling, karakul, exotic animal skin and hair, wool use including ‘mulesing’, and leather. Also check whether brands use these material align with standards.
In vignette file, a presentation demo with class of popular fashion brand is provided by retrieving 6 popoluar footwear and apparel brands' tickers yahoo finance.  
Skills:
Data Acquisition:
Import data from json.
Web scrape data from public websites: https://goodonyou.eco/
Write an API client for an API and/or functions associated with API interaction.
Handle, parse, and transform JSON and XML.
Data Cleaning, Transformation, and Organization:
Use data wrangling to transform data into a dataframe ready for green consumers reference and analysis.
Use loops processes.
Use functions and functional programming to export repetitive or difficult tasks.
Handle and process strings and use regular expressions.
Documentation and Presentation:
Provide and document useful functions as part of a Python package.
Capture error and exceptions
Use class
Use Jupyter Notebook to generate a vignette on how to use your package functions.

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
    
### Function2: trendyesg(region, start=5)
Get trendy tickers' company information from Yahoo Finance api and return their ESG score, environment score, social score, and governance score from ESG api. Users can check trending tickets across market regions, sort by top mktprice, start from specified rank of top marketing price tickers. uplimit = 20
region = ['US', 'BR', 'AU', 'CA', 'FR', 'DE', 'HK', 'IN', 'IT', 'ES', 'GB', 'SG']
Users can make fuzzy search of those trendy tickers by discarding dollar symbol such as usd, cad from trendy tickers search results. For example, shib-usd and shib-cad are both searched with 'shib' keyword, and the esg api only returns the stem ticker symbol.
Also, due to the rate limit of esg api, I set trendy tickers search results limited in 5 tickers. but users can start at any point of trendy tickers list sorted by market prices, the default is start from the 5th higest market price trendy tickers and return 5-10 trendy tickers esg scores.
In vignette file, a presentation demo with US region and ranking 8th - 12th higest market price trendy tickers ESG scores are provided in a dataframe. Another demo is US region ranking 10th - 14th higest market price trendy tickers ESG scores, as it can be seen some new tickers did not report their ESG therefore the result dataframe returns NA in according columns. 
Skills:
Data Acquisition:
Import data from json.
Use APIs to obtain data. - esg api + yahoo finance api
Yahoo finance API: https://rapidapi.com/apidojo/api/yh-finance/
ESG API document: https://www.esgenterprise.com/esg-enterprise-data-api-services/
Write an API client for an API and/or functions associated with API interaction.
Handle, parse, and transform JSON and XML.
Data Cleaning, Transformation, and Organization:
Use data wrangling to transform data into a dataframe ready for analysis.
Use loops processes.
Use functions and functional programming to export repetitive or difficult tasks.
Handle and process strings and use regular expressions.
Documentation and Presentation:
Provide and document useful functions as part of a Python package.
capture error
Use Jupyter Notebook to generate a vignette on how to use your package functions.

    
    """
    Get region's trendy tickers' esg score based on given region and regular rank of market price.

    Parameters
    ----------
    region : string
      A string that limit the region of market consumers are interested in, which include US, BR, AU, CA, FR, DE, HK, IN, IT, ES, GB, and SG.
    start : int
      A int that indicate the ranking .

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
    

## Installation

```bash
$ pip install brandaniethical
```

## Usage

- TODO

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`brandaniethical` was created by Yang Hu. It is licensed under the terms of the MIT license.

## Credits

`brandaniethical` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
