---
layout: post
title:  "Constraints and Views Study Note"
author: Yuchen Zhang
categories: computer
date:   2021-05-06
tags: ["study notes", "constraints", "views"]
---

## Constraints

### Kinds of Constraints

- Keys
- Foreign-key, or referential-integrity
- Value-based constraints
  - Constrain values of a particular attribute
- Tuple-based constraints
  - Constrain relationship among attributes
- Assertions: any SQL boolean expression
  - Very expressive

### Keys

Specified using "primary key" or "unique":

```sql
CREATE TABLE Sells(
    bar VARCHAR(100) REFERENCES Bars(name),
    beer VARCHAR(100) REFERENCES Beers(name),
    price REAL,
    PRIMARY KEY(bar, beer)
);
```

#### Primary Key vs Unique

- Referenced attributes must be declared as `PRIMARY KEY` or `UNIQUE`.
  - Otherwise, MySQL does not allow creation of the table
  - Note that primary key can not be null, but unique attribute can
- Null values can be inserted into attribute of foreign key
  - Even though it refers to primary key in referenced table

### Foreign Keys

Use the keyword `REFERENCES`, either:

1. Within the declaration of an attribute, when only
one attribute is involved, or
2. As an element of the schema, as:
FOREIGN KEY ( \<list of attributes\> ) REFERENCES \<relation\> ( \<attributes\> )

- Note MySQL seems to enforce Foreign Key only when defined as an element

#### Express Foreign Key with Attribute

```sql
CREATE TABLE Beers (
    name CHAR(20) PRIMARY KEY,
    manf CHAR(20) );

CREATE TABLE Sells (
    bar CHAR(20),
    beer CHAR(20) REFERENCES Beers(name), 
    price REAL );
```

#### Express Foreign Key as Element

```sql
CREATE TABLE Beers (
    name CHAR(20) PRIMARY KEY,
    manf CHAR(20) );

CREATE TABLE Sells (
    bar CHAR(20),
    beer CHAR(20),
    price REAL,
    FOREIGN KEY(beer) REFERENCES BEERS(name)); -- here name must be primary key
```

#### Express Foreign Key with Unique Attributes

```sql
CREATE TABLE R (a INT PRIMARY KEY);
INSERT INTO R VALUES (1);
SELECT * FROM R;
```

```
+---+
| a |
+---+
| 1 |
+---+
1 row in set (0.00 sec)
```

```sql
CREATE TABLE S (b INT, FOREIGN KEY (b) REFERENCES R(a));
INSERT INTO S VALUES (1);    -- this works because "a" in R has number 1
INSERT INTO S VALUES (NULL); -- this also works even though "a" is primary key in R
INSERT INTO S VALUES (2);    -- this doesn't work because "a" in R doesn't have number 2
SELECT * FROM S;
```

```
+------+
| b    |
+------+
| NULL |
|    1 |
+------+
2 rows in set (0.00 sec)
```

#### Enforcing Foreign Key Constraints

If there is a foreign-key constraint from attributes of relation S to the primary key (or unique attribute) of relation R, two violations are possible:

1. An insert or update to S introduces values not found in R.
2. A deletion or update to R causes some tuples of S to “dangle.”

#### Dealing with Enforcing Foreign Key Constraints

Example: Suppose R = Beers, S = Sells.

- An insert or update to Sells that introduces a nonexistent beer must be rejected.
- A deletion or update to Beers that removes a beer value found in some tuples of Sells can be handled in three ways. 
  1. *Default*: Reject the modification
  2. *Cascade*: Make the same changes in Sells.
     - Deleted beer: delete Sells tuple.
     - Updated beer: change value in Sells.
  3. *Set NULL*: Change the beers in Sells to `NULL`.

```sql
CREATE TABLE Sells (
    bar CHAR(20),
    beer CHAR(20),
    price REAL,
    FOREIGN KEY(beer)
        REFERENCES Beers(name)
        ON DELETE SET NULL   -- set on delete separately with its type
        ON UPDATE CASCADE ); -- set on update separately with its type
```

### Value-based constraints

#### Attribute-Based Checks

Make sure every insertion of age is smaller than 100:

```sql
CREATE TABLE student (
    age TINYINT CHECK (age < 100)
);
```

Make sure every insertion of beer is in the names of Beers table and price is smaller than or equal to 5.00.

```sql
CREATE TABLE Sells (
    bar CHAR(20),
    beer CHAR(20) CHECK ( beer IN
        (SELECT name FROM Beers)),
        -- Does not checked if a beer is deleted 
        -- from Beers (unlike foreign-keys).
    price REAL CHECK ( price <= 5.00 )
);
```

##### Timing of Attribute-Based Checks

An attribute-based check is checked only when a value for that attribute is inserted or updated.

- Example: CHECK (price <= 5.00) checks every new price and rejects it if it is more than $5.
- Example: CHECK (beer IN (SELECT name FROM Beers)) not checked if a beer is deleted from Beers (unlike foreign-keys).

#### Tuple-based Checks

- CHECK ( \<condition\> ) may be added as another element of a schema definition.
- The condition may refer to any attribute of the relation, but any other attributes or relations require a subquery.
- Checked on insert or update only.

Example: If we want only Joe’s Bar can sell beer for more than $5.

```sql
CREATE TABLE Sells (
    bar CHAR(20),
    beer CHAR(20),
    price REAL,
    CHECK (bar = 'Joe' OR price <= 5.00)
);
```

#### Assertions (Not Supported in MySQL)

- These are database-schema elements, like relations or views.
- Defined by:`CREATE ASSERTION <name> CHECK ( <condition> );`
- Condition may refer to any relation or attribute in the database schema.
- Very expensive to enforce
  - Neither PostgreSQL nor MySQL supports this

Example: In Sells(bar, beer, price), bars cannot charge an average of more than $5.

```sql
CREATE ASSERTION NoRipoffBars CHECK (
    NOT EXISTS (
        SELECT bar FROM Sells
        GROUP BY bar
        HAVING 5.00 < AVG(price)
));
```

Example: In Drinkers(name, addr, phone) and Bars(name, addr, license), there cannot be more bars than drinkers.

```sql
CREATE ASSERTION FewBar CHECK (
    (SELECT COUNT(*) FROM Bars) <=
    (SELECT COUNT(*) FROM Drinkers)
);
```

##### Timing of Assertion Checks

- In principle, we must check every assertion after every modification to any relation of the database.
- A clever system can observe that only certain changes could cause a given assertion to be violated.
  - Example: No change to Beers can affect FewBar. Neither can an insertion to Drinkers.

## Views

- A view is a “virtual table,” a relation that is defined in terms of the contents of other tables and views.
- Declare by: `CREATE VIEW <name> AS <query>;`
- In contrast, a relation whose value is really stored in the database is called a base table.

Example: CanDrink(drinker, beer) is a view “containing” the drinker-beer pairs such that the drinker frequents at least one bar that serves the beer.

```sql
CREATE VIEW CanDrink AS
SELECT distinct drinker, beer
FROM Frequents, Sells
WHERE Frequents.bar = Sells.bar;
```

Example: Accessing a View

- You may query a view as if it were a base table.
  - There is a limited ability to modify views if the modification makes sense as a modification of the underlying base table.

```sql
SELECT * FROM CanDrink
WHERE drinker = 'Bill';
```

### What Happens When a View Is Used?

- The DBMS starts by interpreting the query as if the view were a base table.
  - Typical DBMS turns the query into something like relational algebra.
- The queries defining any views used by the query are also replaced by their algebraic equivalents, and "spliced into" the expression tree for the query.

### DMBS Optimization

- It is interesting to observe that the typical DBMS will then "optimize" the query by transforming the algebraic expression to one that can be executed faster.
- Key optimizations:
  1. Push selections down the tree.
  2. Eliminate unnecessary projections.

{% figure view-optimization png 'Optimization' %}

### Types of Views

- Virtual views:
  - Computed only on-demand -- slow at runtime
  - Always up to date
- Materialized views
  - Precomputed offline -- fast at runtime
  - Common in data warehouses
  - May have stale data