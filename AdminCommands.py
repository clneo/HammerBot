#AdminComamnds.py
import sys
import datetime, time

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def consolelog(name, content, db):
	print("User: " + name + " ran command: " + content + " at: " + st)

def exitbot(client, message, db):
	cur = db.cursor()
	client.send_message(message.channel, 'Discord Bot Stopping')
	consolelog(message.author.name, str(message.content))
	sys.exit(0)

def word(client, message, db):
	cur = db.cursor()
	commandline = str(message.content).split(" ")
	print commandline[1]
	if commandline[1] == "list":
		cur.execute("SELECT * FROM links")
		rows = cur.fetchall()
		keywords = []
		for i in rows:
			keywords.append(str(i[0]))
		keywords = str(', '.join(keywords))
		client.send_message(message.channel, keywords )
		return()
	if commandline[1] == "add":
		print("Attempting to add: " + commandline[2] + " To URL: " + commandline[3])
		try:
			cur.execute('''INSERT INTO links (word,url) VALUES (?,?)''', (commandline[2], commandline[3]))
			db.commit()
			client.send_message(message.channel, "Adding Keyword: " + commandline[2])
			print("User: " + message.author.name + "Added keyword: " + commandline[2] + " That has URL: " + commandline[3] + " At: " + str(st))
		except:
			client.send_message(message.channel, 'Unable to add keyword: %s' % commandline[2])
		return()
	if commandline[1] == "remove":
		cur.execute("SELECT * FROM links")
		rows = cur.fetchall()
		keywords = []
		for i in rows:
			keywords.append(str(i[0]))
			if commandline[2] in keywords:
				try:
					client.send_message(message.channel, "Deleting Keyword: " + commandline[2])
					print("User: " + message.author.name + "Deleted keyword: " + commandline[2] + " At: " + str(st))
					cur.execute("DELETE FROM links WHERE word = ?", (commandline[2],))
					db.commit()
				except:
					client.send_message(message.channel, 'Unable to delete keyword: %s' % commandline[2])
			else:
				client.send_message(message.channel, "Keyword %s not found." % commandline[2])
		return()
	if commandline[1] == "help":
		client.send_message(message.channel, "Word command usage:")
		client.send_message(message.channel, "Command: !word list  -Lists all active keywords-")
		client.send_message(message.channel, "Command: !word add <keyword> <url>  -Adds a keyword-")
		client.send_message(message.channel, "Command: !word remove <keyword>  -Removes a keyword-")
		return()
	else:
		client.send_message(message.channel, "SubCommand %s not found in command !word" % commandline[1]) 
	
adminStrings = {'!exit': exitbot, '!word': word}
