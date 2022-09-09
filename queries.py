QUERY_SELECT_ACTIVITY_NAMES = 'SELECT DISTINCT `Activity Name` FROM dataset ORDER BY 1'

def QUERY_SELECT_ACTIVITY_FREQUENCY(activities: list) -> str:
    if len(activities) == 0:
        where_clause = ''
    else:
        where_clause = 'WHERE `Activity Name` = \'{}\''.format(activities[0])
        for activity in activities[1:]:
            where_clause += ' OR `Activity Name` = \'{}\''.format(activity)     # Note the space at line start!

    return '''
        SELECT
            Name,
            Surname,
            COUNT(*) as Attendance,
            DENSE_RANK() OVER(ORDER BY COUNT(*) DESC) as Rank
        FROM
            dataset
        {where_clause}
        GROUP BY
            Name, Surname
        ORDER BY
            Attendance DESC, Surname, Name

    '''.format(where_clause=where_clause)