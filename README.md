# Superpy_Assignment

A large supermarket chain has asked you to write a command-line tool that is able to keep track of their inventory: they want to call it SuperPy. 

The core functionality is about keeping track and producing reports on various kinds of data:

Which products the supermarket offers;
How many of each type of product the supermarket holds currently;
How much each product was bought for, and what its expiry date is;
How much each product was sold for or if it expired, the fact that it did.
All data must be saved in CSV files. Feel free to come up with your own file structure, but here's an example structure to get started with if you want:

File name	Columns
bought.csv	id,product_name,buy_date,buy_price,expiration_date
sold.csv	id,bought_id,sell_date,sell_price
In this example structure, the id column is an integer that is incremented for each line. This allows for some clever matching of items between different tables. You will later see this pattern a lot in databases, where it is particularly powerful. 

✏️ Note
Your program should have an internal conception of what day it is - perhaps saved to a simple text file - so that you can advance time by two days by using a command like:



👉     $ python super.py --advance-time 2



You might be asking yourself: why should I be able to time travel with my application?
Here's why: simulating time can be of great value when testing and simulating certain situations in your application. And, besides... who wouldn't want to build a time machine?😀

Interaction with your program must go through the command line. 

Here's an example of what a sequence of interactions could look like:

$ python super.py buy --product-name orange --price 0.8 --expiration-date 2020-01-01
OK

$ python super.py report inventory --now
+--------------+-------+-----------+-----------------+
| Product Name | Count | Buy Price | Expiration Date |
+==============+=======+===========+=================+
| Orange       | 1     | 0.8       | 2020-01-01      |
+--------------+-------+-----------+-----------------+

$ python super.py --advance-time 2
OK

$ python super.py report inventory --yesterday
+--------------+-------+-----------+-----------------+
| Product Name | Count | Buy Price | Expiration Date |
+==============+=======+===========+=================+
| Orange       | 1     | 0.8       | 2020-01-01      |
+--------------+-------+-----------+-----------------+

$ python super.py sell --product-name orange --price 2
OK

$ python super.py report inventory --now
+--------------+-------+-----------+-----------------+
| Product Name | Count | Buy Price | Expiration Date |
+==============+=======+===========+=================+


$ python super.py report revenue --yesterday
Yesterday's revenue: 0

$ python super.py report revenue --today
Today's revenue so far: 2

$ python super.py report revenue --date 2019-12
Revenue from December 2019: 0

$ python super.py report profit --today
1.2

$ python super.py sell --product-name orange --price 2
ERROR: Product not in stock.
Numbered divider 2
Requirements

Code

Be creative with your implementation! We intentionally keep the specification open to encourage you to be creative with this project. However, to obtain a passing grade, you will at least need to satisfy the following requirements:


Well-structured and documented code, including: 

Clear and effective variable and function names;
Use of comments where the code does not speak for itself;
Clear and effective separation of code into separate functions and possibly files.

Use of modules to the extent that it shows that you were able to independently read and understand the documentation, and apply the techniques within:

csv
argparse
datetime, including, in particular, the date object, strftime and strptime functions and datetime arithmetic using timedelta.

Use of external text files (CSV) to read and write data.


A well-structured and user-friendly command-line interface with clear descriptions of each argument in the --help section.


A text file containing a usage guide aimed at peers as the target audience. The usage guide should include plenty of examples.


The application must support: 

Setting and advancing the date that the application perceives as 'today';
Recording the buying and selling of products on certain dates;
Reporting revenue and profit over specified time periods;
Exporting selections of data to CSV files;
Two other additional non-trivial features of your choice, for example:
The use of an external module Rich(opens in a new tab) to improve the application.
The ability to import/export reports from/to formats other than CSV (in addition to CSV).
The ability to visualize some statistics using Matplotlib(opens in a new tab) .
Another feature that you thought of.
Numbered divider 3
Report


Please include a short, 300-word report that highlights three technical elements of your implementation that you find notable.


Explain what problem they solve and why you chose to implement them in this way.


Include this in your repository as a report.md file.

Our tips regarding the report:

You may consider using Markdown for your report.

Markdown is a markup language you can use for styling your plain text. It is widely used in programming, so it could be a good choice, but it is not required.
To assist your explanation you may use code snippets.
