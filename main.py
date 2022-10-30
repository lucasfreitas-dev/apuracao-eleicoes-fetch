from urllib import response
import requests as rq
import pandas as pd
import os
import time

uf_list = [ 'ac' , 'al' , 'ap' , 'am' , 'ba' , 'ce' , 'df' , 'es' , 'go' , 'ma' , 'mt' , 'ms' , 'mg' , 'pr' , 'pb' , 'pa' , 'pe' , 'pi' , 'rj' , 'rn' , 'rs' , 'ro' , 'rr' , 'se' , 'sc' , 'sp' , 'to', 'zz' ]

def fetch_data_json(UF):
    
    try:
        response = rq.get(f"https://resultados.tse.jus.br/oficial/ele2022/545/dados-simplificados/{UF}/{UF}-c0001-e000545-r.json").json()
    except:
        print(f"## Fail to get data from UF: {UF}")
        return
    return response

def check_and_update_data(UF):
    old_csv = pd.read_csv(f"{UF}.csv")
    new_response = pd.DataFrame(fetch_data_json(UF))

    if("hg" in new_response and old_csv["hg"][0] != new_response["hg"][0]):
        pd.concat([old_csv, new_response])

def create_csv(UF):
    if f"{UF}.csv" not in os.listdir():
        pd.DataFrame(fetch_data_json(UF)).to_csv(f"{UF}.csv")

def start():
    print("## Fetching data...")
    for uf in uf_list:
        create_csv(uf)
        check_and_update_data(uf)
    print("## Done.")

while(True):
    start()
    time.sleep(60)
