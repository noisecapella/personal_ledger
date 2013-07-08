DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions (
id integer PRIMARY KEY AUTOINCREMENT,
description text NOT NULL,
withdrawal float NOT NULL,
deposit float NOT NULL,
account_id integer NOT NULL,
other_transaction_id integer NOT NULL
);

DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
full_title text NOT NULL,
parent_id integer
);

INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (0, 'Liabilities', NULL, 'Liabilities');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (1, 'Credit Card', 0, 'Liabilities - Credit Card');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (2, 'Assets', NULL, 'Assets');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (3, 'Cash in Wallet', 2, 'Assets - Cash in Wallet');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (4, 'Bank Checking', 2, 'Assets - Bank Checking');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (5, 'Bank Savings', 2, 'Assets - Bank Savings');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (6, 'Expenses', NULL, 'Expenses');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (7, 'Laundry/Dry Cleaning', 6, 'Expenses - Laundry/Dry Cleaning');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (8, 'Travel', 6, 'Expenses - Travel');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (9, 'Music/Movies', 6, 'Expenses - Music/Movies');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (10, 'Dining', 6, 'Expenses - Dining');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (11, 'Supplies', 6, 'Expenses - Supplies');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (12, 'Subscriptions', 6, 'Expenses - Subscriptions');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (13, 'Miscellaneous', 6, 'Expenses - Miscellaneous');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (14, 'Gifts', 6, 'Expenses - Gifts');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (15, 'Phone', 6, 'Expenses - Phone');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (16, 'Public Transportation', 6, 'Expenses - Public Transportation');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (17, 'Books', 6, 'Expenses - Books');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (18, 'Groceries', 6, 'Expenses - Groceries');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (19, 'Charity', 6, 'Expenses - Charity');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (20, 'Recreation', 6, 'Expenses - Recreation');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (21, 'Cable', 6, 'Expenses - Cable');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (22, 'Taxes', 6, 'Expenses - Taxes');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (23, 'Federal', 22, 'Expenses - Taxes - Federal');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (24, 'Other Tax', 22, 'Expenses - Taxes - Other Tax');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (25, 'Social Security', 22, 'Expenses - Taxes - Social Security');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (26, 'Medicare', 22, 'Expenses - Taxes - Medicare');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (27, 'State/Providence', 22, 'Expenses - Taxes - State/Providence');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (28, 'Medical Expenses', 6, 'Expenses - Medical Expenses');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (29, 'Clothes', 6, 'Expenses - Clothes');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (30, 'Bicycle', 6, 'Expenses - Bicycle');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (31, 'Utilities', 6, 'Expenses - Utilities');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (32, 'Water', 31, 'Expenses - Utilities - Water');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (33, 'Gas', 31, 'Expenses - Utilities - Gas');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (34, 'Electric', 31, 'Expenses - Utilities - Electric');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (35, 'Garbage collection', 31, 'Expenses - Utilities - Garbage collection');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (36, 'Computer', 6, 'Expenses - Computer');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (37, 'Online Services', 6, 'Expenses - Online Services');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (38, 'Rent', 6, 'Expenses - Rent');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (39, 'Hobbies', 6, 'Expenses - Hobbies');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (40, 'Education', 6, 'Expenses - Education');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (41, 'Insurance', 6, 'Expenses - Insurance');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (42, 'Life Insurance', 41, 'Expenses - Insurance - Life Insurance');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (43, 'Health Insurance', 41, 'Expenses - Insurance - Health Insurance');
INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (44, 'Auto Insurance', 41, 'Expenses - Insurance - Auto Insurance');
