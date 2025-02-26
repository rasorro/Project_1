INSERT INTO [Authentication] (userID, passwordHash)
Values
	('TEST1', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
	('OTHER', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO [Products] (ProductID, ProductName, CategoryID, QuantityPerUnit, UnitPrice)
Values
	(1, "Example item-1", 1, 5, 9.99),
	(2, "Example item-2", 2, 5, 10.99);

INSERT INTO [Categories] (CategoryID, CategoryName)
Values
	(1, "Example category-1"),
	(2, "Example category-2");