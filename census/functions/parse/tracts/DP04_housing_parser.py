def DP04_parse_housing(sheet, num_cols, num_rows, location_id, index_estimate):
    import pandas as pd

    dfs = []
    ### DEFINE MAIN FUNCTION
    def house_characteristics(start_rowname, end_rowname, characteristic, dfs,subtract='',to_end=''):
        start_rowindex = [n for n in range(num_rows) if sheet.cell_value(n, 0) == start_rowname]
        end_rowindex = [n for n in range(num_rows) if sheet.cell_value(n, 0) == end_rowname]
        if subtract:
            rownames_index = list(range(start_rowindex[0] + 2, end_rowindex[0]-subtract))
        else:
            rownames_index = list(range(start_rowindex[0]+2, end_rowindex[0]))
        if to_end:
            rownames_index = list(range(start_rowindex[0] + 2, num_rows-1))
        dict = {'location_id': [], characteristic: [], 'houses': []}
        for x in range(len(location_id)):
            for c in range(len(rownames_index)):
                dict['location_id'].append(location_id[x])

                dict[characteristic].append(sheet.cell_value(rownames_index[c], 0))
                dict['houses'].append(int(sheet.cell_value(rownames_index[c], index_estimate[x]).replace(',', '')))
        dfs = dfs.append(pd.DataFrame(dict,columns=['location_id',characteristic, 'houses']))

    # housing occupancy
    house_characteristics('HOUSING OCCUPANCY', 'Homeowner vacancy rate', 'housing_occupancy',dfs)

    # units in structure
    house_characteristics('UNITS IN STRUCTURE', 'YEAR STRUCTURE BUILT', 'units_in_structure',dfs)

    # year structure built
    house_characteristics('YEAR STRUCTURE BUILT', 'ROOMS', 'year_built', dfs)

    # rooms
    house_characteristics('ROOMS', 'Median rooms', 'rooms', dfs)

    # bedrooms
    house_characteristics('BEDROOMS', 'HOUSING TENURE', 'bedrooms', dfs)

    # housing tenure
    house_characteristics('HOUSING TENURE', 'Average household size of owner-occupied unit', 'housing_tenure', dfs)

    # year householder moved into unit
    house_characteristics('YEAR HOUSEHOLDER MOVED INTO UNIT', 'VEHICLES AVAILABLE', 'year_moved_in', dfs)

    # vehicles available
    house_characteristics('VEHICLES AVAILABLE', 'HOUSE HEATING FUEL', 'vehicles_available', dfs)

    # house heating fuel
    house_characteristics('HOUSE HEATING FUEL', 'SELECTED CHARACTERISTICS', 'heating_fuel', dfs)

    # selected characteristics
    house_characteristics('SELECTED CHARACTERISTICS', 'OCCUPANTS PER ROOM', 'characteristic', dfs)

    # occupants per room
    house_characteristics('OCCUPANTS PER ROOM', 'VALUE', 'occupants_per_room', dfs)

    # value
    house_characteristics('VALUE', 'MORTGAGE STATUS', 'value', dfs, subtract=1)

    # mortgage status
    house_characteristics('MORTGAGE STATUS', 'SELECTED MONTHLY OWNER COSTS (SMOC)', 'mortgage_status', dfs)

    # gross rent
    house_characteristics('GROSS RENT', 'GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)', 'rent', dfs, subtract=2)

    # gross rent as a percentage of income
    house_characteristics('GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)', 'Not computed', 'rent_%income',dfs,to_end='yes')

    ### CREATE OUTPUT FILE
    excel_name, sheetnames = 'DP04_parsed.xlsx', ['HousingOccupancy','UnitsInStructure','YearStructureBuilt','Rooms',
                                                  'Bedrooms','HousingTenure','YearMovedIn','VehiclesAvailable',
                                                  'HeatingFuel','SelectedCharacteristics','OccupantsPerRoom','HousingValue',
                                                  'MortageStatus','GrossRent','GrossRent_%Income']
    return dfs, excel_name, sheetnames