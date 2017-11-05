import MySQLdb as sql
import re

db = sql.connect(user="user",passwd="password",db="db_name",host="localhost")
path = input("Enter the file path(eg- /home/user/Desktop/vendor1.html.xml)- ")
filename = (path.split('/')[-1]).split('.')[0]
path = "'" + path + "'"
filename = "'" + filename + "'"
base_cur = db.cursor()
base_cur.execute("load xml local infile {0} into table inputdata rows identified by '<text>' (@top, @left, @width, @height, @text,@b) set Top=@top, Left_mar=@left, Width=@width,Height=@height, tag_data=@text, extra=@b, fname={1};".format(path, filename))
base_cur.execute("update inputdata set tag_data=extra where extra is not null;")
base_cur.execute("commit;")

def get_number():
	out_label = None
	out_data = None
	unoi_cur = db.cursor()
	unoi_cur.execute("select id, tag_data from inputdata where (ucase(tag_data) like '%INV%NUM%' or ucase(tag_data) like '%INV%NO%') and fname={0};".format(filename))
	demo = unoi_cur.fetchone()
	if demo == None:
		print("Error")
	else:	
		num = None
		for c in demo[1]:
			if c.isdigit():
				num = demo[1].split()
				break

		if num != None:
			out_label = num[0]
			out_data = num[-1]
		else:
			i_cur1 = db.cursor()
			i_cur2 = db.cursor()
			i_cur1.execute("select a.tag_data,b.id,b.top,b.left_mar,b.tag_data from inputdata a, inputdata b where 1=1 and a.fname=b.fname and a.id =" +str(demo[0])+ " and ((b.Left_mar <= a.Left_mar and a.Left_mar <= (b.Left_mar+b.Width) and b.Top >= (a.Top+a.Height) ) or (b.Left_mar >= a.Left_mar and b.Top >= a.Top and (b.Top >= (a.Top+a.Height) and b.Left_mar <= (a.Left_mar+a.Width) ))) order by b.top,b.Left_mar limit 1;")
			i_cur2.execute("select a.tag_data,b.id,b.top,b.left_mar,b.tag_data from inputdata a, inputdata b where 1=1 and a.fname=b.fname and a.id =" +str(demo[0])+ " and ((b.Top <= a.Top and b.Left_mar >= (a.Left_mar+a.Width) and a.Top <= (b.Top+b.Height) ) or (b.Left_mar >= a.Left_mar and b.Top >= a.Top and (b.Top <= (a.Top+a.Height) and b.Left_mar >= (a.Left_mar+a.Width) ))) order by b.Left_mar,b.top limit 1;")
			
			bi_row = i_cur1.fetchone()
			ri_row = i_cur2.fetchone()

			if bi_row == None and ri_row == None:
				print("Error")
			elif bi_row == None:
				out_label = ri_row[0]
				out_data = ri_row[4]
			elif ri_row == None:
				out_label = bi_row[0]
				out_data = bi_row[4]
			else:
				if bi_row[4].isalpha(): 
					out_label = ri_row[0]
					out_data = ri_row[4]
				elif ri_row[4].isalpha():
					out_label = bi_row[0]
					out_data = bi_row[4]
				elif not bi_row[4][-1:].rstrip().isdigit():
					out_label = ri_row[0]
					out_data = ri_row[4]
				elif not ri_row[4][-1:].rstrip().isdigit():
					out_label = bi_row[0]
					out_data = bi_row[4]
				else:
					out_label = bi_row[0]
					out_data = bi_row[4]

	#print(bi_row[0] + " " + num)
	print(out_label + " : " + out_data)
	
def get_date():
	out_label = None
	out_data = None
	unod_cur = db.cursor()
	unod_cur.execute("select id, tag_data from inputdata where (ucase(tag_data) like '%INV%DATE%' or ucase(tag_data) like '%DATE%ISSUE%' or ucase(tag_data) like '%ISSUE%DATE%') and fname={0};".format(filename))
	demo1 = unod_cur.fetchone()
	if demo1 == None:
		unod_cur.execute("select id, tag_data from inputdata where (ucase(tag_data) like 'DATE%') and fname={0};".format(filename))
		demo1 = unod_cur.fetchone()
	if demo1 == None:
		print("Error")
	else:		
		pat1 = re.compile(r'[\d]+-[\d]+-[\d]+')
		pat2 = re.compile(r'[\d]+/[\d]+/[\d]+')
		pat3 = re.compile(r'[\d]+\\[\d]+\\[\d]+')
		pat4 = re.compile(r'[\d]+\s[\w]+\s[\d]+')
		pat5 = re.compile(r'[w]+\s[\d]+\s[\d]+')
		pat6 = re.compile(r'[\d]+-[\w]+-[\d]+')
		pat7 = re.compile(r'[\d]+-[\w]+-[\d]+')

		date = None
		if pat1.search(demo1[1]) != None or pat2.search(demo1[1]) != None or pat3.search(demo1[1]) != None or pat4.search(demo1[1]) != None or pat5.search(demo1[1]) != None or pat6.search(demo1[1]) != None or pat7.search(demo1[1]) != None:
			out_label = demo1[1].split()[0]
			out_data = demo1[1].split()[-1]

		else:	
			d_cur1 = db.cursor()
			d_cur2 = db.cursor()
			d_cur1.execute("select a.tag_data,b.id,b.top,b.left_mar,b.tag_data from inputdata a, inputdata b where 1=1 and a.fname=b.fname and a.id =" +str(demo1[0])+ " and ((b.Left_mar <= a.Left_mar and a.Left_mar <= (b.Left_mar+b.Width) and b.Top >= (a.Top+a.Height) ) or (b.Left_mar >= a.Left_mar and b.Top >= a.Top and (b.Top >= (a.Top+a.Height) and b.Left_mar <= (a.Left_mar+a.Width) ))) order by b.top,b.Left_mar limit 1;")
			d_cur2.execute("select a.tag_data,b.id,b.top,b.left_mar,b.tag_data from inputdata a, inputdata b where 1=1 and a.fname=b.fname and a.id =" +str(demo1[0])+ " and ((b.Top <= a.Top and b.Left_mar >= (a.Left_mar+a.Width) and a.Top <= (b.Top+b.Height) ) or (b.Left_mar >= a.Left_mar and b.Top >= a.Top and (b.Top <= (a.Top+a.Height) and b.Left_mar >= (a.Left_mar+a.Width) ))) order by b.Left_mar,b.top limit 1;")
			bd_row = d_cur1.fetchone()
			rd_row = d_cur2.fetchone()
			
			if bd_row == None and rd_row == None:
				print("Error")
			elif bd_row == None:
				out_label = rd_row[0]
				out_data = rd_row[4]
			elif rd_row == None:
				out_label = bd_row[0]
				out_data = bd_row[4]
			else:		
				if pat1.search(bd_row[4]) == None and pat2.search(bd_row[4]) == None and pat3.search(bd_row[4]) == None and pat4.search(bd_row[4]) == None and pat5.search(bd_row[4]) == None and pat6.search(bd_row[4]) == None and pat7.search(bd_row[4]) == None:
					out_label = rd_row[0]
					out_data = rd_row[4]
				elif pat1.search(rd_row[4]) == None and pat2.search(rd_row[4]) == None and pat3.search(rd_row[4]) == None and pat4.search(rd_row[4]) == None and pat5.search(rd_row[4]) == None and pat6.search(rd_row[4]) == None and pat7.search(rd_row[4]) == None:
					out_label = bd_row[0]
					out_data = bd_row[4]
				else:
					out_label = bd_row[0]
					out_data = bd_row[4]

	#print(bd_row[0] + " " + date)
	print(out_label + " : " + out_data)

def get_amount():
	out_label = None
	out_data = None
	unoa_cur = db.cursor()
	unoa_cur.execute("select id, tag_data from inputdata where (ucase(tag_data) like '%TOTAL%' and ucase(tag_data) not like '%SUB%') and fname={0};".format(filename))
	demo2 = unoa_cur.fetchone()
	if demo2 == None:
		unoa_cur.execute("select id, tag_data from inputdata where (ucase(tag_data) like '%BALANCE%DUE%' or ucase(tag_data) like '%DUE%BALANCE%') and fname={0};".format(filename)) 
	if demo2 == None:
		print("Error")
	else:	
		a_cur1 = db.cursor()
		a_cur2 = db.cursor()
		apat1 = re.compile(r'[\d]+\.[\d]{1,3}')

		if apat1.search(demo2[1]) != None:
			out_label = demo2[1].split()[0]
			out_data = demo2[1].split()[-1]
		else:	
			a_cur1.execute("select a.tag_data,b.id,b.top,b.left_mar,b.tag_data from inputdata a, inputdata b where 1=1 and a.fname=b.fname and a.id =" +str(demo2[0])+ " and ((b.Left_mar <= a.Left_mar and a.Left_mar <= (b.Left_mar+b.Width) and b.Top >= (a.Top+a.Height) ) or (b.Left_mar >= a.Left_mar and b.Top >= a.Top and (b.Top >= (a.Top+a.Height) and b.Left_mar <= (a.Left_mar+a.Width) ))) order by b.top,b.Left_mar limit 1;")
			a_cur2.execute("select a.tag_data,b.id,b.top,b.left_mar,b.tag_data from inputdata a, inputdata b where 1=1 and a.fname=b.fname and a.id =" +str(demo2[0])+ " and ((b.Top <= a.Top and b.Left_mar >= (a.Left_mar+a.Width) and a.Top <= (b.Top+b.Height) ) or (b.Left_mar >= a.Left_mar and b.Top >= a.Top and (b.Top <= (a.Top+a.Height) and b.Left_mar >= (a.Left_mar+a.Width) ))) order by b.Left_mar,b.top limit 1;")
			ba_row = a_cur1.fetchone()
			ra_row = a_cur2.fetchone()
			if ba_row == None and ra_row == None:
				print("Error")
			elif ba_row == None:
				out_label = ra_row[0]
				out_data = ra_row[4]
			elif ra_row == None:
				out_label = ba_row[0]
				out_data = ba_row[4]
			else:			
				if apat1.search(ba_row[4]) == None:
						out_label = ra_row[0]
						out_data = ra_row[4]
				elif apat1.search(ra_row[4]) == None:
						out_label = ba_row[0]
						out_data = ba_row[4]
				else:
					out_label = ba_row[0]
					out_data = ba_row[4]		

	#print(ba_row[0] + " " + amt)
	print(out_label + " : " + out_data)

get_number()
get_date()
get_amount()
db.close()		
