import sqlite3
from datetime import datetime
import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS [Authentication] (
            [userID]TEXT PRIMARY KEY REFERENCES [Customers]([CustomerID]) ON DELETE CASCADE,
            [passwordHash]TEXT NOT NULL,
            [sessionID]TEXT
        );
                     
        CREATE TABLE IF NOT EXISTS [Shopping_Cart] (
            [cartID]TEXT PRIMARY KEY,
            [shopperID]TEXT,
            [productID]TEXT NOT NULL REFERENCES [Products]([ProductID]),
            [quantity]INTEGER NOT NULL CHECK ([quantity] > 0),
            [added_at]TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS [Orders](
            [OrderID]INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            [CustomerID]TEXT,
            [EmployeeID]INTEGER,
            [OrderDate]DATETIME,
            [RequiredDate]DATETIME,
            [ShippedDate]DATETIME,
            [ShipVia]INTEGER,
            [Freight]NUMERIC DEFAULT 0,
            [ShipName]TEXT,
            [ShipAddress]TEXT,
            [ShipCity]TEXT,
            [ShipRegion]TEXT,
            [ShipPostalCode]TEXT,
            [ShipCountry]TEXT,
            FOREIGN KEY ([EmployeeID]) REFERENCES [Employees] ([EmployeeID]) 
                    ON DELETE NO ACTION ON UPDATE NO ACTION,
                FOREIGN KEY ([CustomerID]) REFERENCES [Customers] ([CustomerID]) 
                    ON DELETE NO ACTION ON UPDATE NO ACTION,
                FOREIGN KEY ([ShipVia]) REFERENCES [Shippers] ([ShipperID]) 
                    ON DELETE NO ACTION ON UPDATE NO ACTION
        );
        
        CREATE TABLE IF NOT EXISTS [Order Details](
            [OrderID]INTEGER NOT NULL,
            [ProductID]INTEGER NOT NULL,
            [UnitPrice]NUMERIC NOT NULL DEFAULT 0,
            [Quantity]INTEGER NOT NULL DEFAULT 1,
            [Discount]REAL NOT NULL DEFAULT 0,
                PRIMARY KEY ("OrderID","ProductID"),
                CHECK ([Discount]>=(0) AND [Discount]<=(1)),
                CHECK ([Quantity]>(0)),
                CHECK ([UnitPrice]>=(0)),
                FOREIGN KEY ([OrderID]) REFERENCES [Orders] ([OrderID]) 
                    ON DELETE NO ACTION ON UPDATE NO ACTION,
                FOREIGN KEY ([ProductID]) REFERENCES [Products] ([ProductID]) 
                    ON DELETE NO ACTION ON UPDATE NO ACTION
        );
        
        CREATE TABLE IF NOT EXISTS [Products](
            [ProductID]INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            [ProductName]TEXT NOT NULL,
            [SupplierID]INTEGER,
            [CategoryID]INTEGER,
            [QuantityPerUnit]TEXT,
            [UnitPrice]NUMERIC DEFAULT 0,
            [UnitsInStock]INTEGER DEFAULT 0,
            [UnitsOnOrder]INTEGER DEFAULT 0,
            [ReorderLevel]INTEGER DEFAULT 0,
            [Discontinued]TEXT NOT NULL DEFAULT '0',
                CHECK ([UnitPrice]>=(0)),
                CHECK ([ReorderLevel]>=(0)),
                CHECK ([UnitsInStock]>=(0)),
                CHECK ([UnitsOnOrder]>=(0)),
                FOREIGN KEY ([CategoryID]) REFERENCES [Categories] ([CategoryID]) 
                    ON DELETE NO ACTION ON UPDATE NO ACTION,
                FOREIGN KEY ([SupplierID]) REFERENCES [Suppliers] ([SupplierID]) 
                    ON DELETE NO ACTION ON UPDATE NO ACTION
        );
        
        CREATE TABLE IF NOT EXISTS [Categories](
            [CategoryID] INTEGER PRIMARY KEY AUTOINCREMENT,
            [CategoryName] TEXT,
            [Description] TEXT,
            [Picture] BLOB
        );
        
        CREATE TABLE IF NOT EXISTS [Customers](
            [CustomerID] TEXT,
            [CompanyName] TEXT,
            [ContactName] TEXT,
            [ContactTitle] TEXT,
            [Address] TEXT,
            [City] TEXT,
            [Region] TEXT,
            [PostalCode] TEXT,
            [Country] TEXT,
            [Phone] TEXT,
            [Fax] TEXT,
            PRIMARY KEY (`CustomerID`)
        );
        
        CREATE TABLE IF NOT EXISTS [Employees](
            [EmployeeID] INTEGER PRIMARY KEY AUTOINCREMENT,
            [LastName] TEXT,
            [FirstName] TEXT,
            [Title] TEXT,
            [TitleOfCourtesy] TEXT,
            [BirthDate] DATE,
            [HireDate] DATE,
            [Address] TEXT,
            [City] TEXT,
            [Region] TEXT,
            [PostalCode] TEXT,
            [Country] TEXT,
            [HomePhone] TEXT,
            [Extension] TEXT,
            [Photo] BLOB,
            [Notes] TEXT,
            [ReportsTo] INTEGER,
            [PhotoPath] TEXT,
            FOREIGN KEY ([ReportsTo]) REFERENCES [Employees] ([EmployeeID]) 
                ON DELETE NO ACTION ON UPDATE NO ACTION
        );
    """)
    db.commit()

@click.command('init-db')
def init_db_command():
    """Create necessary tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('test-db')
def test_db_command():
    db = get_db()
    result = db.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    print([row["name"] for row in result])

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(test_db_command)
    app.cli.add_command(init_db_command)
