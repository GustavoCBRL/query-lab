from django.core.management.base import BaseCommand
from study_hub.models import Topics, Questions, Choices, PracticeExercise

TOPICS = [
    {
        "title": "SELECT",
        "slug": "select",
        "summary": "Retrieve data from database tables.",
        "theory": """
The SELECT statement is used to retrieve data from one or more tables.

Basic syntax:

SELECT column_name
FROM table_name;

Examples:

SELECT name
FROM customers;

SELECT *
FROM customers;
"""
    },
    {
        "title": "WHERE",
        "slug": "where",
        "summary": "Filter records using specific conditions.",
        "theory": """
The WHERE clause is used to filter records returned by a query.

Common operators:

=
!=
>
<
>=
<=

Example:

SELECT *
FROM customers
WHERE city = 'New York';
"""
    },
    {
        "title": "ORDER BY",
        "slug": "order-by",
        "summary": "Sort query results in ascending or descending order.",
        "theory": """
The ORDER BY clause sorts the result set.

ASC = Ascending order
DESC = Descending order

Example:

SELECT name, salary
FROM employees
ORDER BY salary DESC;
"""
    },
    {
        "title": "DISTINCT",
        "slug": "distinct",
        "summary": "Return unique values only.",
        "theory": """
DISTINCT removes duplicate values from query results.

Example:

SELECT DISTINCT country
FROM customers;
"""
    },
    {
        "title": "LIMIT",
        "slug": "limit",
        "summary": "Restrict the number of rows returned.",
        "theory": """
LIMIT is used to specify the maximum number of records returned.

Example:

SELECT *
FROM products
LIMIT 10;
"""
    },
    {
        "title": "GROUP BY",
        "slug": "group-by",
        "summary": "Group rows for aggregate calculations.",
        "theory": """
GROUP BY combines rows with the same values.

Often used with:

COUNT()
SUM()
AVG()
MIN()
MAX()

Example:

SELECT department,
       COUNT(*)
FROM employees
GROUP BY department;
"""
    },
    {
        "title": "HAVING",
        "slug": "having",
        "summary": "Filter grouped results.",
        "theory": """
HAVING filters groups after GROUP BY.

Example:

SELECT department,
       COUNT(*)
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;
"""
    },
    {
        "title": "INNER JOIN",
        "slug": "inner-join",
        "summary": "Return matching records from related tables.",
        "theory": """
INNER JOIN returns rows that have matching values in both tables.

Example:

SELECT customers.name,
       orders.id
FROM customers
INNER JOIN orders
ON customers.id = orders.customer_id;
"""
    },
    {
        "title": "LEFT JOIN",
        "slug": "left-join",
        "summary": "Return all rows from the left table and matching rows from the right table.",
        "theory": """
LEFT JOIN returns every row from the left table.

If no match exists, NULL values are returned.

Example:

SELECT customers.name,
       orders.id
FROM customers
LEFT JOIN orders
ON customers.id = orders.customer_id;
"""
    },
    {
        "title": "RIGHT JOIN",
        "slug": "right-join",
        "summary": "Return all rows from the right table and matching rows from the left table.",
        "theory": """
RIGHT JOIN returns every row from the right table.

Example:

SELECT customers.name,
       orders.id
FROM customers
RIGHT JOIN orders
ON customers.id = orders.customer_id;
"""
    },
    {
        "title": "UNION",
        "slug": "union",
        "summary": "Combine results from multiple queries.",
        "theory": """
UNION combines the results of two or more SELECT statements.

Example:

SELECT city FROM customers
UNION
SELECT city FROM suppliers;
"""
    },
    {
        "title": "SUBQUERY",
        "slug": "subquery",
        "summary": "Use a query inside another query.",
        "theory": """
A subquery is a query nested within another SQL statement.

Example:

SELECT name
FROM employees
WHERE salary >
(
    SELECT AVG(salary)
    FROM employees
);
"""
    },
    {
        "title": "INSERT",
        "slug": "insert",
        "summary": "Add new records to a table.",
        "theory": """
INSERT is used to add data into a table.

Example:

INSERT INTO customers
(name, city)
VALUES
('John', 'Chicago');
"""
    },
    {
        "title": "UPDATE",
        "slug": "update",
        "summary": "Modify existing records.",
        "theory": """
UPDATE changes existing data.

Example:

UPDATE customers
SET city = 'Boston'
WHERE id = 1;
"""
    },
    {
        "title": "DELETE",
        "slug": "delete",
        "summary": "Remove records from a table.",
        "theory": """
DELETE removes rows from a table.

Example:

DELETE FROM customers
WHERE id = 1;
"""
    }
]

QUESTIONS = [
    {
        "topic": "select",
        "statement": "Which SQL statement is used to retrieve data from a table?",
        "explanation": "SELECT is the SQL command used to retrieve data from one or more tables.",
        "choices": [
            ("SELECT", True),
            ("INSERT", False),
            ("UPDATE", False),
            ("DELETE", False),
        ]
    },

    {
        "topic": "where",
        "statement": "Which clause is used to filter rows returned by a query?",
        "explanation": "The WHERE clause filters records according to a specified condition.",
        "choices": [
            ("WHERE", True),
            ("ORDER BY", False),
            ("GROUP BY", False),
            ("HAVING", False),
        ]
    },

    {
        "topic": "order-by",
        "statement": "Which clause is used to sort query results?",
        "explanation": "ORDER BY sorts rows in ascending or descending order.",
        "choices": [
            ("ORDER BY", True),
            ("WHERE", False),
            ("GROUP BY", False),
            ("JOIN", False),
        ]
    },

    {
        "topic": "distinct",
        "statement": "What is the purpose of the DISTINCT keyword?",
        "explanation": "DISTINCT removes duplicate values from the result set.",
        "choices": [
            ("Remove duplicate rows", True),
            ("Sort results", False),
            ("Update records", False),
            ("Delete records", False),
        ]
    },

    {
        "topic": "limit",
        "statement": "What does the LIMIT clause do?",
        "explanation": "LIMIT restricts the number of rows returned by a query.",
        "choices": [
            ("Restricts the number of returned rows", True),
            ("Sorts the results", False),
            ("Filters rows", False),
            ("Groups rows", False),
        ]
    },

    {
        "topic": "group-by",
        "statement": "Which clause groups rows with the same values?",
        "explanation": "GROUP BY groups records to perform aggregate calculations.",
        "choices": [
            ("GROUP BY", True),
            ("ORDER BY", False),
            ("HAVING", False),
            ("WHERE", False),
        ]
    },

    {
        "topic": "having",
        "statement": "Which clause filters grouped results after GROUP BY?",
        "explanation": "HAVING is used to filter groups created by GROUP BY.",
        "choices": [
            ("HAVING", True),
            ("WHERE", False),
            ("LIMIT", False),
            ("DISTINCT", False),
        ]
    },

    {
        "topic": "inner-join",
        "statement": "What does an INNER JOIN return?",
        "explanation": "INNER JOIN returns only rows with matching values in both tables.",
        "choices": [
            ("Matching rows from both tables", True),
            ("All rows from the left table", False),
            ("All rows from the right table", False),
            ("All rows from both tables", False),
        ]
    },

    {
        "topic": "left-join",
        "statement": "What does a LEFT JOIN return?",
        "explanation": "LEFT JOIN returns all rows from the left table and matching rows from the right table.",
        "choices": [
            ("All rows from the left table and matching rows from the right table", True),
            ("Only matching rows", False),
            ("All rows from the right table", False),
            ("No matching rows", False),
        ]
    },

    {
        "topic": "right-join",
        "statement": "What does a RIGHT JOIN return?",
        "explanation": "RIGHT JOIN returns all rows from the right table and matching rows from the left table.",
        "choices": [
            ("All rows from the right table and matching rows from the left table", True),
            ("Only matching rows", False),
            ("All rows from the left table", False),
            ("No matching rows", False),
        ]
    },

    {
        "topic": "union",
        "statement": "What is the purpose of the UNION operator?",
        "explanation": "UNION combines the results of two or more SELECT statements.",
        "choices": [
            ("Combine results from multiple SELECT statements", True),
            ("Join two tables", False),
            ("Filter rows", False),
            ("Sort results", False),
        ]
    },

    {
        "topic": "subquery",
        "statement": "What is a subquery?",
        "explanation": "A subquery is a query nested inside another SQL statement.",
        "choices": [
            ("A query inside another query", True),
            ("A type of JOIN", False),
            ("A database table", False),
            ("A sorting operation", False),
        ]
    },

    {
        "topic": "insert",
        "statement": "Which SQL statement is used to add new records to a table?",
        "explanation": "INSERT is used to add new rows to a table.",
        "choices": [
            ("INSERT", True),
            ("UPDATE", False),
            ("DELETE", False),
            ("SELECT", False),
        ]
    },
    {
        "topic": "update",
        "statement": "Which SQL statement is used to modify existing records?",
        "explanation": "UPDATE changes data already stored in a table.",
        "choices": [
            ("UPDATE", True),
            ("INSERT", False),
            ("DELETE", False),
            ("SELECT", False),
        ]
    },

    {
        "topic": "delete",
        "statement": "Which SQL statement is used to remove records from a table?",
        "explanation": "DELETE removes one or more rows from a table.",
        "choices": [
            ("DELETE", True),
            ("DROP", False),
            ("UPDATE", False),
            ("SELECT", False),
        ]
    },
    {
        "topic": "select",
        "statement": "Which symbol is used to select all columns from a table?",
        "explanation": "The asterisk (*) selects all columns in a table.",
        "choices": [
            ("*", True),
            ("%", False),
            ("#", False),
            ("@", False),
        ]
    },
    {
        "topic": "select",
        "statement": "Which statement returns the 'name' column from the customers table?",
        "explanation": "SELECT name FROM customers retrieves only the name column.",
        "choices": [
            ("SELECT name FROM customers;", True),
            ("GET name FROM customers;", False),
            ("SHOW name FROM customers;", False),
            ("FIND name FROM customers;", False),
        ]
    },
    {
        "topic": "where",
        "statement": "Which operator checks if two values are equal?",
        "explanation": "The = operator compares two values for equality.",
        "choices": [
            ("=", True),
            ("==", False),
            ("===", False),
            ("<>=", False),
        ]
    },
    {
        "topic": "where",
        "statement": "Which query returns products with a price greater than 100?",
        "explanation": "The > operator selects values greater than the specified number.",
        "choices": [
            ("SELECT * FROM products WHERE price > 100;", True),
            ("SELECT * FROM products WHERE price < 100;", False),
            ("SELECT * FROM products ORDER BY price;", False),
            ("SELECT * FROM products GROUP BY price;", False),
        ]
    },
    {
        "topic": "order-by",
        "statement": "Which keyword sorts results in descending order?",
        "explanation": "DESC is used with ORDER BY to sort from highest to lowest.",
        "choices": [
            ("DESC", True),
            ("ASC", False),
            ("DOWN", False),
            ("REVERSE", False),
        ]
    },
    {
        "topic": "order-by",
        "statement": "What is the default sorting order of ORDER BY?",
        "explanation": "ORDER BY sorts in ascending order by default.",
        "choices": [
            ("Ascending", True),
            ("Descending", False),
            ("Random", False),
            ("Alphabetical only", False),
        ]
    },
    {
        "topic": "distinct",
        "statement": "Which query returns unique countries from the customers table?",
        "explanation": "DISTINCT removes duplicate values from the result set.",
        "choices": [
            ("SELECT DISTINCT country FROM customers;", True),
            ("SELECT UNIQUE country FROM customers;", False),
            ("SELECT country ONLY FROM customers;", False),
            ("SELECT FILTER country FROM customers;", False),
        ]
    },

    {
        "topic": "distinct",
        "statement": "What happens if DISTINCT is not used?",
        "explanation": "Duplicate values may appear in the result set.",
        "choices": [
            ("Duplicate values may be returned", True),
            ("Rows are automatically sorted", False),
            ("Rows are deleted", False),
            ("Results are grouped", False),
        ]
    },
    {
        "topic": "limit",
        "statement": "Which query returns only the first 5 rows?",
        "explanation": "LIMIT 5 restricts the result to five rows.",
        "choices": [
            ("SELECT * FROM customers LIMIT 5;", True),
            ("SELECT * FROM customers TOP 5;", False),
            ("SELECT FIRST 5 FROM customers;", False),
            ("SELECT * FROM customers ROWS 5;", False),
        ]
    },

    {
        "topic": "limit",
        "statement": "What is the purpose of LIMIT?",
        "explanation": "LIMIT controls how many rows are returned.",
        "choices": [
            ("Restrict returned rows", True),
            ("Sort rows", False),
            ("Delete rows", False),
            ("Group rows", False),
        ]
    },



    {
        "topic": "group-by",
        "statement": "GROUP BY is commonly used with which type of functions?",
        "explanation": "GROUP BY is usually combined with aggregate functions such as COUNT and SUM.",
        "choices": [
            ("Aggregate functions", True),
            ("String functions", False),
            ("Date functions", False),
            ("Math operators", False),
        ]
    },

    {
        "topic": "group-by",
        "statement": "Which function counts records in a group?",
        "explanation": "COUNT() returns the number of rows in each group.",
        "choices": [
            ("COUNT()", True),
            ("SUM()", False),
            ("AVG()", False),
            ("MAX()", False),
        ]
    },



    {
        "topic": "having",
        "statement": "Which clause is executed after GROUP BY?",
        "explanation": "HAVING filters the groups created by GROUP BY.",
        "choices": [
            ("HAVING", True),
            ("WHERE", False),
            ("LIMIT", False),
            ("DISTINCT", False),
        ]
    },

    {
        "topic": "having",
        "statement": "Why would you use HAVING instead of WHERE?",
        "explanation": "HAVING filters aggregated groups, while WHERE filters individual rows.",
        "choices": [
            ("To filter grouped results", True),
            ("To sort results", False),
            ("To insert rows", False),
            ("To delete rows", False),
        ]
    },

  

    {
        "topic": "inner-join",
        "statement": "Which rows are returned by an INNER JOIN?",
        "explanation": "INNER JOIN returns only rows that have matching values in both tables.",
        "choices": [
            ("Rows with matching values in both tables", True),
            ("All rows from the first table", False),
            ("All rows from the second table", False),
            ("All rows from both tables", False),
        ]
    },

    {
        "topic": "inner-join",
        "statement": "Which keyword is used to define the matching condition in a JOIN?",
        "explanation": "The ON clause specifies how the tables are related.",
        "choices": [
            ("ON", True),
            ("WHERE", False),
            ("MATCH", False),
            ("LINK", False),
        ]
    },



    {
        "topic": "left-join",
        "statement": "What happens when no matching row exists in the right table during a LEFT JOIN?",
        "explanation": "Columns from the right table will contain NULL values.",
        "choices": [
            ("NULL values are returned for the right table columns", True),
            ("The row is removed", False),
            ("The query fails", False),
            ("The row is duplicated", False),
        ]
    },

    {
        "topic": "left-join",
        "statement": "Which table has all of its rows returned in a LEFT JOIN?",
        "explanation": "LEFT JOIN always returns all rows from the left table.",
        "choices": [
            ("The left table", True),
            ("The right table", False),
            ("Both tables", False),
            ("Neither table", False),
        ]
    },



    {
        "topic": "right-join",
        "statement": "Which table has all of its rows returned in a RIGHT JOIN?",
        "explanation": "RIGHT JOIN always returns all rows from the right table.",
        "choices": [
            ("The right table", True),
            ("The left table", False),
            ("Both tables", False),
            ("Neither table", False),
        ]
    },

    {
        "topic": "right-join",
        "statement": "If there is no matching row in the left table during a RIGHT JOIN, what is returned?",
        "explanation": "Columns from the left table will contain NULL values.",
        "choices": [
            ("NULL values for the left table columns", True),
            ("The row is ignored", False),
            ("The query stops", False),
            ("Duplicate rows are created", False),
        ]
    },



    {
        "topic": "union",
        "statement": "What is required for two SELECT statements to be combined with UNION?",
        "explanation": "The SELECT statements must return the same number of columns with compatible data types.",
        "choices": [
            ("The same number of columns", True),
            ("The same table name", False),
            ("The same column names", False),
            ("The same primary key", False),
        ]
    },

    {
        "topic": "union",
        "statement": "What does UNION do with duplicate rows by default?",
        "explanation": "UNION removes duplicate rows from the combined result set.",
        "choices": [
            ("Removes duplicate rows", True),
            ("Keeps all duplicates", False),
            ("Sorts duplicates", False),
            ("Updates duplicates", False),
        ]
    },



    {
        "topic": "subquery",
        "statement": "Where can a subquery be used?",
        "explanation": "Subqueries can be used in SELECT, WHERE, HAVING, and other clauses.",
        "choices": [
            ("Inside another SQL statement", True),
            ("Only in SELECT", False),
            ("Only in WHERE", False),
            ("Only in JOIN", False),
        ]
    },

    {
        "topic": "subquery",
        "statement": "What is another name for a subquery?",
        "explanation": "A subquery is often called a nested query.",
        "choices": [
            ("Nested query", True),
            ("Linked query", False),
            ("Parent query", False),
            ("Aggregate query", False),
        ]
    },



    {
        "topic": "insert",
        "statement": "Which clause is commonly used with INSERT to provide values?",
        "explanation": "VALUES specifies the data that will be inserted.",
        "choices": [
            ("VALUES", True),
            ("SET", False),
            ("FROM", False),
            ("WHERE", False),
        ]
    },

    {
        "topic": "insert",
        "statement": "What does the INSERT statement do?",
        "explanation": "INSERT adds new rows to a table.",
        "choices": [
            ("Adds new rows", True),
            ("Updates rows", False),
            ("Deletes rows", False),
            ("Retrieves rows", False),
        ]
    },



    {
        "topic": "update",
        "statement": "Which keyword is used to specify the new value in an UPDATE statement?",
        "explanation": "SET is used to assign new values to columns.",
        "choices": [
            ("SET", True),
            ("VALUES", False),
            ("CHANGE", False),
            ("MODIFY", False),
        ]
    },

    {
        "topic": "update",
        "statement": "What happens if an UPDATE statement is executed without a WHERE clause?",
        "explanation": "All rows in the table may be updated.",
        "choices": [
            ("All rows may be updated", True),
            ("Only one row is updated", False),
            ("The query fails", False),
            ("No rows are updated", False),
        ]
    },

    {
        "topic": "delete",
        "statement": "What happens if a DELETE statement is executed without a WHERE clause?",
        "explanation": "All rows in the table may be deleted.",
        "choices": [
            ("All rows may be deleted", True),
            ("Only one row is deleted", False),
            ("The query fails", False),
            ("No rows are deleted", False),
        ]
    },

    {
        "topic": "delete",
        "statement": "Which SQL statement removes records from a table?",
        "explanation": "DELETE removes one or more rows from a table.",
        "choices": [
            ("DELETE", True),
            ("DROP", False),
            ("REMOVE", False),
            ("CLEAR", False),
        ]
    }
]

PRACTICES = [
    {
        "topic": "select",
        "title": "Select all customers",
        "instructions": "Return all columns from the customers table ordered by id.",
        "expected_query": "SELECT id, name, city FROM customers ORDER BY id;",
        "dataset": {
            "customers": [
                {"id": "1", "name": "Ana", "city": "Recife"},
                {"id": "2", "name": "Bruno", "city": "Salvador"},
                {"id": "3", "name": "Carla", "city": "Fortaleza"},
            ]
        },
    },
    {
        "topic": "where",
        "title": "Products above 100",
        "instructions": "Return all products with price greater than 100 ordered by id.",
        "expected_query": "SELECT id, name, price FROM products WHERE price > 100 ORDER BY id;",
        "dataset": {
            "products": [
                {"id": "1", "name": "Keyboard", "price": "90"},
                {"id": "2", "name": "Monitor", "price": "150"},
                {"id": "3", "name": "Mouse", "price": "120"},
            ]
        },
    },
    {
        "topic": "order-by",
        "title": "Sort employees by salary",
        "instructions": "Return employee name and salary ordered by salary descending, then name ascending.",
        "expected_query": "SELECT name, salary FROM employees ORDER BY salary DESC, name ASC;",
        "dataset": {
            "employees": [
                {"id": "1", "name": "Ana", "salary": "3000"},
                {"id": "2", "name": "Bruno", "salary": "4500"},
                {"id": "3", "name": "Carla", "salary": "4500"},
            ]
        },
    },
    {
        "topic": "distinct",
        "title": "Unique customer countries",
        "instructions": "Return the distinct countries from customers ordered alphabetically.",
        "expected_query": "SELECT DISTINCT country FROM customers ORDER BY country;",
        "dataset": {
            "customers": [
                {"id": "1", "name": "Ana", "country": "Brazil"},
                {"id": "2", "name": "Bruno", "country": "Brazil"},
                {"id": "3", "name": "Carla", "country": "Chile"},
                {"id": "4", "name": "Diego", "country": "Argentina"},
            ]
        },
    },
    {
        "topic": "limit",
        "title": "First two products",
        "instructions": "Return the first two products ordered by id.",
        "expected_query": "SELECT id, name FROM products ORDER BY id LIMIT 2;",
        "dataset": {
            "products": [
                {"id": "1", "name": "Notebook"},
                {"id": "2", "name": "Keyboard"},
                {"id": "3", "name": "Mouse"},
            ]
        },
    },
    {
        "topic": "group-by",
        "title": "Count employees by department",
        "instructions": "Return each department and the number of employees in it, ordered by department.",
        "expected_query": "SELECT department, COUNT(*) AS total FROM employees GROUP BY department ORDER BY department;",
        "dataset": {
            "employees": [
                {"id": "1", "name": "Ana", "department": "Engineering"},
                {"id": "2", "name": "Bruno", "department": "Engineering"},
                {"id": "3", "name": "Carla", "department": "Sales"},
                {"id": "4", "name": "Diego", "department": "Sales"},
                {"id": "5", "name": "Eva", "department": "Sales"},
            ]
        },
    },
    {
        "topic": "having",
        "title": "Departments with at least two employees",
        "instructions": "Return departments with at least two employees and their totals, ordered by department.",
        "expected_query": "SELECT department, COUNT(*) AS total FROM employees GROUP BY department HAVING COUNT(*) >= 2 ORDER BY department;",
        "dataset": {
            "employees": [
                {"id": "1", "name": "Ana", "department": "Engineering"},
                {"id": "2", "name": "Bruno", "department": "Engineering"},
                {"id": "3", "name": "Carla", "department": "Sales"},
                {"id": "4", "name": "Diego", "department": "HR"},
            ]
        },
    },
    {
        "topic": "inner-join",
        "title": "Orders with customer names",
        "instructions": "Return customer name, order id and total for matching orders, ordered by order id.",
        "expected_query": """
SELECT customers.name, orders.id, orders.total
FROM customers
INNER JOIN orders
ON customers.id = orders.customer_id
ORDER BY orders.id;
""".strip(),
        "dataset": {
            "customers": [
                {"id": "1", "name": "Ana"},
                {"id": "2", "name": "Bruno"},
                {"id": "3", "name": "Carla"},
            ],
            "orders": [
                {"id": "101", "customer_id": "1", "total": "120"},
                {"id": "102", "customer_id": "2", "total": "95"},
                {"id": "103", "customer_id": "2", "total": "200"},
                {"id": "104", "customer_id": "9", "total": "999"},
            ],
        },
    },
    {
        "topic": "left-join",
        "title": "All customers and their orders",
        "instructions": "Return every customer and the matching order id, ordered by customer id and order id.",
        "expected_query": """
SELECT customers.name, orders.id
FROM customers
LEFT JOIN orders
ON customers.id = orders.customer_id
ORDER BY customers.id, orders.id;
""".strip(),
        "dataset": {
            "customers": [
                {"id": "1", "name": "Ana"},
                {"id": "2", "name": "Bruno"},
                {"id": "3", "name": "Carla"},
            ],
            "orders": [
                {"id": "101", "customer_id": "1"},
                {"id": "102", "customer_id": "1"},
                {"id": "103", "customer_id": "2"},
            ],
        },
    },
    {
        "topic": "right-join",
        "title": "All orders and matching customers",
        "instructions": "Return every order and its customer name using right-join semantics, ordered by order id.",
        "expected_query": """
SELECT orders.id, customers.name
FROM orders
LEFT JOIN customers
ON customers.id = orders.customer_id
ORDER BY orders.id;
""".strip(),
        "dataset": {
            "customers": [
                {"id": "1", "name": "Ana"},
                {"id": "2", "name": "Bruno"},
            ],
            "orders": [
                {"id": "101", "customer_id": "1"},
                {"id": "102", "customer_id": "2"},
                {"id": "103", "customer_id": "999"},
            ],
        },
    },
    {
        "topic": "union",
        "title": "Cities from customers and suppliers",
        "instructions": "Return all unique cities from customers and suppliers ordered alphabetically.",
        "expected_query": """
SELECT city FROM customers
UNION
SELECT city FROM suppliers
ORDER BY city;
""".strip(),
        "dataset": {
            "customers": [
                {"id": "1", "city": "Recife"},
                {"id": "2", "city": "Salvador"},
                {"id": "3", "city": "Fortaleza"},
            ],
            "suppliers": [
                {"id": "1", "city": "Recife"},
                {"id": "2", "city": "Natal"},
            ],
        },
    },
    {
        "topic": "subquery",
        "title": "Employees above average salary",
        "instructions": "Return the names of employees whose salary is above the average salary, ordered by name.",
        "expected_query": """
SELECT name
FROM employees
WHERE salary > (
    SELECT AVG(salary)
    FROM employees
)
ORDER BY name;
""".strip(),
        "dataset": {
            "employees": [
                {"id": "1", "name": "Ana", "salary": "3000"},
                {"id": "2", "name": "Bruno", "salary": "4500"},
                {"id": "3", "name": "Carla", "salary": "6000"},
                {"id": "4", "name": "Diego", "salary": "2500"},
            ]
        },
    },
    {
        "topic": "insert",
        "title": "Insert a new customer",
        "instructions": "Insert a new customer with id 4, name Diana and city Recife, returning the inserted row.",
        "expected_query": """
INSERT INTO customers (id, name, city)
VALUES ('4', 'Diana', 'Recife')
RETURNING id, name, city;
""".strip(),
        "dataset": {
            "customers": [
                {"id": "1", "name": "Ana", "city": "Recife"},
                {"id": "2", "name": "Bruno", "city": "Salvador"},
                {"id": "3", "name": "Carla", "city": "Fortaleza"},
            ]
        },
    },
    {
        "topic": "update",
        "title": "Update a customer's city",
        "instructions": "Update Bruno's city to Sao Paulo and return the updated row.",
        "expected_query": """
UPDATE customers
SET city = 'Sao Paulo'
WHERE id = '2'
RETURNING id, name, city;
""".strip(),
        "dataset": {
            "customers": [
                {"id": "1", "name": "Ana", "city": "Recife"},
                {"id": "2", "name": "Bruno", "city": "Salvador"},
                {"id": "3", "name": "Carla", "city": "Fortaleza"},
            ]
        },
    },
    {
        "topic": "delete",
        "title": "Preview the customer to delete",
        "instructions": "Return the customer row that should be deleted for id 3. This is a workaround because the current validator does not safely auto-grade DELETE yet.",
        "expected_query": """
SELECT id, name, city
FROM customers
WHERE id = '3';
""".strip(),
        "dataset": {
            "customers": [
                {"id": "1", "name": "Ana", "city": "Recife"},
                {"id": "2", "name": "Bruno", "city": "Salvador"},
                {"id": "3", "name": "Carla", "city": "Fortaleza"},
            ]
        },
    },
]



class Command(BaseCommand):
    help = "Populate database with QueryLab topics and questions"

    def handle(self, *args, **kwargs):

        for topic_data in TOPICS:

            topic, created = Topics.objects.get_or_create(
                slug=topic_data["slug"],
                defaults=topic_data
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {topic.title}"
                    )
                )
        
        for question_data in QUESTIONS:
            topic = Topics.objects.get(slug=question_data["topic"])
            
            question, created = Questions.objects.get_or_create(

                topic=topic,
                statement=question_data["statement"],
                defaults={
                    "explanation": question_data["explanation"],
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Question Created: {question.topic}"
                    )
                        )
            for choice_text, is_correct in question_data["choices"]:
                Choices.objects.get_or_create(
                    question=question,
                    text=choice_text,
                    defaults={"is_correct": is_correct}
                )


        for practice_data in PRACTICES:
            topic = Topics.objects.get(slug=practice_data["topic"])

            practice, created = PracticeExercise.objects.update_or_create(
                    topic=topic,
                    title=practice_data["title"],
                    defaults={
                        "instructions": practice_data["instructions"],
                        "expected_query": practice_data["expected_query"],
                        "dataset": practice_data["dataset"],
                    },
                )

            action = "Created" if created else "Updated"
            self.stdout.write(
                    self.style.SUCCESS(f"{action} practice: {practice.title}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Topics, Questions, Practices seeded successfully!"
            )
        )
