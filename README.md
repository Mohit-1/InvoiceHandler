## Invoice_handler

Automatically extract relevant data from invoices by processing their .pdf/.xml files.

#### Pre-requisites - 
1. MySQL
2. Python 3
3. Install the Python and MySQL development headers and libraries-

   ```sudo apt-get install python-dev libmysqlclient-dev```
   
   and 
   
   ```sudo apt-get install python3-dev```
   
4. Install mysqlclient- 
```pip3 install mysqlclient```   

#### How to run it - 

1. Clone the repository.
2. Create a new MySQL database and a user. (Credentials- database name = kredX, user = kredx, password = kredx, host = localhost)
3. Run the handler.py script from the command line. 
   eg - ```python3 /path/to/handler.py```
   The script asks the user to input the path for the XML file which is to be processeed and shows the result.
