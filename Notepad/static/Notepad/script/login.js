var flag = 0
function coverit() {
    if (flag == 0) {
		document.getElementById("login-container").style.height = "70vh";
        document.getElementById("signup-form").style.width = "90%";
        function create_timeout() {
            document.getElementById("cover").style.display = "none";
        }
        document.getElementById("cover").style.opacity = "0";
        setTimeout(create_timeout, 1000);
        document.getElementById("change-btn").innerHTML = "از قبل حساب دارم";
        flag = 1
    }
    else {
		document.getElementById("login-container").style.height = "55vh";
        document.getElementById("signup-form").style.width = "10%";
        document.getElementById("cover").style.display = "block";
        document.getElementById("cover").style.opacity = "1";
        document.getElementById("change-btn").innerHTML = "ایجاد حساب جدید";
        flag = 0
    }  
}

const request = new Request (
	window.location.href,
	{headers: {
		'X-CSRFToken': csrf
	}}
);

function login() {
	let data = {
		action: 'login',
		username: document.getElementById('login-name').value,
		password: document.getElementById('login-password').value,
	}
	fetch(request, {
		method: 'POST',
		mode: 'same-origin',
		body:  JSON.stringify(data)
	})
	.then(function(response){
		if (response.status != 200){
			console.log("Hah, Error?")
		}
		else {
			response.json().then(data => {
				if (data['res'] == 'True') {
					console.log("True response :)")
				}
				else {
					console.log("False :(")
				}
			});
		}
	})
	.catch(error => console.log("Hah", error));
}

function login() {
	let data = {
		action: 'login',
		username: document.getElementById('login-name').value,
		password: document.getElementById('login-password').value,
	}
	fetch(request, {
		method: 'POST',
		mode: 'same-origin',
		body:  JSON.stringify(data)
	})
	.then(function(response){
		if (response.status != 200){
			console.log("Hah, Error?")
		}
		else {
			response.json().then(data => {
				if (data['res'] == 'True') {
					let my_url = "http://".concat(window.location.hostname)
					window.location.replace(my_url);
				}
				else {
					alert("False :(")
				}
			});
		}
	})
	.catch(error => console.log("Hah", error));
}

function logout() {
	let data = {
		action: 'logout',
	}
	fetch(request, {
		method: 'POST',
		mode: 'same-origin',
		body:  JSON.stringify(data)
	})
	.then(function(response){
		if (response.status != 200){
			alert("Hah, Error?")
		}
		else {
			response.json().then(data => {
				if (data['res'] == 'True') {
					document.getElementById("loged-in-container").style.display = "none";
					document.getElementById("login-container").style.display = "block";
				}
				else {
					alert("False :(")
				}
			});
		}
	})
	.catch(error => console.log("Hah", error));
}

function sign_up() {
	let data = {
		action: 'signup',
		username: document.getElementById('signup-name').value,
		password: document.getElementById('signup-password').value,
		email: document.getElementById('signup-email').value,
	}
	if (data['password'] != document.getElementById('again-password').value){
		alert("use same passwords");
		return 0;
	}
	fetch(request, {
		method: 'POST',
		mode: 'same-origin',
		body:  JSON.stringify(data)
	})
	.then(function(response){
		if (response.status != 200){
			alert("Hah, Error?")
		}
		else {
			response.json().then(data => {
				if (data['res'] == 'True') {
					let my_url = "http://".concat(window.location.hostname)
					window.location.replace(my_url);
				}
				else {
					alert("False :(", response)
				}
			});
		}
	})
	.catch(error => console.log("Hah", error));
}