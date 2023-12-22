/**
 * Sign up function
 */
function signUp() {
    event.preventDefault();
    // package data in a JSON object
    var data_d = {'email' : document.getElementById("email_signup").value, 'password': document.getElementById("password").value};
    console.log('data_d', data_d);

    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/process_signup",
        data: data_d,
        type: "POST",
        success:function(returned_data){
              returned_data = JSON.parse(returned_data);
              if (returned_data.status === '1'){
                // sign up was successful
                window.location.href = "/login";
              }
              else{
                // Sign up wasnt successful
                const para = document.querySelector('.wrong_signup_box');
                para.style.display = "flex"; 
            }
        }
    });
}


let count = 0;
function checkCredentials() {
    // package data in a JSON object
    var data_d = {'email' : document.getElementById("email_login").value, 'password': document.getElementById("password").value};
    console.log('data_d', data_d);

    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/processlogin",
        data: data_d,
        type: "POST",
        success:function(returned_data){
              returned_data = JSON.parse(returned_data);
              if (returned_data.status === '1'){
                window.location.href = "/home";
              }
              else{
                count += 1;
                const para = document.querySelector('.wrong_login_box');
                para.innerHTML = "Authentication Failure: " + count;
                para.style.display = "flex"; 
            }
        }
    });
}