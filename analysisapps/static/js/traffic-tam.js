// set session storage variable for variable
function set_session_var(s1){
    var s1 = document.getElementById(s1);
    localStorage.setItem(s1.id+'_key', s1.value);
}

// Show hidden div
function show_category_div(s1, s2){
    var s1 = document.getElementById(s1);
    var s2 = document.getElementById(s2);
    localStorage.setItem(s1.id+'_key', s1.value);
    if (s1.value == 'map'){
        s2.style.display = 'block';
    }
    else if (s1.value == 'table') {
        s2.style.display = 'none';
    }
}