# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Import pre-processed datasets
# 
# This notebook imports the preprocessed datasets which come with this repository.
# 

# %%
import pandas as pd
import os


# %%
default_data_dir = "data/processed"

data_files = os.listdir(default_data_dir)


# %% [markdown]
# ## Define import processes
# 
# The idea is that all data sets are read and will all be indexed by a DateTime series and possibly other indices if helpful.
# 

# %%
def read_multi_indexed_csv(file_in, first_data_column, dir_in=default_data_dir):
    ''' Read in preprocessed historical GHG data.

    Arguments:
        file_in (str): Name of file
        first_data_column (str|int) : index or name of first column with data
        dir_in (str): Directory of file
    
    Returns
        (DataFrame, list): The data of the file loaded in a dataframe
        and a list indicating which columns contain the data of interest
    '''
    if not (
        isinstance(first_data_column, type(str()))
        or isinstance(first_data_column, type(int()))
    ) :
        raise TypeError("`first_data_column` must be a column name or an int")

    file_path = os.path.join(dir_in, file_in)
    df = pd.read_csv(file_path)
    index_cols = [c for c in df.columns if c + '.1' in df.columns]
    
    for col in ["date", "Date", "timestamp"]:
        if col in df:
            df[col] = pd.to_datetime(df[col])
    
    if index_cols:
        df.drop([f"{c}.1" for c in index_cols], axis=1, inplace=True)
        df.set_index(
            pd.MultiIndex.from_frame(df[index_cols]), inplace=True
        )

    if isinstance(first_data_column, type(str())):
        first_data_column = df.columns.get_loc(first_data_column)
        
    data_fields = df.columns[first_data_column:]
    return (df, data_fields)

# %% [markdown]
# ### historical green house gas emissions
# 
# 
# define `read_historical_GHG`

# %%
def read_historical_GHG(file_in, dir_in=default_data_dir):
    ''' Read in preprocessed historical GHG data.

    Arguments:
        file_in (str): Name of file
        dir_in (str): Directory of file
    
    Returns
        (DataFrame, list): The data of the file loaded in a dataframe
        and a list indicating which columns contain the data of interest
    '''
    return read_multi_indexed_csv(file_in, 6, dir_in=default_data_dir)

# %% [markdown]
# ### Read mobility data
# 
# 
# define `read_mobility_file`

# %%
def read_mobility_google(file_in, dir_in=default_data_dir):
    return read_multi_indexed_csv(
        file_in, 
        'retail_and_recreation_percent_change_from_baseline',
        dir_in=default_data_dir
    )

def read_mobility_apple(file_in, dir_in=default_data_dir):
    return read_multi_indexed_csv(
        file_in, 
        'driving',
        dir_in=default_data_dir
    )

def read_mobility_citymapper(file_in, dir_in=default_data_dir):
    df, col = read_multi_indexed_csv(
        file_in, 1, dir_in=default_data_dir
    )
    return df.set_index('Date', drop=False), col

# %% [markdown]
# ### load uk energy
# 
# 
# define `read_uk_energy`

# %%
def read_uk_energy(file_in, dir_in=default_data_dir):
    df, col = read_multi_indexed_csv(
        file_in, 1, dir_in=default_data_dir
    )
    return df.set_index('timestamp', drop=False), col

# %% [markdown]
# ## Read in the data
# 
# Now we map each file to the appropriate function

# %%
# Map files to a function that will read it properly
default_file_read_functions = {
    'historical_GHG_Sectors_GCP.csv': read_historical_GHG,
    'historical_GHG_Sectors_PIK.csv': read_historical_GHG,
    'historical_GHG_Sectors_UNFCCC.csv': read_historical_GHG,
    'mobility_apple.csv': read_mobility_apple,
    'mobility_citymapper.csv': read_mobility_citymapper,
    'mobility_google.csv': read_mobility_google,
    'uk_energy_daily.csv': read_uk_energy,
}

# %% [markdown]
# And with a single loop all the different data sets are loaded.

# %%

def load_data_files(data_files=None, file_read_functions=None):
    """Processes a set of data files and 
    """
    if data_files is None:
        data_files = os.listdir(default_data_dir)

    if file_read_functions is None:
        file_read_functions = default_file_read_functions

    data_sets = {}
    data_columns = {}
    for data_file in data_files:
        data_name, _ = os.path.splitext(data_file)
        try:
            data_sets[data_name], data_columns[data_name] = \
                file_read_functions[data_file](data_file)
        except KeyError as eid:
            raise KeyError(
                f'key "{data_file}" not found in dictionary `file_read_functions`.\n'
                + 'It '
            )            
        
    return data_sets, data_columns

# %% [markdown]
# ### Summary of available data

# %%
def summarise_data(data_sets, data_columns):
    for data in data_sets:
        print("=========================================")
        print(data)
        print("--------------------------------------")
        print(data_columns[data])
        print("--------------------------------------")
        print(data_sets[data].info())
        print("--------------------------------------")
        print()

# %%

def find_matching_geo_id(
    df, 
    find_str='FR_France', 
    exclude_str='This garbage is not a country name',
    search_col='unique_geo_id',
):
    '''Finds values containing `find_str` in column `search_col` of df.
    '''
    return [
        name for name in df[search_col].unique()
            if find_str in name 
            if exclude_str not in name
    ]