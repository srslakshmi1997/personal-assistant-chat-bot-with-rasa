import pandas as pd

def get_special_day(params):
    var_special_day_result = ""
    var_query_name = ""
    var_fail_reason = ""
    ## Open CSV file ##
    special_df = pd.read_csv("specialdaysdata.csv" , index_col='query_name')
    ## Read parameter to fetch in the CSV file# 
    name_key = params['query_name'].strip().lower()
    name_key = ' '.join(list(map(lambda s:s.capitalize(),name_key.split(' '))))
    special_key = params['special_day'].lower()
    ##Check Synonym words for birthday##
    if special_key in ['birthday','bday','birth anniversary','birth', 'born','bornday']:
        special_key = 'Birthday'
        var_special_day = "birthday"
    ##Check Synonym words for Joining day##
    if special_key in ['joining day','joiningday','work anniversary','join', 'joined','work']:
        special_key = 'Joiningday'
        var_special_day = "work anniversary"
    ## CSV hit success case : name and special day present##
    if (name_key in special_df.index) and (special_key in list(special_df)) :
        sp_result = special_df.loc[name_key][special_key]
        var_special_day_result = sp_result
        var_query_name = name_key
    ## Name not present in the csv file##
    elif name_key not in special_df.index :
        var_fail_reason = "name"
    ## day is not present in the csv file##
    else :
        var_fail_reason = "day"
        
    return(var_fail_reason,var_special_day_result)


def get_sme(params):
    var_fail_reason = ""
    var_sme_result = ""
    ## Open CSV file ##
    sme_df = pd.read_csv("SME.csv" , index_col='item_search')
    ## Read parameter to fetch in the CSV file#     
    #item_key = params['item_search'].lower()
    item_key = params['item_search'].lower()
    ## Initialize the result list##
    sme_result = []
    ## PRODUCT DICTIONARY to get the Synonym which doesnt work in this erraticly working engine
    product_dict = {
        'Physics' : ['science','phy','physics','space','planets'],
        'Chemistry' : ['che','chemical','medicine'],
        'English' : ['language','eng', 'english','vocabulary','vocab']
    }
    ##Iterate dist keys to find synonym##
    for item_val in product_dict.keys():
        if item_key in product_dict[item_val]:
            item_key = item_val
            sme_result = list(sme_df.loc[item_key])
            break
    if sme_result == []:
        var_fail_reason = "search_key"
        return(var_fail_reason,var_sme_result)
    name = []
    email = []
    final_result = ''
    numb = 1

    final_list = list(filter(lambda x : pd.isnull(x) != True , sme_result))
    name = final_list[::2]
    email = final_list[1::2]
    item_list = zip(name,email)

    for (item_name,item_email) in list(item_list) :
        final_result = final_result +'\n'+ str(numb)+'. '+ item_name +' at '+ item_email 
        numb = numb+1

    var_sme_result = final_result
         
    return(var_fail_reason,var_sme_result)

def get_about_person(params):
    var_fail_reason = ""
    var_colleague_result = ""
    special_df = pd.read_csv("specialdaysdata.csv" , index_col='query_name')
    person_name = params['query_name'].strip().lower()
    person_name = ' '.join(list(map(lambda s:s.capitalize(),person_name.split(' '))))
    if person_name not in special_df.index:
        var_fail_reason = "name"
        return(var_fail_reason,var_colleague_result)
    else :
        specialday_col_list = list(special_df)
        zip_tuple = zip(specialday_col_list,list(special_df.loc[person_name]))
        special_df_dict = { key_val:str(key_options).strip() for (key_val,key_options) in list(zip_tuple)}
        if special_df_dict['Gender']=='M':
            val_gender = 'He'
            val_g = 'his'
        else :
            val_gender = 'She'
            val_g = 'her'
        specialday_col_list = specialday_col_list[:-1]
        special_days_wording = {'Name' : person_name,
                            'Joiningday' : 'joined on ' + special_df_dict['Joiningday']+'. ',
                            'Designation' : val_gender+' is working as '+ special_df_dict['Designation'],
                            'Team' : ' in ' + special_df_dict['Team']+'. ',
                            'Masters' : val_gender +' has completed '+val_g+ ' Masters degree in ' +special_df_dict['Masters'],
                            'Masters University' : ' from ' +special_df_dict['Masters University']+'. ' ,
                            'Bachelors' : val_gender +' has completed '+val_g+ ' Bachelors degree in ' +special_df_dict['Bachelors'],
                            'Bachelors University' : ' from ' +special_df_dict['Bachelors University']+'. ',
                            'Prior work' : 'Prior joining, ' + val_gender + ' worked with ' + special_df_dict['Prior work']+'. ',
                            'hobby' : person_name + '\'s hobby is '+ special_df_dict['hobby']+' and ',
                            'Birthday' : val_g+' birthday is on '+special_df_dict['Birthday']+'. ',
                            'Contact details' : person_name+' can be reached at '+special_df_dict['Contact details']
                            }
        sentwords = special_days_wording['Name']+' '
        for sent in specialday_col_list:
            if special_df_dict[sent] != 'nan':
                sentwords += special_days_wording[sent]
        var_colleague_result = sentwords
    return (var_fail_reason,var_colleague_result)



