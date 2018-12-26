
def get_city_code(p_state, p_state_name, file, p_date = '2018-11-11'):

    import numpy as np
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    from datetime import datetime
    
    max_retries = 5    
    df_code = pd.DataFrame()
    errors = list()
    errors_t = list()
    
    date_load = datetime.strptime(p_date, "%Y-%m-%d")
    
    if isinstance(p_state, str):
        p_state = [p_state]
    if isinstance(p_state_name, str):
        p_state_name = [p_state_name]
    
    
    for country_i in range(len(p_state)):

        id_list = list()
        text_list = list()

        url_const = "https://www.ogimet.com/cgi-bin/" 
        params = "&ano=" + str(date_load.year) + "&mes=" + str(date_load.month) + "&day=" + str(date_load.day)
        url = url_const + "gsynext?lang=en" + "&state=" + p_state[country_i] + "&rank=100" + params + "&hora=" + '23' + "&Send=send"
        
        for _ in range(max_retries):

            try:    
                response = requests.get(url)

                try:
                    results_page = BeautifulSoup(response.content,'lxml')
                    cities = results_page.find_all('a')
                    for city in cities:
                        city_code = city.get('href')
                        city_text = city.get_text()

                        if city_code is not None:
                            if city_code.find(params) != -1:
                                city_code = city_code[city_code.find("&ind=")+5:city_code.find("&ind=")+5+5]
                                city_text = city_text[0:city_text.find(p_state_name[country_i])-1]
                                if city_code not in id_list:
                                    id_list.append(city_code)
                                    text_list.append(city_text)
                        else:
                            id_list = id_list
                            text_list = text_list

                    df_code_i = pd.DataFrame(list(zip(text_list,id_list)), columns=['name', 'id'])
                    df_code_i.loc[:,'country'] = p_state_name[country_i]
                    df_code_i = df_code_i.sort_values(by='id', ascending=True, na_position='last').reset_index(drop=True)
                    df_code = df_code.append(df_code_i,ignore_index=True)
                    
                except ValueError:
                    errors.append('ValueError for: ' + p_state_name[country_i])

                break
                
            except TimeoutError:
                errors_t.append('TimeoutError for: ' + p_state_name[country_i])
            except:
                errors.append('Error for: ' + p_state_name[country_i])    
                
     
    values, counts = np.unique(errors_t, return_counts=True)
    item_index = np.where(np.array(counts) == max_retries)
    errors_t1 = values[item_index].tolist()
    
    [print(e) for e in np.unique(errors)]
    [print(e_t) for e_t in np.unique(errors_t1)]
    
        
    if file is not None: 
        df_code.to_csv(file, sep=';', encoding='utf-8', index=False)
       
    return df_code



df_a = get_city_code(p_state='Pola', p_state_name='Poland', file='output/city_code_pl.csv')
df_b = get_city_code(p_state=['Pola', 'Germ'], p_state_name=['Poland', 'Germany'], file='output/city_code_pl_de.csv')



