import praw

if __name__ == "__main__":
	posts = open('posts.txt', 'r')
	lines = posts.readlines()
	for line in lines:
		line = line.decode('utf-8').rstrip('\n')
		route_syntax = ['5.', ' V', '(V', ' v', '(v']
		is_route = False
		for syntax in route_syntax:
			index = line.find(syntax)
			if index != -1:
				if route_syntax.index(syntax) > 0 :
					if index + 2 < len(line):
						if line[index + 2:index + 3].isdigit():
							is_route = True
							print '__label__1 ' + line.encode("utf8")
				else:
					is_route = True
					print '__label__1 ' + line.encode("utf8")
				break

		if not is_route: print '__label__2 ' + line.encode("utf8")



