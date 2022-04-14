
# Gets the row index for a given list of rown names
def get_rowindex(sheet, num_rows, rownames):
    rownames_index = []
    for n in range(num_rows):
        for r in range(len(rownames)):
            if sheet.cell_value(n,0) == rownames[r]:
                rownames_index.append(n)
    return rownames_index

# Gets the row names and indices between a start and end string
def get_rownameindex(sheet, num_rows, start_st, end_str):
    rownames = []
    rownames_index = []
    for n in range(num_rows):
        if sheet.cell_value(n,0) == start_st:
            startindex = n+1
        if sheet.cell_value(n,0) == end_str:
            endindex = n
    for n in range(startindex,endindex):
        rownames.append(sheet.cell_value(n,0))
        rownames_index.append(n)
    return rownames, rownames_index