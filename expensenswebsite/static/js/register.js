const usernameField = document.querySelector('#usernameField')
const usernameFeedBackArea = document.querySelector('#username_invalid_feedback')

const emailField = document.querySelector('#emailField')
const emailFeedBackArea = document.querySelector('#email_invalid_feedback')

const usernameSuccess = document.querySelector('#usernameSuccess')
const emailSuccess = document.querySelector('#emailSuccess')

const showPasswordToggle = document.querySelector('.showPasswordToggle')
const passwordField = document.querySelector('#passwordField')


const handleToggleInput = (e) => {
    if(showPasswordToggle.textContent === 'SHOW'){
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    }
    else{
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }
}

showPasswordToggle.addEventListener('click', handleToggleInput)

emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value;
    emailSuccess.style.display = 'block';

    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";

    emailSuccess.textContent = `Checking ${emailVal}`

    if (emailVal.length > 0) {
        fetch("/authentication/validate-email", {
            body: JSON.stringify({ email: emailVal }),
            method: 'POST',
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                emailSuccess.style.display = 'none'
                if (data.email_error) {
                    emailField.classList.add("is-invalid");
                    emailFeedBackArea.style.display = "block";
                    emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`
                }
            });
    }
});


usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;
    usernameSuccess.style.display = 'block';

    usernameField.classList.remove("is-invalid");
    usernameFeedBackArea.style.display = "none";

    usernameSuccess.textContent = `Checking ${usernameVal}`

    if(usernameVal.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({username: usernameVal}),
            method: 'POST',
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data);
            usernameSuccess.style.display = 'none'
            if(data.username_error){
                usernameField.classList.add("is-invalid");
                usernameFeedBackArea.style.display = "block";
                usernameFeedBackArea.innerHTML = `<p>${data.username_error}</p>`
            }
        }); 
    }
});