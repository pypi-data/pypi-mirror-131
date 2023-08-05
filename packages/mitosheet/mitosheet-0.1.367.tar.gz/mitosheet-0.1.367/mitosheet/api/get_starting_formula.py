from mitosheet.utils import df_to_json_dumpsable

def get_starting_formula(event, steps_manager) -> str:
    """
    Returns the formula/value of the cell. If the (row_index, column_id) is not a cell 
    (ie: it is a column header), returns ''.

    We have this function becase the actionSearchBar needs to get a value at a specific cell, but
    doesn't have access to the startingRowIndex, which means it can't access the data through the
    sheetDataArray correctly. To avoid complicating the state management, we just use this API call :) 

    Params:
    -   sheet_index: number - the sheet to load
    -   row_index: number - the row number of the cell 
    -   column_id: str - the id of the column to get the data of
    """
    sheet_index = event['sheet_index']
    row_index = event['row_index']
    column_id = event['column_id']

    if sheet_index >= len(steps_manager.curr_step.dfs):
        return ''

    df = steps_manager.curr_step.dfs[sheet_index]
    column_spreadsheet_code = steps_manager.curr_step.post_state.column_spreadsheet_code[sheet_index][column_id]
    
    # If the column is a formula column, return the formula, otherwise return the value as a string
    return column_spreadsheet_code if column_spreadsheet_code != '' else str(df[column_id].at[row_index])


    