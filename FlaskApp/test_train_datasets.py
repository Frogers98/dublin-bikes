from FlaskApp.methods import *
from FlaskApp.data_dictionary import database_dictionary, fr_database_dictionary, js_database_dictionary
from sklearn.model_selection import train_test_split

myhost=database_dictionary['endpoint']
myuser=database_dictionary['username']
mypassword=database_dictionary['password']
myport=database_dictionary['port']
mydb=database_dictionary['database']

# Create new tables if they are not there already
setup_database(myhost, myuser, mypassword, myport, mydb)
# Load the engine to connect to the database and load the entire availability table as a dataframe before splitting it
engine = connect_db_engine(myhost,myuser,mypassword,myport,mydb)
engine = engine[1]
print("about to load df")
df = pd.read_sql_table("01_availability", engine)
print("df loaded")



def get_randomised_data(engine, df):
    """Function to split the dataframe randomly into testing and training data and store these sets as tables in the db"""
    #print(df.head(5))
    # Splits the dataset into training and testing sets
    # 70% training data, 30$ testing data
    print("about to split into train and test")
    train, test = train_test_split(df, test_size=0.3)
    print("finished loading train and test dataframes")

    train.to_sql(name='02_availability_train', con=engine, if_exists='replace', index=False)
    print("finished loading data into 02_availability_train")
    test.to_sql(name='02_availability_test', con=engine, if_exists='replace', index=False)
    print("finished loading data into 02_availability_test")
    return

def get_data_by_date(engine,df):
    """Function to split the training and test data by date, i.e. the first 70% of dates are training and last 30% are testing"""
    print("about to split into train and test")
    # Sort dataframe by created_date
    df = df.sort_values(by=['created_date'])
    # Create a dataframe with the first 70% of values to use as training data
    train = df.head(int(len(df)*0.7))
    # Create a dataframe with the last 30% of values to use as testing data
    test = df.tail(int(len(df) * 0.3))
    print("finished loading train and test dataframes")

    train.to_sql(name='02_availability_train', con=engine, if_exists='replace', index=False)
    print("finished loading data into 02_availability_train")
    test.to_sql(name='02_availability_test', con=engine, if_exists='replace', index=False)
    print("finished loading data into 02_availability_test")
    return

# Can call either function depending on whether you want randomised training/test data or want it split by date
# By default this progoram will split the data by date

# get_randomised_data(engine, df)
get_data_by_date(engine, df)