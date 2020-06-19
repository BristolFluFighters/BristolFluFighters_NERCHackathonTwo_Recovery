# To add a new cell, type '# # %%'
# To add a new markdown cell, type '# # %% [markdown]'
# # %% [markdown]
# # Import pre-processed datasets
# 
# This notebook imports the preprocessed datasets which come with this repository.
# 

# # %%
import pandas as pd
import os


# # %%
default_data_dir = "data/processed"

data_files = os.listdir(default_data_dir)

def shortest_country_match(df, column, country):
    possible_finds = find_matching_geo_id(df, find_str=country, search_col=column)
    len_current = 10000000000

    current_find = ""
    for find in possible_finds:
        if len(find) < len_current:
            len_current = len(find)
            current_find = find
    
    return current_find

class DataSet(object):
    default_date_column_names = [
        "date", "Date", "timestamp"
    ]
    default_country_column_names = [
        "unique_geo_id", "Country", "city"
    ]
    default_data_types = [
        "historical_GHG", "mobility", "energy_daily"
    ]

    def __init__(
        self,
        df:pd.DataFrame,
        data_columns:list,
        dataset_name="",
        data_type = None,
        date_column_name=None,
        country_column_name=None,
        country_column_fun=None,
        country_fun=shortest_country_match,
    ):
        self.df = df
        self.data_columns = data_columns
        self.date_column_name = date_column_name
        self.country_column_name = country_column_name
        self.country_column_fun = country_column_fun
        self.country_fun = country_fun
        self.dataset_name = dataset_name
        self.data_type = data_type

        # Input validation
        self._guess_country_column()
        self._guess_date_column()
        self._guess_data_type()

        self.df.set_index(
            pd.MultiIndex.from_frame(
                self.df[[self.country_column_name, self.date_column_name]]
            ), inplace=True
        )
        self.df.sort_index(inplace=True)
        self.country_cache = {}

    def _guess_date_column(self):
        if self.date_column_name is None:
            for date_col in DataSet.default_date_column_names:
                if date_col in self.df.columns:
                    self.date_column_name = date_col
        else:
            # if the specified date_column does not exist in df
            # remove it
            if self.date_column_name not in self.df.columns:
                self.date_column_name = None
        
        if self.date_column_name is None:
            raise ValueError("Invalid `date_column_name` or dataframe, cannot find date")

    def _guess_country_column(self):
        if self.country_column_name is None:
            for geo_col in DataSet.default_country_column_names:
                if geo_col in self.df.columns:
                    self.country_column_name = geo_col
        else:
            # if the specified country_column does not exist in df
            # remove it
            if self.country_column_name not in self.df.columns:
                self.country_column_name = None
        
        if self.country_column_name is None:
            raise ValueError("Invalid `country_column_name` or dataframe, cannot find geo")

    def _guess_data_type(self):
        if self.data_type is None:
            for geo_col in DataSet.default_data_types:
                if geo_col in self.dataset_name:
                    self.data_type = geo_col
        else:
            # if the specified data_type does not exist in df
            # remove it
            if self.data_type not in self.df.columns:
                self.dataset_name = None
        if not self.dataset_name:
            print("WARNING: Please define dataset_name to use class DataSet")
        elif self.data_type is None:
            raise ValueError("Unrecognised `data_type` or dataset_name")

    def remove_from_cache(self, country):
        self.country_cache.pop(country)

    def clear_cache(self):
        self.country_cache = {}

    def get_country_string(self, country:str):
        if country not in self.country_cache:
            best_guess = self.country_fun(
                self.df,
                self.country_column_name,
                country
            )
            if best_guess:
                self.country_cache[country] = best_guess
            else:
                raise ValueError(
                    f'"{country}" could not be found by '
                    +f'function `{self.country_fun.__name__}`')
        return self.country_cache[country]

    def get_country(self, country:str):
        return self.df.loc[self.get_country_string(country)]

    def get_country_data(self, country:str):
        return self.df.loc[self.get_country_string(country), self.data_columns]

    def summarise(self):
        print("=========================================")
        print(self.dataset_name)
        print("--------------------------------------")
        print(self.data_columns)
        print("--------------------------------------")
        print(self.df.info())
        print("--------------------------------------")
        print()


class DataGroup(dict):
    def __init__(self, iterable):
        super().__init__(iterable)
    
    def get_country(self, country):
        d_uk = {}
        for dset in self:
            try:
                d_uk[dset] = self[dset].get_country(country)
                print(f"Success: {dset}")
            except:
                print(f"Failed: {country} not in {dset}")
        return d_uk


# # %% [markdown]
# ## Define import processes
# 
# The idea is that all data sets are read and will all be indexed by a DateTime series and possibly other indices if helpful.
# 

# # %%
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
        # index cols are repeated in the datasets so appear with a .1
        df.drop([f"{c}.1" for c in index_cols], axis=1, inplace=True)
        df.set_index(
            pd.MultiIndex.from_frame(df[index_cols]), inplace=True
        )

    if isinstance(first_data_column, type(str())):
        first_data_column = df.columns.get_loc(first_data_column)
        
    data_fields = df.columns[first_data_column:]
    return (df, data_fields)

# # %% [markdown]
# ### historical green house gas emissions
# 
# 
# define `read_historical_GHG`

# # %%
def read_historical_GHG(file_in, dir_in=default_data_dir):
    ''' Read in preprocessed historical GHG data.

    Arguments:
        file_in (str): Name of file
        dir_in (str): Directory of file
    
    Returns
        (DataFrame, list): The data of the file loaded in a dataframe
        and a list indicating which columns contain the data of interest
    '''
    data_pos = 6
    data_set, data_cols = read_multi_indexed_csv(file_in, data_pos, dir_in=default_data_dir)
    # deindex by gas as it is not general, instead different gases are gonna get different 
    # columns
    data_set = data_set.reorder_levels([1, 0, 2])
    new_data_set = data_set.drop(labels=['max_year', 'GH_Gas', *data_cols], axis='columns')
    new_data_set.drop_duplicates(ignore_index=True, inplace=True)
    new_data_set.set_index(
        pd.MultiIndex.from_frame(new_data_set[["Country", "date"]]), inplace=True
    )
    
    for i, gas in enumerate(data_set.GH_Gas.unique()):
        
        temp_set = data_set.loc[gas, data_cols]
        temp_set.rename({c:f"{c} ({gas})" for c in data_cols}, axis='columns', inplace=True)

        new_data_set = new_data_set.join(temp_set)

    new_data_set.dropna(axis='columns',how='all', inplace=True)
    new_data_set.sort_index(inplace=True)
    data_cols = new_data_set.columns[data_pos-2:]
    return new_data_set, data_cols
    
    

# # %% [markdown]
# ### Read mobility data
# 
# 
# define `read_mobility_file`

# # %%
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
    id_vars = df.columns[:1]
    date_vars = df.columns[1:]
    df = df.melt(
        id_vars=id_vars, value_vars=date_vars,
        var_name="city", value_name='citymapper_mobility_index'
    )
    df.set_index(
        pd.MultiIndex.from_frame(df[["city", "Date"]]), inplace=True
    )
    col = df.columns[2:]
    return df, col

# # %% [markdown]
# ### load uk energy
# 
# 
# define `read_uk_energy`

# # %%
def read_uk_energy(file_in, dir_in=default_data_dir):
    df, col = read_multi_indexed_csv(
        file_in, 1, dir_in=default_data_dir
    )
    df["Country"] = "United Kingdom"
    return df.set_index('timestamp', drop=False), col

# # %% [markdown]
# ## Read in the data
# 
# Now we map each file to the appropriate function

# # %%
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

# # %% [markdown]
# And with a single loop all the different data sets are loaded.

# # %%

def load_data_files(data_files=None, file_read_functions=None):
    """Processes a set of data files and 
    """
    if data_files is None:
        data_files = os.listdir(default_data_dir)

    if file_read_functions is None:
        file_read_functions = default_file_read_functions

    data_sets = DataGroup({})
    for data_file in data_files:
        data_name, _ = os.path.splitext(data_file)
        try:
            data, col = file_read_functions[data_file](data_file)
            data_sets[data_name] = DataSet(data, col, data_name)
        except KeyError as eid:
            print(
                'WARNING:'
                f' "{data_file}" not found in dictionary `file_read_functions`.\n'
                + 'A loading function must be defined in `data_access.default_file_read_functions`.'
            )            
        
    return data_sets

# # %% [markdown]
# ### Summary of available data

# # %%
def summarise_data(data_sets):
    for data in data_sets:
        data_sets[data].summarise()

# # %%

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
