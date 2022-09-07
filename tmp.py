import sql_query
import sys

if __name__ == '__main__':
    ds = sql_query.read_file(sys.argv[1])
    res =  sql_query.execute_query(ds, 'SELECT DISTINCT `Activity Name` FROM dataset ORDER BY 1')
    
    print(res)