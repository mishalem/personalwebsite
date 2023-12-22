// Author: Mikhail Lemper

//Gets add entry and stores it in add_entry
const add_entry = document.getElementById('add_entry');
//Adds event listener to add_entry
add_entry.addEventListener('click', displayEntryForm);

/**
 * Displays entry form if button was pressed and hides it if it was pressed again
 */
function displayEntryForm(){
    const entry_form = document.querySelector(".entryForm");
    if (entry_form.style.display === "table-row"){
        entry_form.style.display = "none"; 
    }
    else {
        entry_form.style.display = "table-row"; 
    }
}


/**
 * Saves changes made taht were made to the resume
 */
function SaveChanges() {
    //Updates the name
    $('input[id^="name_"]').each(function() {
        var inst_id = $(this).attr('id').split('_')[1];
        var name = $(this).val();
        data_d = {'inst_id' : inst_id, 'name' : name};
                jQuery.ajax({
                url: "/update_name",
                data: data_d,
                type: "POST",   
                async: false,  
                    success: function(response) {
                }
            });
        });
    //Updates the department
    $('input[id^="department_"]').each(function() {
        var inst_id = $(this).attr('id').split('_')[1];
        var department = $(this).val();
        data_d = {'inst_id' : inst_id, 'department' : department};
                jQuery.ajax({
                url: "/update_department",
                data: data_d,
                type: "POST",  
                async: false,   
                    success: function(response) {
                }
            });
        });
    //Updates the address 
    $('input[id^="address_"]').each(function() {
        var inst_id = $(this).attr('id').split('_')[1];
        var address = $(this).val();
        data_d = {'inst_id' : inst_id, 'address' : address};
                jQuery.ajax({
                url: "/update_address",
                data: data_d,
                type: "POST", 
                async: false,    
                    success: function(response) {
                }
            });
        });
    //Updates the city    
    $('input[id^="city_"]').each(function() {
        var inst_id = $(this).attr('id').split('_')[1];
        var city = $(this).val();
        data_d = {'inst_id' : inst_id, 'city' : city};
                jQuery.ajax({
                url: "/update_city",
                data: data_d,
                type: "POST",  
                async: false,   
                    success: function(response) {
                }
            });
        });
    //Updates the title
    $('input[id^="title_"]').each(function() {
        var pos_id = $(this).attr('id').split('_')[1];
        var title = $(this).val();
        data_d = {'pos_id' : pos_id, 'title' : title};
                jQuery.ajax({
                url: "/update_title",
                data: data_d,
                type: "POST",
                async: false,     
                    success: function(response) {
                }
            });
        });
    //Updates the start date
    $('input[id^="startdate_"]').each(function() {
        var pos_id = $(this).attr('id').split('_')[1];
        var start_date = $(this).val();
        data_d = {'pos_id' : pos_id, 'start_date' : start_date};
                jQuery.ajax({
                url: "/update_start_date",
                data: data_d,
                type: "POST", 
                async: false,    
                    success: function(response) {
                }
            });
        });
     
    //Updates the end date
    $('input[id^="enddate_"]').each(function() {
        var pos_id = $(this).attr('id').split('_')[1];
        var end_date = $(this).val();
        data_d = {'pos_id' : pos_id, 'end_date' : end_date};
                jQuery.ajax({
                url: "/update_end_date",
                data: data_d,
                type: "POST", 
                async: false,    
                    success: function(response) {
                }
            });
        });

    //Updates the skills
    $('input[id^="skills_"]').each(function() {
        var skill_id = $(this).attr('id').split('_')[1];
        var skills = $(this).val();
        data_d = {'skill_id' : skill_id, 'skills' : skills};
                jQuery.ajax({
                url: "/update_skills",
                data: data_d,
                type: "POST",    
                async: false, 
                    success: function(response) {
                }
            });
        });

    //Updates the experience name
    $('input[id^="expname_"]').each(function() {
        var exp_id = $(this).attr('id').split('_')[1];
        var expname = $(this).val();
        data_d = {'exp_id' : exp_id, 'expname' : expname};
                jQuery.ajax({
                url: "/update_expname",
                data: data_d,
                type: "POST",   
                async: false,  
                    success: function(response) {
                }
            });
        });
    //Updates the description
    $('input[id^="description_"]').each(function() {
        var exp_id = $(this).attr('id').split('_')[1];
        var description = $(this).val();
        data_d = {'exp_id' : exp_id, 'description' : description};
                jQuery.ajax({
                url: "/update_description",
                data: data_d,
                type: "POST", 
                async: false,   
                    success: function(response) {
                }
            });
        });
    window.location.href = "/resume";
}