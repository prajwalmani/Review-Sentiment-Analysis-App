import pandas as pd 
from glob import glob

file='Clothing_Shoes_and_Jewelry.json'

df_json=pd.read_json(file,chunksize=1000000,lines=True)
counter=1


for chunk in df_json:
    new_df=pd.DataFrame(chunk[['overall','reviewText','summary']])
    new_df1=new_df[new_df['overall']==5].sample(4000)
    new_df2=new_df[new_df['overall']==4].sample(4000)
    new_df3=new_df[new_df['overall']==3].sample(8000)
    new_df4=new_df[new_df['overall']==2].sample(4000)
    new_df5=new_df[new_df['overall']==1].sample(4000)
    new_df6=pd.concat([new_df1,new_df2,new_df3,new_df4,new_df5],axis=0,ignore_index=True)
    new_df6.to_csv(f"{counter}.csv",index=False)
    new_df=None
    print("We are in",counter)
    counter+=1

file_names=glob("*.csv")
dataframes=[pd.read_csv(f) for f in file_names]
frame=pd.concat(dataframes,axis=0,ignore_index=True)
frame.to_csv('balanced_review.csv',index=False)
frame.info()
