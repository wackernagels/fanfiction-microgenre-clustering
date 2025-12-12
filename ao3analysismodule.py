import pandas as pd

def csvtodf(filename):
    """unpacking the text from csv into two dfs. one is in the format of chapter per row and one in work per row"""
    data= pd.read_csv(filename)
    data= data.fillna('')
    data['expected_chapters']= data['expected_chapters'].replace('', 0)
    data= data.convert_dtypes()

    data['date_edited']=pd.to_datetime(data['date_edited'], utc=True, format='%Y-%m-%d %H:%M:%S')
    data['date_published']=pd.to_datetime(data['date_published'], utc=True, format='%Y-%m-%d %H:%M:%S')
    data['date_updated']=pd.to_datetime(data['date_updated'], utc=True, format='%Y-%m-%d %H:%M:%S')
    
    data= data.sort_values(by=['date_published', 'title'])
    data.reset_index(inplace=True, drop=True)
    
    fulltextdata= data.groupby("workurl").agg(lambda x: list(x.unique()) if x.nunique() > 1 else x.iloc[0])
    fulltextdata= fulltextdata.sort_values(by=['date_published', 'title'])
    fulltextdata.reset_index(inplace=True, drop=True)
    
    return {'bychapter': data, 'bywork': fulltextdata}

def filterbydate(df, start= '2015-01-01 00:00:00+00:00', end= '2025-12-31 00:00:00+00:00'):  
    '''filters dataframe by date published. default start is 1/1/2020 and default end is 12/31/2025'''  
    filtered= df[(df['date_published'] >= start) & (df['date_published'] <= end)]
    return filtered

#filter by number chapters
def filterbychapternum(df, min= 0, max= 999999):   
    '''filters dataframe by number of chapters. default minimum is 0 and default maximum is 999999'''   
    filtered= df[(df['nchapters'] >= min) & (df['nchapters'] <= max)]
    return filtered

#filter by language
def filterbylanguage(df, language):
    '''filters dataframe by language. language must be capitalized'''
    filtered= df[df['language'].str.contains(language, na=False)]
    return filtered

def retrievetags(df):
    '''returns a list of all tags in the dataframe'''
    rows= df['tags']
    tagslist=[]
    for row in rows:
        tagslist= tagslist + row.split(',')
    return [x for x in tagslist if x.strip()]

def filterbyfandom(df, fandom):
    '''filters dataframe by fandom. use this instead of groupby to get the proper groupings'''
    filtered= df[df['fandoms'].str.contains(fandom, na=False)]
    return filtered

def retrieveratings(df):
    '''returns a list of all ratings in the dataframe'''
    rows= df['rating']
    ratings=[]
    for row in rows:
        ratings= ratings + row.split(',')
    return ratings

def retrievewarnings(df):
    '''returns a list of all warnings in the dataframe'''
    rows= df['warnings']
    warnings=[]
    for row in rows:
        warnings= warnings + row.split(',')
    return warnings

def retrievecharacters(df):
    '''returns a list of characters tagged in the dataframe with no duplicates'''
    rows= df['characters']
    characterlist=[]
    for row in rows:
        characterlist= characterlist + row.split(',')
    return list(dict.fromkeys(characterlist))#removes duplicates

def filterbyratings(ratings,df):
    'input ratings in a list, returns dataframe with works that have those ratings'
    filtered= df[df['rating'].str.contains('|'.join(ratings), na=False)]
    return filtered

def filterbytags(tags, df):
    'input tags in a list, returns dataframe with works that contain those tags'
    filtered= df[df['tags'].str.contains('|'.join(tags), na=False)]
    return filtered