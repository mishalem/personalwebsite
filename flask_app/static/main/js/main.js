// Author: Mikhail Lemper

//Gets menu bar and stores it in para
const para = document.querySelector('.menu_bar');
//Adds event listener to para
para.addEventListener('click', displayMenuBar);
//Gets feedback and stores it in feedback
const feedback = document.querySelector('.feedback');
//Adds event listener to feedback
feedback.addEventListener('click', displayFeedbackForm);
/**
 * Displays menu bar
 */
function displayMenuBar() {
    const vertical_wrapper = document.querySelector(".vertical_wrapper");
    if (vertical_wrapper.style.display === "flex"){
        vertical_wrapper.style.display = "none"; 
    }
    else {
        vertical_wrapper.style.display = "flex"; 
    }

}
/**
 * Dispalys feedback form
 */
function displayFeedbackForm() {
    const feedbackForm = document.querySelector(".feedbackForm");
    if (feedbackForm.style.display === "block"){
        feedbackForm.style.display = "none";
    }
    else{
    feedbackForm.style.display = "block";
    }
}
