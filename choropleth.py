from os.path import abspath
import webbrowser
import pandas as pd
import holoviews as hv
from holoviews import opts

hv.extension('bokeh')  # specify bokeh as holoview backend extension
from bokeh.sampledata.us_counties import data as counties  # import us counties map data

df = pd.read_csv('census_data_popl_2010.csv', encoding="ISO-8859-1")  # use pandas to read the population data

df = pd.DataFrame(df, columns=['Target Geo Id2', 'Geographic area.1',
                               'Density per square mile of land area - Population'])  # pick columns from data frame

df.rename(columns={'Target Geo Id2': 'fips',
                   'Geographic area.1': 'County',
                   'Density per square mile of land area - Population': 'Density'},
          inplace=True)  # rename columns in data frame

print(f"Initial popl data:\n {df.head()}")  # print dataframe headers
print(f"Shape of df = {df.shape}\n")  # print size of dataframe

df = df[df['fips'] > 100]  # create new data frame without rows with fip scores less than 100
print(f"Popl data with non county rows removed:\n {df.head()}")  # print new frame preview
print(f"Shape of df = {df.shape}\n")  # print shape of df

df['state_id'] = (df['fips'] // 1000).astype('int64')  # divide fips by 1000 to get state id number
df['cid'] = (df['fips'] % 1000).astype('int64')  # get county id from fips number
print(f"Popl data with new ID columns:\n {df.head()}")  # print frame again
print(f"Shape of df = {df.shape}\n")  # print shape again
print("df Info:")
print(df.info())

print("\nPopl data at row 500:")
print(df.loc[500])

state_ids = df.state_id.tolist()  # create list of state_ids from dataframe
cids = df.cid.tolist()  # create list of county ids from data frame
den = df.Density.tolist()  # create list of population density entries from data frame

tuple_list = tuple(zip(state_ids, cids))  # create list of tuples from state ids and county ids
popl_dens_dict = dict(zip(tuple_list, den))  # create population density dictionary from state and county tuple as key
# and population density as value

EXCLUDED = ('ak', 'hi', 'pr', 'gu', 'vi', 'mp', 'as')  # constant of excluded territories

counties = [dict(county, Density=popl_dens_dict[cid])
            for cid, county in counties.items()
            if county["state"] not in EXCLUDED]  # create list of  dictionaries with county key and population density value
# for each county id and county in counties if not in list of excluded places

choropleth = hv.Polygons(counties, ['lons', 'lats'], [('detailed name', 'County'), 'Density'])
# create instance of choropleth map with counties list, and hover stats

choropleth.opts(opts.Polygons(logz=True, tools=['hover'], xaxis=None, yaxis=None, show_grid=False, show_frame=False,
                              width=1100, height=700, colorbar=True, toolbar='above', color_index='Density',
                              cmap='Greys', line_color=None,
                              title='2010 Population Density per Square Mile of Land Area'))  # set choropleth options

hv.save(choropleth, 'choropleth.html', backend='bokeh')  # save choropleth to html file
url = abspath('choropleth.html')  # create url for choropleth
webbrowser.open(url)  # open webbrowser to choropleth map
