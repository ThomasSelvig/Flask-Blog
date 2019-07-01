from flask import Flask, request, jsonify
from datetime import datetime
try:
	from gpiozero import LED
except:
	print("Failed import of gpiozero")

app = Flask(__name__)

def verify(req):
	if "trust" in req:
		if req["trust"] == datetime.now().strftime("%H%d"):
			# req["trust"] = hour0-23 + month1-31
			return True
	return False

def formulateReply(req):
	out = ""
	for key, value in req.items():
		if not key == "trust":
			try:
				state = "HIGH" if bool(int(value)) else "LOW"
			except Exception as e:
				state = "LOW:errorSettingBoolean:" + str(e)

			try:
				LED(int(key)).on() if bool(int(value)) else LED(17).off()
				out += "Set GPIO:" + str(key) + " to " + state
				out += "\n"
			except Exception as e:
				print("Error setting GPIO:", str(e))
				out += "Error setting GPIO:" + str(key) + " to " + state
				out += "\n - Error Message: " + str(e) + "\n"

	return out


def handle():
	req = request.args

	if request.remote_addr == "127.0.0.1":
		return formulateReply(req)

	if not verify(req):
		return "Denied"
	else:
		return formulateReply(req)

@app.route("/", methods=["GET", "POST"])
def rootDir():
	return handle()

if __name__ == "__main__":
	app.run(debug = True, port = 23085, host="0.0.0.0")
