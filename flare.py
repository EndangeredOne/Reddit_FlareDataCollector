import praw, sys, decimal

reddit=praw.Reddit("praw_info")
sub=reddit.subreddit("politicalcompassmemes")

def getSubComments(comment, allComments, verbose=True):
  allComments.append(comment)
  if not hasattr(comment, "replies"):
    replies=comment.comments()
    if verbose: print("fetching ("+str(len(allComments))+" comments fetched total)")
  else:
    replies=comment.replies
  for child in replies:
    getSubComments(child, allComments, verbose=verbose)


def getAll(r, post, verbose=True):
  post.comments.replace_more(limit=None)
  commentsList=[]
  for comment in post.comments:
    getSubComments(comment, commentsList, verbose=verbose)
  return commentsList
  

class Quadrant:
	def __init__(self, label, flair):
		self.Label=label
		self.Flair=flair
		self.Posts=0
		self.PostKarma=0
		self.Comments=0
		self.CommentKarma=0
		self.UniqueMembers=0

quadrantList=[Quadrant("AuthLeft",":authleft: - AuthLeft"),
			Quadrant("AuthCenter",":auth: - AuthCenter"),
			Quadrant("AuthRight",":authright: - AuthRight"),
			Quadrant("Left",":left: - Left"),
			Quadrant("Centrist",":centrist: - Centrist"),
			Quadrant("Right",":right: - Right"),
			Quadrant("LibLeft",":libleft: - LibLeft"),
			Quadrant("LibCenter",":lib: - LibCenter"),
			Quadrant("Yellow LibRight",":libright: - LibRight"),
			Quadrant("Purple LibRight",":libright2: - LibRight"),
			Quadrant("Unflaired","")]

encounteredUsernames=[]

postsScanned=0
commentsScanned=0

for post in sub.new(limit=10000):
	postsScanned+=1
	for quad in quadrantList:
		if post.author_flair_text==quad.Flair:
			quad.Posts+=1
			quad.PostKarma+=post.score
			if post.author.name not in encounteredUsernames:
				encounteredUsernames.append(post.author.name)
				quad.UniqueMembers+=1
			break
	for comment in getAll(reddit, post):
		commentsScanned+=1
		for quad in quadrantList:
			if comment.author_flair_text==quad.Flair:
				quad.Comments+=1
				quad.CommentKarma+=comment.score
				if comment.author.name not in encounteredUsernames:
					encounteredUsernames.append(comment.author.name)
					quad.UniqueMembers+=1
				break
	sys.stdout.write("\rPosts scanned: "+str(postsScanned)+", comments scanned: "+str(commentsScanned))
	sys.stdout.flush()

decimal.getcontext().prec=10
for quad in quadrantList:
	print("")
	print(quad.Label+":")
	print(str(quad.UniqueMembers)+" unique users found")
	print(str(quad.Posts)+" posts found, with "+str(quad.PostKarma)+" total points, avg "
		+str(decimal.Decimal(quad.PostKarma)/decimal.Decimal(max(quad.Posts,1))))
	print(str(quad.Comments)+" comments found, with "+str(quad.CommentKarma)+" total points, avg "+str(decimal.Decimal(quad.CommentKarma)/decimal.Decimal(max(quad.Comments,1))))
	
	
input()