var age_slider = document.getElementById("ageSlider");
var age_output = document.getElementById("ageTextBox");
age_output.innerHTML = age_slider.value; // Display the default slider value
// Update the current slider value (each time you drag the slider handle)
age_slider.oninput = function() {
  age_output.innerHTML = this.value;
}



var gender_slider = document.getElementById("genderSlider");
var gender_output = document.getElementById("genderTextBox");
gender_output.innerHTML = gender_slider.value; // Display the default slider value
// Update the current slider value (each time you drag the slider handle)
gender_slider.oninput = function() {
  gender_output.innerHTML = this.value;
}



var hobby_slider = document.getElementById("hobbySlider");
var hobby_output = document.getElementById("hobbyTextBox");
hobby_output.innerHTML = hobby_slider.value; // Display the default slider value
// Update the current slider value (each time you drag the slider handle)
hobby_slider.oninput = function() {
  hobby_output.innerHTML = this.value;
}



var interest_slider = document.getElementById("interestSlider");
var interest_output = document.getElementById("interestTextBox");
interest_output.innerHTML = interest_slider.value; // Display the default slider value
// Update the current slider value (each time you drag the slider handle)
interest_slider.oninput = function() {
  interest_output.innerHTML = this.value;
}
