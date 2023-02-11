import pandas as pd
import sqlite3 

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# df = pd.read_csv('store/data_1.csv')

# print(df)

# df.to_sql('auto_tmp', conn, if_exists='replace')

# cursor.execute('select * from auto_tmp')

# for row in cursor.fetchall():
# 	print(row)

# ф-я кот получает путь до файла и название таблицы в
# кач-ве арг-в и грузит данные из файл в таблицу

def csv_to_sql(path, table):
	df = pd.read_csv(path)
	df.to_sql(table, conn, if_exists='replace')

def show_data(source):
	print('_-' * 20)
	print(source)
	print('_-' * 20)

	cursor.execute(f'select * from {source}')

	for row in cursor.fetchall():
		print(row)
	print('_-' * 20)

def init_auto_hist():
	cursor.execute('''
		CREATE TABLE if not exists auto_hist(
			id integer primary key autoincrement,
			model varchar(128),
			transmission varchar(128),
			body_type varchar(128),
			drive_type varchar(128),
			color varchar(128),
			production_year integer,
			auto_key integer,
			engine_capacity real,
			horsepower integer,
			engine_type varchar(128),
			price integer,
			milage integer,
			deleted_flg integer default 0,
			start_dttm datetime default current_timestamp,
			end_dttm datetime default (datetime('2999-12-31 23:59:59'))
		)
	''')

	# представление v_auto с актуальным срезом
	cursor.execute('''
		CREATE VIEW if not exists v_auto as 
		select 
			model, 
			transmission,
			body_type,
			drive_type,
			color,
			production_year,
			auto_key,
			engine_capacity,
			horsepower,
			engine_type,
			price,
			milage
		from auto_hist
		where deleted_flg = 0
		and current_timestamp between start_dttm and end_dttm
	''')

# новые записи - те, которые есть в auto_temp и которых нет в auto_hist  

def create_new_rows():
	cursor.execute('''
		CREATE TABLE new_rows_tmp as
			select 
				t1.* 
			from auto_tmp t1
			left join v_auto t2
			on t1.auto_key = t2.auto_key 
			where t2.auto_key is null
	''')

# удаленные записи - те, которые есть в auto_hist и которых нет в auto_temp  

def create_deleted_rows():
	cursor.execute('''
		CREATE TABLE deleted_rows_tmp as
			select 
				t1.* 
			from v_auto t1
			left join auto_tmp t2
			on t1.auto_key = t2.auto_key 
			where t2.auto_key is null
	''')

# измененные записи - те, которые есть в auto_temp и auto_temp 
# по ключу auto_key, но одно из бизнес-полей отличается
def create_changed_rows():
	cursor.execute('''
		CREATE TABLE if not exists changed_rows_tmp as
			select 
				t2.* 
			from v_auto t1
			inner join auto_tmp t2
			on t1.auto_key = t2.auto_key 
			and (t1.model           <> t2.model
			    or t1.transmission    <> t2.transmission
			    or t1.body_type       <> t2.body_type
			    or t1.drive_type      <> t2.drive_type
			    or t1.color           <> t2.color
			    or t1.production_year <> t2.production_year
			    or t1.engine_capacity <> t2.engine_capacity
			    or t1.horsepower      <> t2.horsepower
			    or t1.engine_type     <> t2.engine_type
			    or t1.price           <> t2.price
			    or t1.milage          <> t2.milage
			) 
	''')	

def update_auto_hist():
	cursor.execute('''
		INSERT INTO auto_hist(
				model, 
				transmission,
				body_type,
				drive_type,
				color,
				production_year,
				auto_key,
				engine_capacity,
				horsepower,
				engine_type,
				price,
				milage
			) 
			select
				model, 
				transmission,
				body_type,
				drive_type,
				color,
				production_year,
				auto_key,
				engine_capacity,
				horsepower,
				engine_type,
				price,
				milage
		from new_rows_tmp
	''')

# актуализировать изм-е данные в auto_hist
	cursor.execute('''
		UPDATE auto_hist
		set end_dttm = datetime('now', '-1 second')
		where auto_key in (select auto_key from changed_rows_tmp)
		and end_dttm = datetime ('2999-12-31 23:59:59')
	''')

	cursor.execute('''
		INSERT INTO auto_hist(
				model, 
				transmission,
				body_type,
				drive_type,
				color,
				production_year,
				auto_key,
				engine_capacity,
				horsepower,
				engine_type,
				price,
				milage
			) 
			select
				model, 
				transmission,
				body_type,
				drive_type,
				color,
				production_year,
				auto_key,
				engine_capacity,
				horsepower,
				engine_type,
				price,
				milage
			from changed_rows_tmp
		''')

# актуализировать удален-е данные в auto_hist
	cursor.execute('''
		UPDATE auto_hist
		set end_dttm = datetime('now', '-1 second')
		where auto_key in (select auto_key from deleted_rows_tmp)
		and end_dttm = datetime ('2999-12-31 23:59:59')
	''')
	
	cursor.execute('''
		INSERT INTO auto_hist(
				model, 
				transmission,
				body_type,
				drive_type,
				color,
				production_year,
				auto_key,
				engine_capacity,
				horsepower,
				engine_type,
				price,
				milage,
				deleted_flg
			) 
			select
				model, 
				transmission,
				body_type,
				drive_type,
				color,
				production_year,
				auto_key,
				engine_capacity,
				horsepower,
				engine_type,
				price,
				milage,
				1
			from deleted_rows_tmp
		''')

	conn.commit()

def drop_tmp_tables():
	cursor.execute('DROP TABLE if exists auto_tmp'),
	cursor.execute('DROP TABLE if exists new_rows_tmp'),
	cursor.execute('DROP TABLE if exists deleted_rows_tmp'),
	cursor.execute('DROP TABLE if exists changed_rows_tmp')

	
init_auto_hist()
drop_tmp_tables()
csv_to_sql('store/data_3.csv', 'auto_tmp')
create_new_rows()
create_deleted_rows()
create_changed_rows()
update_auto_hist()

show_data('auto_tmp')
show_data('new_rows_tmp')
show_data('deleted_rows_tmp')
show_data('changed_rows_tmp')
show_data('auto_hist')



# заменить auto_hist на v_auto при форм-и временных таблиц