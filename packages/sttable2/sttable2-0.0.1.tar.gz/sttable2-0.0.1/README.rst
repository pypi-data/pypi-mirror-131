~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Welcome to sttable2's documentation!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Parser of string representation tables, input example::

      header_1st_col   | header_2nd_col   |\n
      row_1_of_1st_col | row_1_of_2nd_col |\n
      row_2_of_1st_col | row_2_of_2nd_col |


Parsed information can be accessed by rows::

    [{'header_1st_col': 'row_1_of_1st_col', 'header_2nd_col': 'row_1_of_2nd_col'},
     {'header_1st_col': 'row_2_of_1st_col', 'header_2nd_col': 'row_2_of_2nd_col'}]

As well as by columns::

    {'header_1st_col': ['row_1_of_1st_col', 'row_2_of_1st_col'],
      header_2nd_col': ['row_1_of_2nd_col', 'row_2_of_2nd_col']}

Fields::

    ['header_1st_col', 'header_2nd_col', 'header_3rd_col']


======================================================================================

Also support Parser of multi-lines string representation tables, input example::

      | INSERT INTO `CustomTable` (`column1`, `column2`, `column3`)
        VALUES
        ('value11', 'value12', 'value13'),
        ('value21', 'value22', 'value23'),
        ('value31', 'value32', 'value33');           |

