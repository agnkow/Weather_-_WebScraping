
def get_weather(date_start, date_end, city_id, file):   
    
    import numpy as np
    import pandas as pd
    from datetime import datetime, date, timedelta
    import requests
    from bs4 import BeautifulSoup
    from tqdm import tqdm
    import pathlib
    import csv
    
    max_retries = 5
    cols_var = ['Date','T(C)','Id','Tmax(C)','ffkmh','Snow(cm)','Gustkmh','Tmin(C)','ddd','Td(C)',
                'Nt','P seahPa','Viskm','HKm','Nh','PTnd','InsoD-1','P0hPa','WW','Prec(mm)']
    errors = list()
    errors_t = list()
    
    if isinstance(city_id, int) or isinstance(city_id, str):    
        city_id = [city_id]
    
    date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
    date_end = datetime.strptime(date_end, "%Y-%m-%d").date()
    delta = date_end - date_start
    
    date_period = list()
    for i in range(delta.days + 1):
        date_period.append(date_start + timedelta(i))   
    pbar = tqdm(total = len(date_period) * len(city_id))

	
    for date_i in range(delta.days + 1):
        date_load = (date_start + timedelta(date_i))
        
        for city_i in range(len(city_id)):

            p_year = date_load.year
            p_month = date_load.month
            p_day = date_load.day
            p_hour = '23'

            url_const = "https://www.ogimet.com"
            n_days = str(1)
            params_time = "&ano=" + str(p_year) + "&mes=" + str(p_month) + "&day=" + str(p_day) + "&hora=" + str(p_hour)
            url = url_const + "/cgi-bin/gsynres?" + "ind=" + str(city_id[city_i]) + "&lang=en&decoded=yes" + "&ndays=" + n_days + params_time  
            
            for _ in range(max_retries):
                
                try:
                    response = requests.get(url)

                    try:  
                        results_page = BeautifulSoup(response.content,'lxml')
                        table_tag = results_page.find('table', attrs={'bgcolor':'#d0d0d0'})
                        
                        def all_th():
                            all_th_tags = table_tag.find_all('th')
                            for var_name in all_th_tags:
                                var_name_text = var_name.get_text()
                                yield var_name_text       
                        list_names = list(all_th())

                        df_result = pd.DataFrame(columns=list_names)
                        for tr in range(0,len(table_tag.find_all('tr'))-2):
                            row_result = list()
                            for td in range(0,len(list_names)):
                                row_result.append(table_tag.find_all('tr')[tr+1].find_all('td')[td].get_text())   
                            df_result.loc[tr] = row_result

                        if len(df_result) > 0:
                            df_result.loc[:,'Id'] = int(city_id[city_i])
                            

                            ## without providing variable names; unique elements in csv
                            #f = pathlib.Path(file)
                            #if not f.exists ():
                            #    df = pd.DataFrame(columns=['weather'])
                            #    df.to_csv(file, index = False)
                            #    
                            #df_saved = pd.read_csv(file, encoding="utf-8")
                            #if len(df_saved) == 0:
                            #    df_saved_2 = df_result
                            #else:
                            #    cols_to_use = list(set(df_result.columns) & set(df_saved.columns))
                            #    df_saved_2 = pd.merge(df_saved, df_result, on=cols_to_use, how='outer').drop_duplicates()
                            #sort_column = ['Date', 'T(C)', 'Id'] + list((set(df_saved_2.columns) - set(['Date', 'T(C)', 'Id'])))
                            #df_saved_2 = df_saved_2[sort_column]
                            #df_saved_2.to_csv(file, index = False, encoding="utf-8")
              
                            # with providing variable names
                            cols_to_use = list(set(df_result.columns) & set(cols_var))
                            cols_add = list(set(cols_var) - set(cols_to_use))

                            df_result = df_result[cols_to_use]
                            for add_i in range(len(cols_add)):
                                df_result[cols_add[add_i]] = '-'
                            df_result = df_result[cols_var]
                            
                            f = pathlib.Path(file)
                            if f.exists ():
                                with open(file,'a',newline='') as fd:
                                    writer = csv.writer(fd)
                                    for row in range(len(df_result)):
                                        writer.writerow(list(df_result.loc[row]))     
                            else:
                                df_result.to_csv(file, index = False, encoding="utf-8")


                    except ValueError:
                        errors.append('ValueError for: ' + 'code_' + city_id[city_i] + ' - ' + str(date_load))

                    break

                except TimeoutError:
                    errors_t.append('TimeoutError for: ' + 'code_' + city_id[city_i] + ' - ' + str(date_load))
                except:
                    errors.append('Error for: ' + 'code_' + city_id[city_i] + ' - ' + str(date_load))        
            
            pbar.update(1)
    
    
    values, counts = np.unique(errors_t, return_counts=True)
    item_index = np.where(np.array(counts) == max_retries)
    errors_t1 = values[item_index].tolist()
    
    [print(e) for e in np.unique(errors)]
    [print(e_t) for e_t in np.unique(errors_t1)]
    
    df_saved = pd.read_csv(file, encoding="utf-8")
    
    return df_saved

	

	


# Example:	
df_weather = get_weather(date_start = '2018-11-11', date_end = '2018-11-12',
			 city_id = ['12566', '10381'], file = 'output/weather_test.csv')


						   
						   
