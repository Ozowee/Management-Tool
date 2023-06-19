import json
import requests
import discord
from discord_webhook import DiscordWebhook
from currency_converter import CurrencyConverter
import pymongo
import io
import requests
from pprint import pprint
from csv import reader
from logs import log_info,log_error,log_success
from proxy import get_proxy
from random_user_agent.params import SoftwareName, HardwareType
from random_user_agent.user_agent import UserAgent


software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)

SizeChartTd = {'1c':'16','2c':'17','3c':'18.5','4c':'19.5','5c':'21','6c':'22','7c':'23.5','8c':'25','9c':'26','10c':'27'}
SizeChartPs = {'10.5C':'27.5','11C':'28','11.5C':'28.5','12C':'29.5','12.5C':'30','13C':'31','13.5C':'31.5','1Y':'32','1.5Y':'33','2Y':'33.5','2.5Y':'34','3Y':'35'}
SizeCharWmns = {'4.5W':'35','5W':'35.5','5.5W':'36','6W':'36.5','6.5W':'37.5','7W':'38','7.5W':'38.5','8W':'39','8.5W':'40','9W':'40.5','9.5W':'41','10W':'42','10.5W':'42.5','11W':'43','11.5W':'44','12W':'44.5','12.5W':'45','13W':'45.5','13.5W':'46','14W':'47','14.5W':'47.5','15W':'48','15.5W':'48.5','16W':'49','16.5W':'50','17W':'50.5','17.5W':'51',"18W":"52"}
SizeChartMens = {'3':'35','3.5':'35.5','4':'36','4.5':'36.5','5':'37.5','5.5':'38','6':'38.5','6.5':'39','7':'40','7.5':'40.5','8':'41','8.5':'42','9':'42.5','9.5':'43','10':'44','10.5':'44.5','11':'45','11.5':'45.5','12':'46','12.5':'47','13':'47.5','13.5':'48','14':'48.5','15':'49.5','16':'50.5','17':'51.5','18':'52.5'}
SizeChartYeezy = {'4':'36','4.5':'36 2/3','5':'37 2/3','5.5':'38','6':'38 2/3','6.5':'39 1/3','7':'40','7.5':'40 2/3','8':'41 1/3','8.5':'42','9':'42 2/3','9.5':'43 1/3','10':'44','10.5':'44 2/3','11':'45 1/3','11.5':'46','12':'46 2/3','12.5':'47 1/3','13':'48','13.5':'48 2/3','14':'49 1/3','14.5':'50','15':'50 2/3','16':'51 1/3','17':'52 2/3','18':'53 1/3' }
SizeChartGs = {'3.5Y':'35.5','4Y':'36','4.5Y':'36.5','5Y':'37.5','5.5Y':'38','6Y':'38.5','6.5Y':'39','7Y':'40'}
SizeChartUGG = {'5W':'36','6W':'37','7W':'38','8W':'39','9W':'40','10W':'41','11W':'42','12W':'44'}
SizeChartSlide = {'4':'37','5':'38','6':'39','7':'40.5','8':'42','9':'43','10':'44.5','11':'46','12':'47','13':'48.5','14':'49.5'}
SizeChartGazelle = {'5W':'36','5.5W':'36 2/3','6W':'37 1/3','7W':'38','7.5W':'38 2/3','8W':'39 1/3','8.5W':'40','9W':'40 2/3','9.5W':'41 1/3','10W':'42','10.5W':'42 2/3','11W':'43 1/3'}

with open("access.json",'r') as accessFile:
    jsonFile = json.load(accessFile)
    pyMongoAccess = jsonFile['Keys']['pyMongoClient']

def getDB():
    client = pymongo.MongoClient(pyMongoAccess)
    db = client.SneakersTool
    return db

def getDB_settings():
    client = pymongo.MongoClient(pyMongoAccess)
    db = client.Settings
    return db

def get_StockXInfo(query):
    #STOCKX#
    headersWeb = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Accept': '*/*',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
    'x-algolia-api-key': '8e4a7462fb74cdb921581efb97633b2e',
    'x-algolia-application-id': 'XW7SBCT9V6',
    'content-type': 'application/x-www-form-urlencoded',
    'Origin': 'https://pro.stockx.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    }
    data = {"query":query,"hitsPerPage":1,"page":0}
    req_stockx1 = requests.post('https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.13.0)%3B%20Browser', headers=headersWeb, json=data,proxies=get_proxy())
    
    if str(query.lower()) in str(req_stockx1.json()['hits']).lower():
        for query_results in req_stockx1.json()['hits']:
            if query_results['style_id'] == query.upper():
                photo = query_results['thumbnail_url']
                itemID = query_results['objectID']
                url = query_results['url']
                linkstockx=f"https://stockx.com/{query_results['url']}"
                retail_price = query_results['price']
                shoe_name = query_results['name']


                market_data_72 = query_results['sales_last_72']
                market_data_bid = query_results['highest_bid']
                market_data_last_sale = query_results['last_sale']

                info = {
                    "photo":photo,
                    "itemID":itemID,
                    "url":url,
                    "linkstockx":linkstockx,
                    "shoe_name":shoe_name,
                    "retail_price":int(retail_price),
                    "marketInfo":{
                            "72sales":int(market_data_72),
                            "highestBid":int(market_data_bid),
                            "lastSale":int(market_data_last_sale)
                        }
                    }
  
    return info

def Stockx_Prices(user,sku):
    User_DB = user
    Sizes_added = []
    x = [user_find['User'] for user_find in getDB_settings()['StockX'].find()]

    if User_DB in x:
        for element in x:
            if User_DB==element:
                query = {"User":User_DB}
                doc = getDB_settings()['StockX'].find_one(query)

                stockx_lvl = doc['Info']['Level']
                AccountType = doc['Info']['AccountType']
                oldSuccessful_Ship = doc['Info']['SuccessfulShipBonus']
                oldQuickShipBonus = doc['Info']['QuickShipBonus']

                if stockx_lvl == 1:
                    if str(oldQuickShipBonus)=="YES" and str(oldSuccessful_Ship)=="YES":
                        stockx_multiplication = 0.92
                    if str(oldQuickShipBonus)=="YES" and str(oldSuccessful_Ship)=="NO":
                        stockx_multiplication = 0.91
                    if str(oldQuickShipBonus)=="NO" and str(oldSuccessful_Ship)=="YES":
                        stockx_multiplication = 0.91
                    if str(oldQuickShipBonus)=="NO" and str(oldSuccessful_Ship)=="NO":
                        stockx_multiplication = 0.90
                if stockx_lvl == 2:
                    if str(oldQuickShipBonus)=="YES" and str(oldSuccessful_Ship)=="YES":
                        stockx_multiplication = 0.925
                    if str(oldQuickShipBonus)=="YES" and str(oldSuccessful_Ship)=="NO":
                        stockx_multiplication = 0.915
                    if str(oldQuickShipBonus)=="NO" and str(oldSuccessful_Ship)=="YES":
                        stockx_multiplication = 0.915
                    if str(oldQuickShipBonus)=="NO" and str(oldSuccessful_Ship)=="NO":
                        stockx_multiplication = 0.905
                if stockx_lvl == 3:
                    if str(oldQuickShipBonus)=="YES" and str(oldSuccessful_Ship)=="YES":
                        stockx_multiplication = 0.93
                    if str(oldQuickShipBonus)=="YES" and str(oldSuccessful_Ship)=="NO":
                        stockx_multiplication = 0.92
                    if str(oldQuickShipBonus)=="NO" and str(oldSuccessful_Ship)=="YES":
                        stockx_multiplication = 0.92
                    if str(oldQuickShipBonus)=="NO" and str(oldSuccessful_Ship)=="NO":
                        stockx_multiplication = 0.91
                if stockx_lvl == 4:
                    if str(oldQuickShipBonus)=="YES" and str(oldSuccessful_Ship)=="YES":
                        stockx_multiplication = 0.935
                    if str(oldQuickShipBonus)=="YES" and str(oldSuccessful_Ship)=="NO":
                        stockx_multiplication = 0.925
                    if str(oldQuickShipBonus)=="NO" and str(oldSuccessful_Ship)=="YES":
                        stockx_multiplication = 0.925
                    if str(oldQuickShipBonus)=="NO" and str(oldSuccessful_Ship)=="NO":
                        stockx_multiplication = 0.915
                    
                if stockx_lvl == 5:
                    if str(oldQuickShipBonus)=="YES" and str(oldSuccessful_Ship)=="YES":
                        stockx_multiplication = 0.94
                    if str(oldQuickShipBonus)=="YES" and str(oldSuccessful_Ship)=="NO":
                        stockx_multiplication = 0.93
                    if str(oldQuickShipBonus)=="NO" and str(oldSuccessful_Ship)=="YES":
                        stockx_multiplication = 0.93
                    if str(oldQuickShipBonus)=="NO" and str(oldSuccessful_Ship)=="NO":
                        stockx_multiplication = 0.92

                globaldict= dict()
                
                

                #stockx#
                headersWeb = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
                'Accept': '*/*',
                'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
                'x-algolia-api-key': '8e4a7462fb74cdb921581efb97633b2e',
                'x-algolia-application-id': 'XW7SBCT9V6',
                'content-type': 'application/x-www-form-urlencoded',
                'Origin': 'https://pro.stockx.com',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                }
                data = {"query":sku,"hitsPerPage":1,"page":0}
                req_stockx1 = requests.post('https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.13.0)%3B%20Browser', headers=headersWeb, json=data,proxies=get_proxy())
                log_success(req_stockx1.status_code)
                photo = req_stockx1.json()['hits'][0]['thumbnail_url']
                itemID = req_stockx1.json()['hits'][0]['objectID']
                url = req_stockx1.json()['hits'][0]['url']
                linkstockx=f"https://stockx.com/{req_stockx1.json()['hits'][0]['url']}"
                retail_price = req_stockx1.json()['hits'][0]['price']
                shoe_name = req_stockx1.json()['hits'][0]['name']
                try:
                    release_date = req_stockx1.json()['hits'][0]['searchable_traits']['Release Date']   
                except:
                    release_date = "N/A"


                headers=  {"user-agent": user_agent_rotator.get_random_user_agent(),
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"  }


                if AccountType == "PRIVATE":
                    req_stock2_prices = requests.get(f'https://stockx.com/api/products/{url}?includes=market&currency=EUR&country=PL',headers=headers,proxies=get_proxy())
                if AccountType == "B2B":
                    req_stock2_prices = requests.get(f'https://stockx.com/api/products/{url}?includes=market&currency=EUR&country=PL&market=PL.vat-registered',headers=headers,proxies=get_proxy())
                log_success(req_stock2_prices.status_code)
                for variant in req_stock2_prices.json()['Product']['children']:
                    variant2 = req_stock2_prices.json()['Product']['children'][variant]
                    
                    ask = variant2['market']['lowestAsk']
                    if AccountType == "PRIVATE":
                        ask_payout = int(ask)*0.95*stockx_multiplication - (int(ask)*0.03)

                    if AccountType == "B2B":
                        ask_payout = int(ask)*stockx_multiplication - (int(ask)*0.03)


                    if ask_payout !=0:
                        ask_payout_without_shipping = ask_payout - 5
                    else:
                        ask_payout_without_shipping = ask_payout

                    bid = variant2['market']['highestBid']
                    
                    bid_payout = int(bid)*stockx_multiplication
                    if bid_payout !=0:
                        bid_payout_without_shipping = bid_payout - 5
                    else:
                        bid_payout_without_shipping = bid_payout

                    shoe_size = variant2['market']['lowestAskSize']
                    


                    try:    
                        if "-ps" in linkstockx.split("/")[-1]:
                            size_swap = SizeChartPs[shoe_size]
                        elif "yeezy" in linkstockx.split("/")[-1]:
                            if "slide" in linkstockx.lower() or "rnnr" in linkstockx.lower():
                                size_swap = SizeChartSlide[shoe_size]
                            else:
                                size_swap = SizeChartYeezy[shoe_size]             
                        elif "-td" in linkstockx.split("/")[-1]:    
                            size_swap = SizeChartTd[shoe_size]
                        elif "-gs" in linkstockx.split("/")[-1]:    
                            size_swap = SizeChartGs[shoe_size]
                        elif "-w" == str(linkstockx.split("/")[-1][-2:]):
                            if "ugg" in linkstockx.lower(): 
                                size_swap = SizeChartUGG[shoe_size]
                            if "gazelle" in linkstockx.lower():
                                size_swap = SizeChartGazelle[shoe_size]
                            if "ugg" not in linkstockx.lower() and "gazelle" not in linkstockx.lower():
                                size_swap = SizeCharWmns[shoe_size]
                        else: 
                            if "samba" in linkstockx.lower():
                                size_swap = SizeChartYeezy[shoe_size] 
                            else: 
                                size_swap = SizeChartMens[shoe_size]
                    
                        globaldict[size_swap] = {"PayoutASK":round(ask_payout_without_shipping,2),"PayoutBID":round(bid_payout_without_shipping,2)}
                    
                    

                    except KeyError:
                        pass
                #ALIAS
                headers = {
                'Host': 'ac.cnstrc.com',
                'sec-ch-ua': '"Chromium";v="108", "Opera";v="94", "Not)A;Brand";v="99"',
                'dnt': '1',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
                'sec-ch-ua-platform': '"Windows"',
                'accept': '*/*',
                'origin': 'https://www.goat.com',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
                }

                params = {
                    'c': 'ciojs-client-2.29.12',
                    'key': 'key_XT7bjdbvjgECO5d8',
                    'i': '115b2811-4b21-4332-a13f-5b21e64fb52d',
                    's': '1',
                    'num_results_per_page': '25',
                    '_dt': '1672247378780',
                }

                response = requests.get(f'https://ac.cnstrc.com/search/{sku}', params=params, headers=headers)
                try:
                    slug =  response.json()['response']['results'][0]['data']['slug']
                

                    headers = {
                        'Host': 'sell-api.goat.com',
                        'Accept': 'application/json',
                        'Authorization': 'Bearer Ip8zYF3Hhz8yQY5Q8KwvmyrtT1WGzgizPTfKXu2sJIs.tEKF51ojOQr0t9gkWzajfBtkze_4E3YTIM285dSbCAk',
                        'Accept-Language': 'pl-PL,pl;q=0.9',
                        'User-Agent': 'alias/1.20.1 (iPhone; iOS 16.1.1; Scale/2.00) Locale/en',
                        'Content-Type': 'application/x-www-form-urlencoded',
                    }

                    data = '{"variant":{"id":"'+slug+'","packagingCondition":1,"consigned":false,"regionId":"2"}}'

                    response2 = requests.post(
                        'https://sell-api.goat.com/api/v1/analytics/list-variant-availabilities',
                        headers=headers,
                        data=data,
                        
                    )


                    for i in response2.json()['availability']:
                        if i['variant']['product_condition'] == "PRODUCT_CONDITION_NEW" and i['variant']['packaging_condition'] == "PACKAGING_CONDITION_GOOD_CONDITION":
                            try:
                                if "ps" in linkstockx.split("/")[-1]:
                                    sizeAlias = str(i['variant']['size'])+"C"
                                    size_swap_alias = SizeChartPs[sizeAlias]
                                    

                                elif "yeezy" in linkstockx.split("/")[-1]:
                                    sizeAlias = str(i['variant']['size'])
                                    if "slide" in linkstockx.lower() or "rnnr" in linkstockx.lower():
                                        size_swap_alias = SizeChartSlide[sizeAlias]
                                    else:
                                        size_swap_alias = SizeChartYeezy[sizeAlias]

                                elif "td" in linkstockx.split("/")[-1]:    
                                    sizeAlias = str(i['variant']['size']) + "c"
                                    size_swap_alias = SizeChartTd[sizeAlias]

                                elif "gs" in linkstockx.split("/")[-1]:    
                                    sizeAlias = str(i['variant']['size'])+"Y"
                                    size_swap_alias = SizeChartGs[sizeAlias]

                                elif "-w" == str(linkstockx.split("/")[-1][-2:]):
                                    sizeAlias = str(i['variant']['size'])+"W"
                                    if "ugg" in linkstockx.lower():  
                                        size_swap_alias = SizeChartUGG[sizeAlias]
                                    if "gazelle" in linkstockx.lower():
                                        size_swap_alias = SizeChartGazelle[sizeAlias]
                                    if "ugg" not in linkstockx.lower() and "gazelle" not in linkstockx.lower():
                                        size_swap_alias = SizeCharWmns[sizeAlias]
                                else: 
                                    sizeAlias = str(i['variant']['size'])
                                    
                                    if "samba" in linkstockx.lower():
                                        size_swap_alias = SizeChartYeezy[sizeAlias] 
                                    else: 
                                        size_swap_alias = SizeChartMens[sizeAlias]

                                price1usd = ((int(i['lowest_price_cents'][:-2]) * 0.905) - 12 )* 0.971
                                price2usd = ((int(i['high_demand_price_cents'][:-2]) * 0.905) - 12 )* 0.971
                            

                                cr = CurrencyConverter()
                                price1 = round(cr.convert(price1usd,"USD",'EUR'),2)
                                

                                try:
                                    globaldict[size_swap_alias]['PayoutAlias'] = price1
                                
                                except KeyError:
                                    globaldict[size_swap_alias]['PayoutAlias'] = "N/A"
                            except Exception:
                                pass  
                except IndexError:
                    pass  
                return globaldict

    else:
        log_info(f"{User_DB} not found in settingsDB!")

        dataError = "brak danych"
        return dataError

def get_NewMarketData(query):
    
    headersWeb = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Accept': '*/*',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
    'x-algolia-api-key': '8e4a7462fb74cdb921581efb97633b2e',
    'x-algolia-application-id': 'XW7SBCT9V6',
    'content-type': 'application/x-www-form-urlencoded',
    'Origin': 'https://pro.stockx.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    }
    data = {"query":query,"hitsPerPage":1,"page":0}
    req_stockx1 = requests.post('https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.13.0)%3B%20Browser', headers=headersWeb, json=data,proxies=get_proxy())
    
    if str(query.lower()) in str(req_stockx1.json()['hits']).lower():
        for query_results in req_stockx1.json()['hits']:
            if query_results['style_id'] == query.upper():

                market_data_72 = query_results['sales_last_72']
                market_data_bid = query_results['highest_bid']
                market_data_last_sale = query_results['last_sale']

                info = {
                        "Info.marketInfo.72sales":int(market_data_72),
                        "Info.marketInfo.highestBid":int(market_data_bid),
                        "Info.marketInfo.lastSale":int(market_data_last_sale)
                    }
    
    return info

def Add(sku,size,quantity,user):
    if "," in str(size):
        size = str(size).replace(',','.')
    if ".5" in str(size):
        size = str(size).replace(".5"," 1/2")
    
    User_DB = user

    x = [sku_find['SKU'] for sku_find in getDB()[User_DB].find()]
    sku = str(sku).upper()
    if str(sku) in str(x):
        for element in x:
            if str(sku) == element:
                Sizes = []
                if int(quantity) >=1:
                    DB_sizes = [sku['Size'] for sku in getDB()[User_DB].find() if sku['SKU']==element]
                    if size in str(DB_sizes):
                            
                            query = {'SKU':element}
                            doc = getDB()[User_DB].find_one(query)
                            
                            for d in doc['Size']:
                                
                                if str(d) == str(size):
                                    
                                    OldQuantity = doc['Size'][d]['Quantity']
                                    NewQuantity = int(OldQuantity)+int(quantity)
                                    doc['Size'][d]['Quantity'] = int(NewQuantity)

                                    getDB()[User_DB].update_one(query,{'$set':doc}) 
                                    log_success(f"[ADD] Successfully updated Quantity for {element} | {size}")

                                    embed = discord.Embed(title=f'Successfully added {quantity} to {sku} | {size}', color = 0x212129)

                                    return embed
                            else:
                                
                                update = {'$set':{f"Size.{size}":{'Quantity':int(quantity)}}}

                                getDB()[User_DB].update_one(query,update)
                                log_success(f"[ADD] Successfully added details for {element} | {size}")

                                embed = discord.Embed(title=f'Successfully added {quantity} to {sku} | {size}!', color = 0x212129)

                                return embed
                    else:
                        
                        query = {'SKU':element}
                        update = {'$set':{f"Size.{size}":{'Quantity':int(quantity)}}}

                        getDB()[User_DB].update_one(query,update)
                        log_success(f"[ADD] Successfully added details for {element} | {size}")

                        embed = discord.Embed(title=f'Successfully added {quantity} to {sku} | {size}!', color = 0x212129)

                        return embed
                    
                else:
                    log_info(f"[ADD] Wrong Quantity!")
                    embed = discord.Embed(title=f'Quantity has to be atleast 1!', color = 0x212129)

                    return embed
    try:
        if str(sku) not in str(x):
            data = {
                str("SKU"):sku,
                str("Size"):{
                    str(size):{
                        "Quantity":int(quantity)
                    }
                },
                str("Info"):get_StockXInfo(sku)
                
            }

            getDB()[User_DB].insert_one(data)
            log_success(f"[ADD] Successfully added {sku} to DB!")
            
            embed = discord.Embed(title=f'Successfully added {sku} details!', color = 0x212129)
            return embed
        
    except Exception as e:
        log_error(f"{sku} not exist")
        embed = discord.Embed(title=f'{sku} not exist! Try again', color = 0x212129)
        return embed
        
def Remove(sku,size,quantity,user):
    if ".5" in str(size):
        size = str(size).replace(".5"," 1/2")

    User_DB = user

    x = [sku_find['SKU'] for sku_find in getDB()[User_DB].find()]
    sku = str(sku).upper()
    if str(sku) in x:
        for element in x:
            if str(sku) == element:
                z = [sku['Size'] for sku in getDB()[User_DB].find() if sku['SKU']==element]
                if str(size) in str(z):
                    if int(quantity) >=1:
                    
                        query = {'SKU':element}
                        doc = getDB()[User_DB].find_one(query)
                        for d in doc['Size']:
                            if str(size)==str(d):
                                OldQuantity = doc['Size'][d]['Quantity']
                                
                        
                                NewQuantity = OldQuantity-quantity
                                if NewQuantity == 0:
                                    del doc['Size'][size]
                                    getDB()[User_DB].update_one(query,{'$set':doc})
                                    
                                    checkUpdated = getDB()[User_DB].find_one(query)

                                    log_success(f"[REMOVE] Successfully updated Quantity for {element} | {size}")

                                    if len(checkUpdated['Size'])==0:
                                        getDB()[User_DB].delete_one(query)

                                        log_success(f"[REMOVE] Successfully dropped {sku} records")
                                        embed = discord.Embed(title=f"{sku} removed from the DB! Last item was deleted!", color = 0x212129)
                                        return embed
                                    else:
                                        embed = discord.Embed(title=f'Removed {quantity} from {sku} | {size}', color = 0x212129)

                                        return embed

                                else:
                                    doc['Size'][size]['Quantity'] = int(NewQuantity) #{'$numberInt':NewQuantity}

                                    getDB()[User_DB].update_one(query,{'$set':doc}) 

                                    log_success(f"[REMOVE] Successfully updated Quantity for {element} | {size}")

                                    embed = discord.Embed(title=f'Removed {quantity} from {sku} | {size}', color = 0x212129)

                                    return embed
                    else:
                        embed = discord.Embed(title=f'Quantity has to be atleast 1!', color = 0x212129)

                        log_info("[REMOVE] Wrong Quantity, has to be atleast 1!")
                        return embed
                
                else:
                    embed = discord.Embed(title=f'This Size-SKU is not in the DB!', color = 0x212129)
                    log_info("[REMOVE] Wrong Size!")
                    return embed
    else:
        embed = discord.Embed(title=f'This SKU is not in the DB!', color = 0x212129)

        log_info("[REMOVE] Wrong SKU!")
        return embed
    
def Check(sku,user):
    User_DB = user

    marketData = []
    added_sizes = []
    sku_DB = [sku_find['SKU'] for sku_find in getDB()[User_DB].find()]
    sku = str(sku).upper()
    settings = [element['User'] for element in getDB_settings()['StockX'].find()]
    if str(User_DB) in settings:
        if str(sku) in str(sku_DB):
            Col = getDB()[User_DB]
            query = {'SKU':sku}
            
            
            getDB()[User_DB].update_one(query,{'$set':get_NewMarketData(sku)})
            log_info(f"[CHECK] Updated market data for {sku}")

            
            data = Col.find_one(query)

            for keys in data['Info']['marketInfo']:
                market = data['Info']['marketInfo'][keys]
                marketData.append(market)

            
            imageUrl = data['Info']['photo']
            productName = data['Info']['shoe_name']
            stockxurl = data['Info']['linkstockx']
            
            for d in data['Size']:
                quantity = data['Size'][d]['Quantity']
                
                if " 1/2" in str(d):
                    d = str(d).replace(" 1/2",".5")

                added_sizes.append(d)

            
            payouts = Stockx_Prices(User_DB,sku)

            if payouts != "brak danych":
            
                PayoutsForSizes = {}
                for key,value in payouts.items():
                    if key in added_sizes:
                        try:
                            PayoutsForSizes[key] = {"Payout Ask":value['PayoutASK'], "Payout Bid":value['PayoutBID'], "Payout Alias":value['PayoutAlias']}
                        except KeyError:
                            PayoutsForSizes[key] = {"Payout Ask":value['PayoutASK'], "Payout Bid":value['PayoutBID']}

                for d in data['Size']:
                    quantity = data['Size'][d]['Quantity']
                    
                    if " 1/2" in str(d):
                        d = str(d).replace(" 1/2",".5")


                    PayoutsForSizes[d]['Quantity'] = quantity

                try:
                    currency_r = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/eur/today/')
                    EurPln = currency_r.json()['rates'][0]['mid']
                    

                    CheckItemsReturn = []
                    for k,v in PayoutsForSizes.items():
                        try:
                            payoutASK = f"{v['Payout Ask']}€ ({round(float(v['Payout Ask'])*float(EurPln))} PLN)"
                            payoutBID = f"{v['Payout Bid']}€ ({round(float(v['Payout Bid'])*float(EurPln))} PLN)"
                            PayoutAlias = f"{v['Payout Alias']}€ ({round(float(v['Payout Alias'])*float(EurPln))} PLN)"
                            CheckItemsReturn.append(f"```{k} | {v['Quantity']} | {payoutASK} | {PayoutAlias}```")
                        except Exception:
                            payoutASK = f"{v['Payout Ask']}€ ({round(float(v['Payout Ask'])*float(EurPln))} PLN)"
                            CheckItemsReturn.append(f"```{k} | {v['Quantity']} | {payoutASK} | N/A```")

                except Exception:
                    cr = CurrencyConverter()
                    CheckItemsReturn = []
                    for k,v in PayoutsForSizes.items():
                        try:
                            payoutASK = f"{v['Payout Ask']}€"
                            payoutBID = f"{v['Payout Bid']}€"
                            PayoutAlias = f"{v['Payout Alias']}€"
                            payoutASKpln = round(cr.convert(v['Payout Ask'],"EUR",'PLN'),2)
                            payoutAliaspln = round(cr.convert(v['Payout Alias'],"EUR",'PLN'),2)
                            CheckItemsReturn.append(f"```{k} | {v['Quantity']} | {payoutASK} ({payoutASKpln}PLN) | {PayoutAlias} ({payoutAliaspln}PLN)```")
                        except Exception:
                            payoutASK = f"{v['Payout Ask']}€"
                            CheckItemsReturn.append(f"```{k} | {v['Quantity']} | {payoutASK} ({payoutASKpln}PLN) | N/A```")
                
                
                log_success(f"[CHECK] Successfully checked {sku}")
                embed = discord.Embed(title=f"{productName}", color = 0x212129)
                embed.set_thumbnail(url = imageUrl)
                embed.add_field(name='Size | Quantity | StockX payout | Alias payout',value=''.join(CheckItemsReturn),inline=False)
                embed.add_field(name="Market Data:",value=f"Last 72h sales: **{marketData[0]}**\nHighest bid: **{marketData[1]}€**\nLast Sale: **{marketData[2]}€**",inline=False)
                embed.add_field(name="SKU:",value=sku,inline=True)
                embed.add_field(name="StockX:",value=f"[[click]]({stockxurl})",inline=True)
                embed.set_footer(text="Created by Rafał#6750",icon_url="https://i.imgur.com/yeUP0WC.png")
                return embed
            
            else:
                embed = discord.Embed(title=f"Setup stockX settings first! ./setup_stockX", color = 0x212129)
                return embed
        
        else:
            log_info(f"{sku} not found in user DB!")
            embed = discord.Embed(title=f"{sku} not found in your DB!", color = 0x212129)
            return embed
    else:
        embed = discord.Embed(title=f"Setup stockX settings first! ./setup_stockX", color = 0x212129)
        return embed

def ReadCSV(user,file):
    User_DB = user
    csv_lines = []
    response = requests.get(file)
    csv_file = io.StringIO(response.text)
    csv_reader = reader(csv_file)
    for row in csv_reader:
        if 'SKU' not in row:
            csv_lines.append(row)
    count = 0
    Error_lines = ""
    for line in csv_lines:
        count += 1

        if ".5" in str(line[1]):
            line[1] = str(line[1]).replace(".5"," 1/2")
        
        sku_DB = [sku_find['SKU'] for sku_find in getDB()[User_DB].find()]
        if str(line[0]) in sku_DB:
            for element in sku_DB:
                if str(line[0])==element:
                    if int(line[2]) >=1:
                        query = {'SKU':element}
                        update = {'$set':{f"Size.{str(line[1])}":{'Quantity':int(line[2])}}}
                        
                        getDB()[User_DB].update_one(query,update)
                        log_success(f"[ADD_CSV] Successfully added details for {element} | {line[1]}")

                        
                    else:
                        log_info(f"[ADD_CSV] Wrong Quantity in line {count}!")
                        Error_lines += f"{count}, "

                    
        if str(line[0]) not in sku_DB:
            if int(line[2]) >=1:
                try:
                    data = {
                        str("SKU"):line[0],
                        str("Size"):{
                            str(line[1]):{
                                "Quantity":int(line[2])
                                }
                            },
                        str("Info"):get_StockXInfo(line[0])   
                        }

                    getDB()[User_DB].insert_one(data)
                    log_success(f"[ADD_CSV] Successfully added new product to DB from CSV file! {line[0]} | {line[1]}")

                except Exception as e:
                    log_error(f"[ADD_CSV] {line[0]} not exist")
                    Error_lines += f"{count}, "

                
            else:
                log_info(f"[ADD_CSV] Wrong Quantity in line {count}!")
                Error_lines += f"{count}, "

    embed = discord.Embed(title=f'Successfully added to {User_DB} DB! Wrong SKU in lines: {Error_lines}', color = 0x212129)
    return embed

def ClearQuery(sku,user):
    User_DB = user

    sku_DB = [sku_find['SKU'] for sku_find in getDB()[User_DB].find()]
    sku = str(sku).upper()
    
    if str(sku) in sku_DB:
        Col = getDB()[User_DB]
        query = {'SKU':str(sku)}

        data = Col.find_one(query)

        Col.delete_one(query)

        log_success(f"[DROP] Successfully dropped {sku} records")
        embed = discord.Embed(title=f"{sku} removed from the DB!", color = 0x212129)
        return embed
    else:
        log_info(f"[DROP] {sku} not found in the DB!")
        embed = discord.Embed(title=f"{sku} not found in the DB!", color = 0x212129)
        return embed

def CheckAll(user,page):
    items1 = []
    itemsTEMP = []
    TotalCount = 0

    for data in getDB()[user].find():
        SizeSUM = ""
        shoe_name = get_StockXInfo(data['SKU'])['shoe_name']
        
        for size in data['Size']:
            quantity = data['Size'][size]['Quantity']

            if " 1/2" in str(size):
                size = str(size).replace(" 1/2",".5")
            SizeSUM += f"{size}x{quantity} "
            TotalCount += quantity
        items1.append(f"```{shoe_name} | {data['SKU']} | {SizeSUM}\n```")

    splitted_to_twenty = list()
    chunk_size = 20

    for i in range(0,len(items1),chunk_size):
            splitted_to_twenty.append(items1[i:i+chunk_size])
    
    if len(splitted_to_twenty) > page and page >= 0:
        embed = discord.Embed(title=f"Unique Products: {len(splitted_to_twenty[page])} | Total Stock: {TotalCount}", color = 0x212129)
        log_success(f"[CHECK_ALL] Successfully scrapped {len(splitted_to_twenty[page])} products!")
        if len(splitted_to_twenty[page]) > 10:
            listdiff1 = splitted_to_twenty[page][:int(len(splitted_to_twenty[page])/2)]
            listdiff2 = splitted_to_twenty[page][int(len(splitted_to_twenty[page])/2):]

            embed.add_field(name='NAME | SKU | SIZES',value=f'{"".join(listdiff1)}',inline=True)
            embed.add_field(name='NAME | SKU | SIZES',value=f'{"".join(listdiff2)}',inline=True)
            embed.set_footer(text="Created by Rafał#6750",icon_url="https://i.imgur.com/yeUP0WC.png")
        else:
            embed.add_field(name='NAME | SKU | SIZES',value=f'{"".join(splitted_to_twenty[page])}',inline=False)
            embed.set_footer(text="Created by Rafał#6750",icon_url="https://i.imgur.com/yeUP0WC.png")
    else:
        embed = discord.Embed(title=f"Unique Products: 0 | Total Stock: {TotalCount}", color = 0x212129)
        embed.add_field(name='Info:',value='Koniec listy',inline=True)
        embed.set_footer(text="Created by Rafał#6750",icon_url="https://i.imgur.com/yeUP0WC.png")

    return embed

def Setup(user,level,accounttype,successful_ship,quick_ship):
    User_DB = user
    accounttype = str(accounttype).upper()

    successful_ship = str(successful_ship).upper()
    quick_ship = str(quick_ship).upper()

    x = [user_find['User'] for user_find in getDB_settings()['StockX'].find()]
    
    if User_DB in x:
        for element in x:
            if User_DB==element:
                query = {"User":User_DB}
                doc = getDB_settings()['StockX'].find_one(query)

                oldLevel = doc['Info']['Level']
                oldType = doc['Info']['AccountType']
                oldSuccessful_Ship = doc['Info']['SuccessfulShipBonus']
                oldQuickShipBonus = doc['Info']['QuickShipBonus']


                if int(level) != oldLevel or str(accounttype) != oldType or str(successful_ship) != oldSuccessful_Ship or str(quick_ship) != oldQuickShipBonus:
                    getDB_settings()['StockX'].update_one(query,{"$set": {"Info.Level": int(level),"Info.AccountType": str(accounttype),"Info.SuccessfulShipBonus":str(successful_ship),"Info.QuickShipBonus":str(quick_ship)}})
                    log_success(f"Updated {User_DB} info!")

                    embed = discord.Embed(title=f'StockX info updated!', color = 0x212129)
                    return embed
                else:
                    log_success(f"This info was saved previously!")

                    embed = discord.Embed(title=f'Nothing changed in your StockX info', color = 0x212129)
                    return embed
                    
    else:

        data = {
            str("User"):User_DB,
                str("Info"):{
                    "Level":int(level),
                    "AccountType":str(accounttype),
                    "SuccessfulShipBonus":str(successful_ship),
                    "QuickShipBonus":str(quick_ship)
                
            }   
                }

        getDB_settings()['StockX'].insert_one(data)
        log_success(f"[SETUP] Successfully set up {User_DB} account!")
        
        embed = discord.Embed(title=f'StockX info saved!', color = 0x212129)
        return embed
    
def SetupCheck(user):
    User_DB = user

    x = [user_find['User'] for user_find in getDB_settings()['StockX'].find()]

    if User_DB in x:
        for element in x:
            if User_DB==element:
                query = {"User":User_DB}
                doc = getDB_settings()['StockX'].find_one(query)

                oldLevel = doc['Info']['Level']
                oldType = doc['Info']['AccountType']
                oldSuccessful_Ship = doc['Info']['SuccessfulShipBonus']
                oldQuickShipBonus = doc['Info']['QuickShipBonus']

                log_info(f"scrapped {User_DB} stockX info")

                embed = discord.Embed(title=f"Your StockX Info:", color = 0x212129)
                embed.add_field(name="Account Info:",value=f"StockX level: **{oldLevel}**\nAccount Type: **{oldType}**\nSuccessful Ship Bonus: **{oldSuccessful_Ship}**\nQuick Ship Bonus: **{oldQuickShipBonus}**")
                return embed

    else:
        log_info(f"{User_DB} not found in settingsDB!")
        embed = discord.Embed(title=f"Nothing found! Use ./setup_stockx first", color = 0x212129)
        return embed

def CheckByName(user,name):
    User_DB = user

    items = []
    marketData = []
    added_sizes = []
    Shoe_nameDB = [sku_find["Info"]["shoe_name"] for sku_find in getDB()[User_DB].find()]
    settings = [element['User'] for element in getDB_settings()['StockX'].find()]
    if str(User_DB) in settings:
        if str(name) in str(Shoe_nameDB):

            Col = getDB()[User_DB]
            queryName = {'Info.shoe_name':str(name)}
            getSKU = Col.find_one(queryName)
            sku = str(getSKU['SKU'])

            querySKU = {'SKU':sku}

            Col.update_one(querySKU,{'$set':get_NewMarketData(sku)})
            log_info(f"[CHECK] Updated market data for {sku}")

            data = Col.find_one(querySKU)

            for keys in data['Info']['marketInfo']:
                market = data['Info']['marketInfo'][keys]
                marketData.append(market)

            
            imageUrl = data['Info']['photo']
            productName = data['Info']['shoe_name']
            stockxurl = data['Info']['linkstockx']

            for d in data['Size']:
                quantity = data['Size'][d]['Quantity']
                
                if " 1/2" in str(d):
                    d = str(d).replace(" 1/2",".5")

                added_sizes.append(d)

            
            payouts = Stockx_Prices(User_DB,sku)
            if payouts != "brak danych":
            
                PayoutsForSizes = {}
                for key,value in payouts.items():
                    if key in added_sizes:
                        try:
                            PayoutsForSizes[key] = {"Payout Ask":value['PayoutASK'], "Payout Bid":value['PayoutBID'], "Payout Alias":value['PayoutAlias']}
                        except KeyError:
                            PayoutsForSizes[key] = {"Payout Ask":value['PayoutASK'], "Payout Bid":value['PayoutBID']}

                for d in data['Size']:
                    quantity = data['Size'][d]['Quantity']
                    
                    if " 1/2" in str(d):
                        d = str(d).replace(" 1/2",".5")

                    items.append(f"{d} | {quantity} in stock\n")

                    PayoutsForSizes[d]['Quantity'] = quantity

                try:
                    currency_r = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/eur/today/')
                    EurPln = currency_r.json()['rates'][0]['mid']
                    

                    CheckItemsReturn = []
                    for k,v in PayoutsForSizes.items():
                        try:
                            payoutASK = f"{v['Payout Ask']}€ ({round(float(v['Payout Ask'])*float(EurPln))} PLN)"
                            payoutBID = f"{v['Payout Bid']}€ ({round(float(v['Payout Bid'])*float(EurPln))} PLN)"
                            PayoutAlias = f"{v['Payout Alias']}€ ({round(float(v['Payout Alias'])*float(EurPln))} PLN)"
                            CheckItemsReturn.append(f"```{k} | {v['Quantity']} | {payoutASK} | {PayoutAlias}```")
                        except Exception:
                            payoutASK = f"{v['Payout Ask']}€ ({round(float(v['Payout Ask'])*float(EurPln))} PLN)"
                            CheckItemsReturn.append(f"```{k} | {v['Quantity']} | {payoutASK} | N/A```")

                except Exception:
                    CheckItemsReturn = []
                    cr = CurrencyConverter()
                    
                    for k,v in PayoutsForSizes.items():
                        try:
                            payoutASK = f"{v['Payout Ask']}€"
                            payoutASKpln = round(cr.convert(v['Payout Ask'],"EUR",'PLN'),2)
                            payoutBID = f"{v['Payout Bid']}€"
                            PayoutAlias = f"{v['Payout Alias']}€"
                            payoutAliaspln = round(cr.convert(v['Payout Alias'],"EUR",'PLN'),2)
                            CheckItemsReturn.append(f"```{k} | {v['Quantity']} | {payoutASK} ({payoutASKpln}PLN) | {PayoutAlias} ({payoutAliaspln}PLN)```")
                        except Exception:
                            payoutASK = f"{v['Payout Ask']}€"
                            CheckItemsReturn.append(f"```{k} | {v['Quantity']} | {payoutASK} ({payoutASKpln}PLN) | N/A```")
                
                log_success(f"[CHECK] Successfully checked {sku}")
                embed = discord.Embed(title=f"{productName}", color = 0x212129)
                embed.set_thumbnail(url = imageUrl)
                # for i in items:
                #     embed.add_field(name=f"Size | Quantity:", value=f"```{i}```",inline=False)

                embed.add_field(name='Size | Quantity | StockX payout | Alias payout',value=''.join(CheckItemsReturn),inline=False)
                embed.add_field(name="Market Data:",value=f"Last 72h sales: **{marketData[0]}**\nHighest bid: **{marketData[1]}€**\nLast Sale: **{marketData[2]}€**",inline=False)
                embed.add_field(name="SKU:",value=sku,inline=True)
                embed.add_field(name="StockX:",value=f"[[click]]({stockxurl})",inline=True)
                embed.set_footer(text="Created by Rafał#6750",icon_url="https://i.imgur.com/yeUP0WC.png")
                return embed
            
            else:
                embed = discord.Embed(title=f"Setup stockX settings first! ./setup_stockX", color = 0x212129)
                return embed
        
        else:
            log_info(f"{sku} not found in user DB!")
            embed = discord.Embed(title=f"{sku} not found in your DB!", color = 0x212129)
            return embed
    else:
        embed = discord.Embed(title=f"Setup stockX settings first! ./setup_stockX", color = 0x212129)
        return embed
        
def RemoveByName(name,size,quantity,user):
    if ".5" in str(size):
        size = str(size).replace(".5"," 1/2")

    User_DB = user
    Shoe_nameDB = [sku_find["Info"]["shoe_name"] for sku_find in getDB()[User_DB].find()]
    Col = getDB()[User_DB]
    queryName = {'Info.shoe_name':str(name)}
    getSKU = Col.find_one(queryName)
    sku = str(getSKU['SKU'])

    if str(name) in Shoe_nameDB:
        for element in Shoe_nameDB:
            if str(name) == element:
                queryName = {'Info.shoe_name':str(name)}
                getSKU = Col.find_one(queryName)
                skuDB = str(getSKU['SKU'])
                z = [sku['Size'] for sku in getDB()[User_DB].find() if sku['SKU']==skuDB]
                if str(size) in str(z):
                    if int(quantity) >=1:
                    
                        query = {'SKU':skuDB}
                        doc = getDB()[User_DB].find_one(query)
                        for d in doc['Size']:
                            if str(size)==str(d):
                                OldQuantity = doc['Size'][d]['Quantity']
                                
                        
                                NewQuantity = OldQuantity-quantity
                                if NewQuantity == 0:
                                    del doc['Size'][size]
                                    getDB()[User_DB].update_one(query,{'$set':doc})
                                    
                                    checkUpdated = getDB()[User_DB].find_one(query)

                                    log_success(f"[REMOVE] Successfully updated Quantity for {element} | {size}")

                                    if len(checkUpdated['Size'])==0:
                                        getDB()[User_DB].delete_one(query)

                                        log_success(f"[REMOVE] Successfully dropped {name} records")
                                        embed = discord.Embed(title=f"{name} removed from the DB! Last item was deleted!", color = 0x212129)
                                        return embed
                                    else:
                                        embed = discord.Embed(title=f'Removed {quantity} from {name} | {size}', color = 0x212129)

                                        return embed

                                else:
                                    doc['Size'][size]['Quantity'] = int(NewQuantity) 

                                    getDB()[User_DB].update_one(query,{'$set':doc}) 

                                    log_success(f"[REMOVE] Successfully updated Quantity for {element} | {size}")

                                    embed = discord.Embed(title=f'Removed {quantity} from {name} | {size}', color = 0x212129)

                                    return embed
                    else:
                        embed = discord.Embed(title=f'Quantity has to be atleast 1!', color = 0x212129)

                        log_info("[REMOVE] Wrong Quantity, has to be atleast 1!")
                        return embed
                
                else:
                    embed = discord.Embed(title=f'This Shoe-size is not in the DB!', color = 0x212129)
                    log_info("[REMOVE] Wrong Size!")
                    return embed
    else:
        embed = discord.Embed(title=f'This Shoe is not in the DB!', color = 0x212129)

        log_info("[REMOVE] Wrong SKU!")
        return embed
        


    






