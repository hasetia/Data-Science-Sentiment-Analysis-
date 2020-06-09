def word_count(string):
    #Replaced the \n with space
    cont = re.sub('\n{1,}', ' ', string)
    #Replace any spaces in groups of 2 or more with just 1 space
    cont = re.sub(' {2,}', ' ', cont)
    #Split the content on space, and then find the contents length
    return len(cont.split())

#This function will assign a state to the row of the dataframe depending on the conditions that are met
def give_state(string):
    if string in cal_schools:
        return 'cal'
    elif string in tex_schools:
        return 'tex'
    elif string in fl_schools:
        return 'fl'
    else:
        print('ERROR')
        return 'ERROR'
    
    
def fix_year(string):
    string = string.replace('April', 'Apr') # the only case where it wasn't abbreviated
    if string[-4:] != '2020': #if it wasn't properly formatted
        if string[-2:] == '20': # still had some year, but not all
            return string+'20' #only add the last two digits
        else: # had no year data at all
            return string+'-2020' # add the entire year
    else:
        return string
    
# create function that will output dataframe 
# that stores sentiment information
def get_sentiments(input_list):
    
    output = pd.DataFrame()

    for sentence in input_list:
        ss = analyser.polarity_scores(sentence)
        ss['sentence'] = sentence
        output = output.append(ss, ignore_index=True)

    return output


def sort_df(word):
    new = allSchools[allSchools['content'].str.contains(word, case=False)]
    new = new.reset_index(drop = True)
    new_list = list(new['content'].values)
    new_sentiments = get_sentiments(new_list)
    
    new = new.drop(['token', 'stop'], axis = 1)
    new = new.assign(pos = new_sentiments['pos'])
    new = new.assign(neg = new_sentiments['neg'])
    new = new.assign(neu = new_sentiments['neu'])
    new = new.assign(compound = new_sentiments['compound'])
    
    return new

