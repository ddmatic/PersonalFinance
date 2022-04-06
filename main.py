from conn import sqlite as d
from sqlite3 import Error
from model.finance import Record

conn = d.create_connection()
with conn:
    try:
        op_choice = input("""Select operation!\n- New (1)\n- Delete (2)\n- Update (3)\n- View all (4)\n- View category (5)\n- SUM (6)\n- Overview (7)\nCHOICE: """).lower()

        if op_choice in (
                'new', 'delete', 'view all', 'view category', 'sum', 'overview', 'update', '1', '2', '3', '4', '5', '6',
                '7'):

            if op_choice == 'new' or op_choice == '1':
                print('\nCreating new record!')
                i_cat = input('Input category: ').capitalize()
                i_amount = int(input('Amount: '))
                record_1 = Record(i_cat, i_amount)
                d.create_record(conn, record_1)

            elif op_choice == 'delete' or op_choice == '2':
                print('\nDELETING RECORD!!!')
                d.delete_record(conn, int(input('Id to delete: ')))

            elif op_choice == 'update' or op_choice == '3':
                print('\nUPDATING RECORD!!!')
                i_id = int(input('Input record ID: '))
                i_amount = int(input('Input new amount: '))
                d.update_amount(conn, i_id, i_amount)

            elif op_choice == 'view all' or op_choice == '4':
                print('\nID', '|', 'CATEGORY', '|', 'AMOUNT')
                for id, cat, amount in d.get_all(conn):
                    print(id, '|', cat, '|', amount)

            elif op_choice == 'view category' or op_choice == '5':
                print('\nSelect category for details!')
                i_cat = input('Input category: ').capitalize()
                print('ID', '|', 'CATEGORY', '|', 'AMOUNT')
                for id, cat, amount in d.get_category(conn, i_cat):
                    print(id, '|', cat, '|', amount)

            elif op_choice == 'sum' or op_choice == '6':
                print('\nSelect category to summarize!')
                i_cat = input('Input category: ').capitalize()
                isolated = d.sum_cat(conn, i_cat)
                print(*isolated[0])



            elif op_choice == 'overview' or op_choice == '7':
                print('\n')
                for i, z in d.cat_overview(conn):
                    print(i + ': ' + str(z) + '%')
        else:
            print('\nInvalid operation, please select again!')
    except Error as e:
        print(e)
