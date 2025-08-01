# Simple Python Database

This project implements a simple in-memory database system using Python. It supports basic SQL-like operations such as CREATE, INSERT, SELECT, UPDATE, DELETE, COUNT, and JOIN via command-line input.

## Features

- Create new tables (`CREATE_TABLE`)
- Insert rows into tables (`INSERT`)
- Select rows with conditions (`SELECT`)
- Update rows with conditions (`UPDATE`)
- Delete rows or entire tables (`DELETE`)
- Count rows that match conditions (`COUNT`)
- Join two tables on a common column (`JOIN`)

## Usage

### Run the script

```bash
python <script_name>.py <commands_file>.txt
```

Example:

```bash
python simple_database.py commands.txt
```

### Command syntax

Write your commands in a text file with the following formats:

```
CREATE_TABLE <table_name> <column1,column2,...>
INSERT <table_name> <value1,value2,...>
SELECT <table_name> <column1,column2,...> WHERE {"column":"value",...}
UPDATE <table_name> {"column":"new_value",...} WHERE {"column":"value",...}
DELETE <table_name> WHERE {"column":"value",...}
DELETE <table_name> WHERE *
COUNT <table_name> WHERE {"column":"value",...}
COUNT <table_name> WHERE *
JOIN <table1>,<table2> ON <common_column>
```

### Example

```
CREATE_TABLE Students Name,Age,Grade
INSERT Students Alice,20,A
INSERT Students Bob,21,B
SELECT Students Name,Age WHERE {"Grade":"A"}
UPDATE Students {"Grade":"B"} WHERE {"Name":"Alice"}
DELETE Students WHERE {"Name":"Bob"}
COUNT Students WHERE *
JOIN Students,Courses ON StudentID
```

### Help

You can add `/help` to your commands file to print available commands.

## Notes

- The database only exists in memory while the script runs.
- Data is not saved to disk automatically.
- Make sure to provide the correct input file name.

## Author

*Your Name Here*

