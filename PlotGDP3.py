"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    dict_country_code_map = dict()
    set_extra_code_plot= set()

    for country in plot_countries :
        if plot_countries[country] in gdp_countries:
            dict_country_code_map[country]=plot_countries[country]
        else:
            set_extra_code_plot.add(country)

    return dict_country_code_map,set_extra_code_plot


def return_dict_csv(gdpinfo):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary

    Output:
      A dictionary which has Country names as Key & related GDP details as value
    """
    gdp_countries = {}
    key_field=gdpinfo["country_name"]

    with open(gdpinfo["gdpfile"]) as file:
        input_file=csv.DictReader(file,delimiter=gdpinfo["separator"],quotechar=gdpinfo["quote"])

        for row in input_file:
            gdp_countries[row[key_field]]=row

    return gdp_countries

def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdp_countries=return_dict_csv(gdpinfo)
    #file closed
    tup1=reconcile_countries_by_name(plot_countries,gdp_countries)
    dict_country_code_map=tup1[0]
    set_extra_code_plot=tup1[1]

    dict_code_gdp=dict()
    set_no_gdp_data=set()

    for country_code, country_name in dict_country_code_map.items():
        if country_name in gdp_countries:
            if str(year) in gdp_countries[country_name]:
                if gdp_countries[country_name][str(year)] == '':
                    set_no_gdp_data.add(country_code)
                else:
                    gdp_float=float(gdp_countries[country_name][str(year)])
                    dict_code_gdp[country_code]=math.log10(gdp_float)

    return dict_code_gdp, set_extra_code_plot, set_no_gdp_data


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    tuple1=build_map_dict_by_name(gdpinfo, plot_countries, year)

    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = 'World GDP Data for year '+str(year)
    worldmap_chart.add('Country GDP', tuple1[0])
    worldmap_chart.add('Missing Country', tuple1[1])
    worldmap_chart.add('Missing GDP', tuple1[2])

    return worldmap_chart


def test_render_world_map(input_year):
    """
    Test the project code for several years.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    #render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    #1980
    #render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    #2000
    #render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    #2010
    worldmap_chart = render_world_map(gdpinfo, pygal_countries, input_year, "isp_gdp_world_name_2010.svg")
    return worldmap_chart

# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map(2010)
