#!/usr/bin/python3
from flask import Flask, request, redirect, url_for, render_template as renderTemp

# make app from class using __name__ special variable
app = Flask(__name__)

class link:
	def __init__(self, title, url):
		self.title, self.url = title, url

class headerLink:
	def __init__(self, title, url, dropdown = False):
		self.title, self.url, self.dropdown = title, url, dropdown

class post:
	def __init__(self, title, description, date, thumbnail):
		# thumbnail is a "link" class object
		self.title, self.description, self.date, self.thumbnail = title, description, date, thumbnail

headerContent = [
	headerLink("Home", "/"),
	headerLink("Projects", "/projects", True),
	headerLink("About", "/about"),
	headerLink("Contact", "/contact"),
	headerLink("Post", "/post")
]

projectsPosts = [
	post(
		link("Post 1 title", "first-post.html"),
		"First post! increadible, to be honest.",
		"April 4/15/2019", 
		link("nebula", "/static/nebula-y.jpg")),
	post(
		link("Post 1 title", "first-post.html"),
		"First post! increadible, to be honest.",
		"April 4/15/2019", 
		link("nebula", "/static/nebula-y.jpg")),
	post(
		link("Second post", "second-post.html"), 
		"Getting old", 
		"April 5/15/2019", 
		link("sandcastle", "/static/sandcastle.png"))
]


def currentPath():
	return request.path.split("/")[-1].capitalize()

def getAddCont():
	global headerContent
	additionalContent = {
		"mainTitle": currentPath(),
		"curPage": currentPath(),
		"headerContent": headerContent
	}
	return additionalContent

@app.route("/", methods = ["GET", "POST"])
def rootDir():
	if request.method == "POST":
		for i in range(28):
			if request.form["GPIO"] == str(i):
				pass

	return redirect(url_for("home"))

@app.route("/home")
def home():
	return renderTemp("home.html", **getAddCont())

@app.route("/home/<page>")
def homeIndex(page):
	if page == "control":
		return renderTemp("control.html", **getAddCont())
	else:
		return redirect(url_for("home"))

@app.route("/projects")
def projects():
	return renderTemp("projects.html", posts = projectsPosts, **getAddCont())

@app.route("/about")
def about():
	return renderTemp("about.html", **getAddCont())

@app.route("/contact")
def contact():
	return renderTemp("contact.html", **getAddCont())

@app.route("/post")
def postPost():
	return renderTemp("newpost.html", **getAddCont())

# __name__ special var (will be __main__ if started on it's own, else if it was started from a program it will be programname.py)
if __name__ == "__main__":
	app.run(debug = True, port = 23085)

