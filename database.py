from sys import argv

# Creates a new table with specified columns if it doesn't already exist
def table_create(all_tables, table_name, columns):
    # Check if table hadn't created before.
    if table_name in all_tables:
        print("Table already exists")
        return
    else:
        print("###################### CREATE #########################")
        # Create table in database and create column and data parts.
        all_tables[table_name] = {
            "columns": columns,
            "data": [] }
        print(f"Table '{table_name}' created with columns: {columns}")
        print("#######################################################")
        return

# Displays the structure and data of a specific table in a formatted view
def table_vis(all_tables, table_name):
    print(f"\nTable: {table_name}")
    columns = all_tables[table_name]["columns"]
    rows = all_tables[table_name]["data"]

    # Calculate column widths for proper formatting
    col_widths = []
    for i, col in enumerate(columns):
        max_width = len(str(col))
        for row in rows:
            cell_length = len(str(row[i]))
            max_width = max(max_width, cell_length)
        col_widths.append(max_width)

    # Create the header of the table
    header = "+"
    for m in col_widths:
        header += "-" * (m + 2) + "+"
    header_line = "| "
    for i in range(len(columns)):
        header_line += f"{columns[i]}".ljust(col_widths[i])
        if i < len(columns) - 1:
            header_line += " | "
    header_line += " |"

    # Print the header and rows
    print(header)
    print(header_line)
    print(header)
    for row in rows:
        row_line = "| "
        for i in range(len(row)):
            row_line += f"{row[i]}".ljust(col_widths[i])
            if i < len(row) - 1:
                row_line += " | "
        row_line += " |"
        print(row_line)
    print(header)
    print("#######################################################")

# Inserts data into a specific table
def table_insert(all_tables, table_name, data):
    print("###################### INSERT #########################")
    try:
        all_tables[table_name]["data"].append(data)
        print(f"Inserted into '{table_name}': {tuple(data)}")
        return table_vis(all_tables, table_name)
    # Check if table exists
    except KeyError:
        print(f"Table {table_name} not found")
        print(f"Inserted into '{table_name}': {tuple(data)}")
        print("#######################################################")

# Selects rows from a table based on specified conditions and columns
def table_select(all_tables, table_name, columns, conditions):
    print("###################### SELECT #########################")
    try:
        all_columns = all_tables[table_name]["columns"]

        # Validate conditions and columns
        for key, value in conditions.items():
            if key not in all_columns:
                print(f"Column {key} does not exist")
                print(f"Condition: {conditions}")
                print(f"Select result {'from'} '{table_name}': None")
                print("#######################################################")
                return
        # If no columns are specified, select all columns.
        if columns == ["*"]:
            columns = all_columns
        else:
            for col in columns:
                if col not in all_columns:
                    print(f"Column {col} does not exist")
                    print(f"Condition: {conditions}")
                    print(f"Select result {'from'} '{table_name}': None")
                    print("#######################################################")
                    return

        # Filter rows based on conditions
        selected_rows = []
        rows = all_tables[table_name]["data"]
        for row in rows:
            for key, value in conditions.items():
                col_index = all_columns.index(key)
                if row[col_index] != value:
                    if row in selected_rows:
                        selected_rows.remove(row)
                    break
                if row not in selected_rows:
                    selected_rows.append(row)

        # Extract selected columns
        select_result = []
        for row in selected_rows:
            row_data = []
            for col in columns:
                col_index_b = all_columns.index(col)
                row_data.append(row[col_index_b])
            select_result.append(tuple(row_data))

        print(f"Condition: {conditions}")
        print(f"Select result {'from'} '{table_name}': {select_result}")
        print("#######################################################")
    # Check if table exists
    except KeyError:
        print(f"Table {table_name} not found")
        print(f"Condition: {conditions}")
        print(f"Select result {'from'} '{table_name}': None")
        print("#######################################################")

# Updates rows in a table based on specified conditions
def table_update(all_tables, table_name, updates, conditions):
    print("###################### UPDATE #########################")
    print(f"Updated '{table_name}' with {updates} where {conditions}")
    try:
        all_columns = all_tables[table_name]["columns"]
        updated_rows_num = 0
        # Select rows with conditions
        for row in all_tables[table_name]["data"]:
            match = True
            for update_key, update_value in updates.items():
                if update_key not in all_columns:
                    print(f"Column {update_key} does not exist")
                    print("0 rows updated.")
                    return table_vis(all_tables, table_name)
            for cond_key, cond_value in conditions.items():
                if cond_key not in all_columns:
                    print(f"Column {cond_key} does not exist")
                    print("0 rows updated.")
                    return table_vis(all_tables, table_name)
            for cond_key, cond_value in conditions.items():
                col_index = all_columns.index(cond_key)
                # Search until no match
                if row[col_index] != cond_value:
                    match = False
                    break
            # Select matched rows
            if match:
                for update_key, update_value in updates.items():
                    col_index_b = all_columns.index(update_key)
                    row[col_index_b] = update_value
                updated_rows_num += 1

        print(f"{updated_rows_num} rows updated.")
        table_vis(all_tables, table_name)
    # Check if table exists
    except KeyError:
        print(f"Table {table_name} not found")
        print("0 rows updated.")
        print("#######################################################")

# Delete rows from a table based on specified conditions
def table_delete(all_tables, table_name, conditions):
    print("###################### DELETE #########################")
    if conditions != "*":
        # Convert condition if it is integer
        converted_conditions = {}
        for key, value in conditions.items():
            if isinstance(value, str) and value.isdigit():
                converted_conditions[key] = int(value)
            else:
                converted_conditions[key] = value
        print(f"Deleted from '{table_name}' where {converted_conditions}")
    try:
        # If no conditions are specified, select all rows.
        if conditions == "*":

            del all_tables[table_name]
            print(f"Table '{table_name}' deleted.")
            print(f"All rows deleted.")
            print("#######################################################")
            return
        else:
            # Select and delete specified rows in table.
            all_columns = all_tables[table_name]["columns"]
            deleted_rows_num = 0
            for cond_key, cond_value in conditions.items():
                if cond_key not in all_columns:
                    print(f"Column {list(conditions.keys())[0]} does not exist")
                    print("0 rows deleted.")
                    table_vis(all_tables, table_name)
                    return

            for row in all_tables[table_name]["data"]:
                match = True
                for cond_key, cond_value in conditions.items():
                    col_index = all_columns.index(cond_key)
                    if row[col_index] != cond_value:
                        match = False
                        break
                if match:
                    all_tables[table_name]["data"].remove(row)
                    deleted_rows_num += 1

            print(f"{deleted_rows_num} rows deleted.")
            table_vis(all_tables, table_name)
    # Check if table exists
    except KeyError:
        print(f"Table {table_name} not found")
        print("0 rows deleted.")
        print("#######################################################")

# Counts rows in a table that meet specified conditions
def table_count(all_tables, table_name, conditions):
    print("###################### COUNT #########################")
    try:
        all_columns = all_tables[table_name]["columns"]
        if conditions == "*" :
            count_num = len(all_tables[table_name]["data"])
        else:
            count_num = 0
            for cond_key, cond_value in conditions.items():
                if cond_key not in all_columns:
                    print(f"Column {cond_key} does not exist")
                    print(f"Total number of entries in '{table_name}' is 0")
                    print("#######################################################")
                    return
            for row in all_tables[table_name]["data"]:
                match = True
                for cond_key, cond_value in conditions.items():
                    col_index = all_columns.index(cond_key)
                    if row[col_index] != cond_value:
                        match = False
                        break
                if match:
                    count_num += 1

        print(f"Count: {count_num}")
        print(f"Total number of entries in '{table_name}' is {count_num}")
        print("#######################################################")
    # Check if table exists
    except KeyError:
        print(f"Table {table_name} not found")
        print(f"Total number of entries in '{table_name}' is 0")
        print("#######################################################")

# Joins two tables based on a common column and creates a new joined table
def table_join(all_tables, table1, table2, common_column):
    print("####################### JOIN ##########################")
    print(f"Join tables {table1} and {table2}")
    try:
    # Check tables in database
        if table1 not in all_tables:
            print(f"Table {table1} does not exist")
            print("#######################################################")
            return
        if table2 not in all_tables:
            print(f"Table {table2} does not exist")
            print("#######################################################")
            return
        table1_columns = all_tables[table1]["columns"]
        table2_columns = all_tables[table2]["columns"]
        table1_data = all_tables[table1]["data"]
        table2_data = all_tables[table2]["data"]

        # Get column indexes for join
        col1_index = table1_columns.index(common_column)
        col2_index = table2_columns.index(common_column)

        # Combine columns and data for join
        joined_columns = table1_columns + table2_columns
        joined_data = []
        for row1 in table1_data:
            for row2 in table2_data:
                if row1[col1_index] == row2[col2_index]:
                    joined_row = row1 + row2
                    joined_data.append(joined_row)

        # Store the result as a new table
        all_tables['Joined Table'] = {"data": joined_data, "columns": joined_columns}
        row_num = len(all_tables['Joined Table']["data"])
        print(f"Join result ({row_num} rows):")
        table_vis(all_tables, 'Joined Table')
    except ValueError:
        print(f"Column {common_column} does not exist")
        print("#######################################################")

# Call the appropriate table function based on the input command
def func_caller(all_tables, line):
    func = line.strip().split()[0]
    table_name = line.strip().split()[1]

    if func == "CREATE_TABLE":
        line_separated = line.strip().split()
        columns = line_separated[2].split(",")
        return table_create(all_tables, table_name, columns)

    if func == "INSERT":
        data_parts = line.strip().split(' ', 2)
        data = data_parts[2].split(',')
        return table_insert(all_tables, table_name, data)

    if func == "SELECT":
        line_separated = line.strip().split(' ')
        columns = line_separated[2].split(",")
        condition_str = line.split('WHERE', 1)[1].strip().replace("{", "").replace("}", "")
        conditions = {}
        for condition in condition_str.split(','):
            key, value = condition.split(':')
            conditions[key.strip().replace('"', '')] = value.strip().replace('"', '')
        return table_select(all_tables, table_name, columns, conditions)

    if func == "UPDATE":
        line_separated = line.split('WHERE', 1)
        update_str = line_separated[0].split(' ', 2)[2].strip().strip('{}')
        updates = {}
        for update in update_str.split(','):
            key, value = update.split(':')
            updates[key.replace('"', "").replace(" ", "")] = value.replace('"', "").replace(" ", "")

        condition_str = line_separated[1].strip().strip('{}')
        conditions = {}
        for condition in condition_str.split(','):
            key, value = condition.split(':')
            conditions[key.replace('"', "").strip()] = value.replace('"', "").strip()
        return table_update(all_tables, table_name, updates, conditions)

    if func == "DELETE":
        if len(line.split()) == 2:
            return table_delete(all_tables, table_name, "*")
        elif line.split()[2] == 'WHERE':
            line_separated = line.split('WHERE', 1)
            condition_str = line_separated[1].replace("{", "").replace("}", "").replace(' ', '')
            if condition_str == "*":
                return table_delete(all_tables, table_name, "*")
            conditions = {}
            for condition in condition_str.split(','):
                key, value = condition.split(':')
                conditions[key.replace('"', "").strip()] = value.replace('"', "").strip()
            return table_delete(all_tables, table_name, conditions)

    if func == "COUNT":
        line_separated = line.split('WHERE', 1)
        condition_str = line_separated[1].replace("{", "").replace("}", "").replace(' ', '')
        if condition_str == "*":
            return table_count(all_tables, table_name, "*")
        conditions = {}
        for condition in condition_str.split(','):
            key, value = condition.split(':')
            conditions[key.replace('"', "").strip()] = value.replace('"', "").strip()
        return table_count(all_tables, table_name, conditions)

    if func == "JOIN":
        line_separated = line.split()
        table1, table2 = line_separated[1].split(',')
        common_column = line_separated[3]
        return table_join(all_tables, table1, table2, common_column)

# Main function to process input commands from a file
def main():
    try:
        input_file = open(argv[1], 'r')
# Check user command right
    except IndexError:
        print("You didn't command input file")
    except IOError:
        print("Input file cannot be opened")
    else:
        all_tables = {}
        all_functions = ("CREATE_TABLE", "INSERT", "SELECT", "UPDATE", "DELETE", "COUNT", "JOIN")
        for line in input_file.readlines():
            line = line.replace("\n", "")
            if not line.strip():     # Pass empty lines
                continue
            # Print command list if user writes help
            elif "/help" in line:
                print("CREATE_TABLE <table_name> <columns>\nINSERT <table_name> <data>\nSELECT <table_name> <columns> WHERE <conditions>\nUPDATE <table_name> <updates> WHERE <conditions>\nDELETE <table_name> WHERE <conditions>\nJOIN <table1>,<table2> ON <column>\nCOUNT <table_name> WHERE <conditions>")
            elif line.split(' ')[0] in all_functions:
                try:
                    func_caller(all_tables,line)
                except IndexError:
                    print("You didn't provide a valid function. Write /help for command list.")
                except ValueError:
                    print("You didn't provide a valid function. Write /help for command list.")
                else:
                    print()
            else:
                continue
        input_file.close()

if __name__ == '__main__':
    main()
