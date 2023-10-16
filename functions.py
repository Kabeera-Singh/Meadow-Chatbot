import pandas as pd
import numpy as np

def fix_sun(sun_df):
    for col in ['Sun.M', 'LightRequirements.L', 'Sun.Exposure.E']:
        sun_df.loc[:,col] = sun_df.loc[:,col].str.lower()  # make everything lowercase
        sun_df.loc[:,col] = sun_df.loc[:,col].str.replace(' to ', ', ')  # replace ' to ' with ', '
        sun_df.loc[:,col] = sun_df.loc[:,col].str.split(', ')  # split on ', '


    # Create a function to combine the lists and remove any duplicates and nans
    combine_lists = lambda x: list(set([i for sublist in x.dropna().tolist() for i in sublist]))

    # Apply the function to each row
    sun_df.loc[:,'combined'] = sun_df.apply(combine_lists, axis=1)

    # Define a mapping dictionary
    sun_map = {
        'shade': 'Full Shade',
        'full shade': 'Full Shade',
        'part shade': 'Part Shade',
        'part shade ': 'Part Shade',
        'sun': 'Full Sun',
        'sun ': 'Full Sun',
        'full sun': 'Full Sun'
    }

    # Function to remap elements in the list
    def remap_suns(sun_list):
        return [sun_map[sun] for sun in sun_list]

    # Apply the function to the combined column
    sun_df.loc[:,'combined'] = sun_df.loc[:,'combined'].apply(remap_suns)

    # Remove duplicates from remapped lists
    sun_df.loc[:,'combined'] = sun_df.loc[:,'combined'].apply(lambda x: list(set(x)))

    sun_df.loc[:,'combined'] = sun_df.loc[:,'combined'].apply(lambda x: np.nan if len(x) == 0 else x)

    # Create new columns filled with zeros
    sun_df['Full Sun'] = False
    sun_df['Part Shade'] = False
    sun_df['Full Shade'] = False

    # Define a function to set the values based on the presence of each value
    def set_values(row):
        if type(row['combined']) != list:
            return row
        if 'Full Sun' in row['combined']:
            row['Full Sun'] = True
        if 'Part Shade' in row['combined']:
            row['Part Shade'] = True
        if 'Full Shade' in row['combined']:
            row['Full Shade'] = True
        return row

    # Apply the function to each row in the DataFrame
    sun_df = sun_df.apply(set_values, axis=1)
    return sun_df.iloc[:, -3:]


def fix_moisture(soil_df):
    for col in ['Moisture.M','SoilMoisture.L']:
        soil_df.loc[:,col] = soil_df.loc[:,col].str.lower()  # make everything lowercase
        soil_df.loc[:,col] = soil_df.loc[:,col].str.replace(' to ', ' , ')  # replace ' to ' with ', '
        soil_df.loc[:,col] = soil_df.loc[:,col].str.split(' , ')  # split on ', '


    # Create a function to combine the lists and remove any duplicates and nans
    combine_lists = lambda x: list(set([i for sublist in x.dropna().tolist() for i in sublist]))

    # Apply the function to each row
    soil_df.loc[:,'combined'] = soil_df.apply(combine_lists, axis=1)

    # Define a mapping dictionary
    soil_map = {
        'wet': 'Wet',
        'dry': 'Dry',
        'medium': 'Medium',
        'moist': 'Medium',
    \
    }

    # Function to remap elements in the list
    def remap_suns(sun_list):
        return [soil_map[sun] for sun in sun_list]

    # Apply the function to the combined column
    soil_df.loc[:,'combined'] = soil_df.loc[:,'combined'].apply(remap_suns)

    # Remove duplicates from remapped lists
    soil_df.loc[:,'combined'] = soil_df.loc[:,'combined'].apply(lambda x: list(set(x)))

    soil_df.loc[:,'combined'] = soil_df.loc[:,'combined'].apply(lambda x: np.nan if len(x) == 0 else x)

    # Create new columns filled with zeros
    soil_df['Wet'] = False
    soil_df['Medium'] = False
    soil_df['Dry'] = False


    # Define a function to set the values based on the presence of each value
    def set_values(row):
        if type(row['combined']) != list:
            return row
        if 'Wet' in row['combined']:
            row['Wet'] = True
        if 'Medium' in row['combined']:
            row['Medium'] = True
        if 'Dry' in row['combined']:
            row['Dry'] = True

        return row

    # Apply the function to each row in the DataFrame
    soil_df = soil_df.apply(set_values, axis=1)
    return soil_df.iloc[:, -3:]

def explode_col(df,col):
    new_df = df[['Accepted_SPNAME', col]]
    new_df.loc[:,col] = new_df.loc[:,col].str.replace(' , ',', ')
    new_df.loc[:,col] = new_df.loc[:,col].str.split(', ')
    new_df = new_df.explode(col)
    return new_df