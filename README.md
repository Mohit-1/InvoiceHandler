## Invoice_handler

Automatically extract relevant data from invoices by processing their .pdf/.xml files.

#### Pre-requisites - 
1. MySQL
2. Python 3

#### How to run it - 

1. Clone the repository.
2. Install the dependencies from the requirements.txt file.
3. Create a new MySQL database. (Credentials- database name = kredX, user = kredx, password = kredx, host = localhost)
4. Run the handler.py script from the command line. 
   eg - ```python3 /path/to/handler.py```
   The script asks the user to input the path for the XML file which is to be processeed and shows the result.
