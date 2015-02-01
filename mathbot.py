import json
import praw
import sqlite3

userAgent = "/u/simple_math_bot python reddit mathBot"
userName = "username"
password = "password"
subredditName = "umw_cpsc470Z"
magicPhrase = ["add", "subtract", "multiply", "divide"]
magicPhrase1 = ["math"]

sql = sqlite3.connect("sql.db")
cursor = sql.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)")
sql.commit()

print("logging in to reddit")
r = praw.Reddit(userAgent)
r.login("username", "password")

def mathBot():
        print("Fetching subreddit" + subredditName)
        subreddit = r.get_subreddit(subredditName)
        print("Fetching comments")
        comments = subreddit.get_comments(limit=10)
        for comment in comments:
                cursor.execute('SELECT * FROM oldposts WHERE ID=?', [comment.id])
                if not cursor.fetchone():
                        try:
                                cbody = comment.body.lower()
                                cauthor = comment.author.name
                                if cauthor.lower() != userName.lower():
                                        if any(key.lower() in cbody for key in magicPhrase1):
                                                print("replying to cauthor")
                                                if any(key.lower() in cbody for key in magicPhrase1):
                                                        comment_words = cbody.split()
                                                        numbers = []
                                                        operator = ""
                                                        for word in comment_words:
                                                                if word != "math" and word not in magicPhrase:
                                                                        numbers.append(int(word))
                                                                if word in magicPhrase:
                                                                        operator = word
                                                        total = 0
                                                        for number in numbers:
                                                                if operator == "add":
                                                                        total = total + number
                                                                elif operator == "subtract":
                                                                        if total == 0:
                                                                                total = number
                                                                        else:
                                                                                total = total - number
                                                                elif operator == "multiply":
                                                                        if total == 0:
                                                                                total = 1 * number
                                                                        else:
                                                                                total = total * number
                                                                elif operator == "divide":
                                                                        if total == 0:
                                                                                total = number
                                                                        else:
                                                                                total = total / number
                                                        comment.reply("Your answer is %d" % total)
                                                        #comment.reply(result)
                        except AttributeError:
                                pass
                        cursor.execute("INSERT INTO oldposts VALUES(?)", [comment.id])
                        sql.commit()

while True:
        mathBot()
