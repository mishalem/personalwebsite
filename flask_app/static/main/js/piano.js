//Author: Mikhail Lemper

//Initialize weeseeyou to empty string
weeseeyou = "";
//Gets menu bar and stores it in para
const para = document.querySelector('.menu_bar');
//Adds event listener to para
para.addEventListener('click', displayMenuBar);
//Sets boolean whther its end of piano to true
end_of_piano = true;
//Adds event listener to document
document.addEventListener("keydown", keyEvent);
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
 * Event for every key pressed 
 */
function keyEvent (event){
    if (event.keyCode === 65 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav");
        audio.play();
        weeseeyou = "";
    }
    else if (event.keyCode === 87 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav");
        audio.play();
        weeseeyou = "w";
        const w = document.querySelector("#W");
        // w.style.backgroundColor = "orange";
        // w.style.backgroundColor = "black";
        // w.classList.toggle("pressed")

    }
    else if (event.keyCode === 83  && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav");
        audio.play();
        if (weeseeyou === "we"){
            weeseeyou += "s";
        }
        else{
            weeseeyou = "";
        }
    }
    else if (event.keyCode === 69 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav");
        audio.play();
        if (weeseeyou === "w" || weeseeyou === "wes" || weeseeyou === "wese"){
            weeseeyou += "e";
        }
        else{
            weeseeyou = "";
        }
    }
    else if (event.keyCode === 68 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav");
        audio.play();
        weeseeyou = "";
    }
    else if (event.keyCode === 70 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav");
        audio.play();
        weeseeyou = "";
    }
    else if (event.keyCode === 84 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav");
        audio.play();
        weeseeyou = "";
    }
    else if (event.keyCode === 71 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav");
        audio.play();
        weeseeyou = "";
    }
    else if (event.keyCode === 89 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav");
        audio.play();
        if (weeseeyou === "wesee"){
            weeseeyou += "y";
        }
        else{
            weeseeyou="";
        }
    }
    else if (event.keyCode === 72 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav");
        audio.play();
        weeseeyou = "";
    }
    else if (event.keyCode === 85 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav");
        audio.play();
        if (weeseeyou === "weseeyo"){
            weeseeyou += "u";
        }
        else{
            weeseeyou = "";
        }
    }
    else if (event.keyCode === 74 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav");
        audio.play();
        weeseeyou = "";
    }
    else if (event.keyCode === 75 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav");
        audio.play();
        weeseeyou = "";
    }
    else if (event.keyCode === 79 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav");
        audio.play();
        if (weeseeyou === "weseey"){
            weeseeyou += "o";
        }
        else{
            weeseeyou = "";
        }
    }
    else if (event.keyCode === 76 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav");
        audio.play();
        weeseeyou = "";
    }
    else if (event.keyCode === 80 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav");
        audio.play();
        weeseeyou = "";
    }
    else if (event.keyCode === 186 && end_of_piano){
        const audio = new Audio("http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav");
        audio.play();
        weeseeyou = "";
    }
    if (weeseeyou === "weseeyou" && end_of_piano){
        const audio = new Audio("https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1");
        audio.play(); 
        const old_one = document.querySelector(".old_one");
        const piano = document.querySelector(".piano");
        const awoken = document.querySelector(".awoken");
        old_one.style.display = "block";
        // piano.style.display = "none";
        old_one.style.opacity = "1";
        piano.style.opacity = '0';
        // old_one.style.display = "flex";
        awoken.style.display = "block";
        end_of_piano = false;
        weeseeyou = "";
    }
}