from FlaskApp.methods import *
from FlaskApp.data_dictionary import database_dictionary, fr_database_dictionary, js_database_dictionary
from sklearn.model_selection import train_test_split

myhost=database_dictionary['endpoint']
myuser=database_dictionary['username']
mypassword=database_dictionary['password']
myport=database_dictionary['port']
mydb=database_dictionary['database']

setup_database(myhost, myuser, mypassword, myport, mydb)

engine = connect_db_engine(myhost,myuser,mypassword,myport,mydb)
engine = engine[1]
print("about to load df")
df = pd.read_sql_table("01_availability", engine)
print(df.head(5))
print("df loaded")
# Splits the dataset into training and testing sets
# 70% training data, 30$ testing data
print("about to split into train and test")
train, test = train_test_split(df, test_size=0.3)

print("finished loading train and test dataframes")

train.to_sql(name='02_availability_train', con=engine, if_exists='replace', index=False)
print("finished loading data into 02_availability_train")
test.to_sql(name='02_availability_test', con=engine, if_exists='replace', index=False)
print("finished loading data into 02_availability_test")