// function to populate table drop down based on tract or blockgroup selected
function populate_tables(s1,s2,s3,s4,s5){
    var s1 = document.getElementById(s1);
    var s2 = document.getElementById(s2);
    var s3 = document.getElementById(s3);
    var s4 = document.getElementById(s4);
    var s5 = document.getElementById(s5);

    var vals = [s2,s3,s4,s5];
    for (v in vals) {
        vals[v].value = '';
        vals[v].innerHTML = '';
    }

    localStorage.setItem(s1.id+'_key', s1.value);

    // set session storage variable for tract-block group, remove all others when changed
    if (s1.value == null | s1.value == '') {
        for (v in vals) {
            localStorage.removeItem(vals[v].id + '_key')
        }
        localStorage.removeItem('col_ind_key_html');
        localStorage.removeItem('col_dep_key_html');
        localStorage.removeItem('col_ind_key_list');
        localStorage.removeItem('col_dep_key_list');
        localStorage.removeItem('col_ind_key_list_html');
        localStorage.removeItem('col_dep_key_list_html');
    }

    // assign table drop down items by tract or block group selection
    if(s1.value == 'tract'){
        var optionArray = [
            '|Select a table...',
            'dp04|DP04 - Selected Housing Characteristics',
            'dp05|DP05 - ACS Demographic and Housing Estimates',
            // 's0802|S0802 - Means of Transportation to Work by Selected Characteristics',
            // 's1501|S1501 - Educational Attainment', 's1701|S1701 - Poverty Status in the Past 12 Months',
            // 's1810|S1810 - Disability Characteristics', 's1901|S1901 - Income in the Past 12 Months'
    ];
    } else if(s1.value == 'blockgroup'){
        var optionArray = ['|Select a table...', 'b01001|B01001 - Sex by Age', 'b03002|B03002 - Hispanic or Latino Origin by Race',
        'b08134|B08134 - Means of Transportation to Work by Travel Time',
        'b15002|B15002 - Sex by Educational Attainment for the Population 25 Years and Over',
        'b17017|B17017 - Poverty Status in the Past 12 Months by Household Type by Age of Householder',
        'b19001|B19001 - Household Income in the Past 12 Months',
        'b25008|B25008 - Total Population in Occupied Housing Unites by Tenure', 'b25034|B25034 - Year Structure Built',
        'b25075|B25075 - House Value', 'c17002|C17002 - Ratio of Income to Poverty Level in the Past 12 Months',
        'c21007|C21007 - Age by Veteran Status by Disability Status'];
    }

    // run for loop to assign the value and label
    for(var option in optionArray) {
        var pair = optionArray[option].split('|');
        var newOption = document.createElement('option');
        newOption.value = pair[0];
        newOption.innerHTML = pair[1];
        s2.options.add(newOption);
    }

    for(var option in optionArray) {
        var pair = optionArray[option].split('|');
        var newOption = document.createElement('option');
        newOption.value = pair[0];
        newOption.innerHTML = pair[1];
        s4.options.add(newOption);
    }

    // reset the variable drop downs to blank if tr_bg changed after
    if(s1.value == ''){
        var newOption = document.createElement('option')
        newOption.value = '';
        newOption.innerHTML = '';
        s4.options.add(newOption);
        s5.options.add(newOption);
        }
}

//function to populate category drop down based on variable selected
function populate_cat(s1,s2,s3,s4){
    var s1 = document.getElementById(s1);
    var s2 = document.getElementById(s2);
    var s3 = document.getElementById(s3);

    // Reset values if previous drop down is blank
    if (s1.value == '') {
        s2.innerHTML = '';
        var newOption = document.createElement('option')
        newOption.value = '';
        newOption.innerHTML = '';
        s2.options.add(newOption);
        localStorage.removeItem(s2.id + '_key')
        localStorage.removeItem(s2.id + '_key_list')
        
        s3.innerHTML = '';
        s3.options.add(newOption);
        localStorage.removeItem(s3.id + '_key')
        localStorage.removeItem(s3.id + '_key_list')
    }
    else {
        s2.innerHTML = '';
        var newOption = document.createElement('option')
        newOption.value = '';
        newOption.innerHTML = 'Select a category...';
        s2.options.add(newOption);
        localStorage.removeItem(s2.id + '_key')
        localStorage.removeItem(s2.id + '_key_list')
    }

    // set session storage variable for table
    localStorage.setItem(s1.id+'_key', s1.value);

    // Add options to category drop down
    var cat_sesh_var = [];
    var cat_sesh_html = [];
    var selected_table = s1.value.toUpperCase();
    var data = JSON.parse(s4)
    var cats = []
    for (var option in data) {
        if (data[option]['group']==selected_table) {
            var showtext = data[option]['label'].substring(9,);
            showtext = showtext.substring(0,showtext.indexOf('!!'));
            if (cats.includes(showtext)==false && showtext!=='') {
                cats.push(showtext);
            }
        }
    }
    cats.sort();

    for (var cat in cats) {
        var newOption = document.createElement('option');
        newOption.value = cats[cat];
        newOption.innerHTML = cats[cat];
        s2.options.add(newOption);
        cat_sesh_var.push(data[option]['name']);
        cat_sesh_html.push(data[option]['label'].substring(9,));
    }
    localStorage.setItem(s2.id+'_key_list', cat_sesh_var.join("`"));
    localStorage.setItem(s2.id+'_key_list_html', cat_sesh_html.join("`"));
}

//function to populate variable drop down based on category selected
function populate_var(s1,s2,s3){
    var s1 = document.getElementById(s1);
    var s2 = document.getElementById(s2);

    // Reset values if previous drop down is blank
    if (s1.value == '') {
        s2.innerHTML = '';
        var newOption = document.createElement('option')
        newOption.value = '';
        newOption.innerHTML = '';
        s2.options.add(newOption);
        localStorage.removeItem(s2.id + '_key')
        localStorage.removeItem(s2.id + '_key_list')
    }
    else {
        s2.innerHTML = '';
        var newOption = document.createElement('option')
        newOption.value = '';
        newOption.innerHTML = 'Select a category...';
        s2.options.add(newOption);
        localStorage.removeItem(s2.id + '_key')
        localStorage.removeItem(s2.id + '_key_list')
    }

    // set session storage variable for table
    localStorage.setItem(s1.id+'_key', s1.value);

    // Add options to column drop down
    var var_sesh_var = [];
    var var_sesh_html = [];
    var selected_table = s1.value.toUpperCase();
    var data = JSON.parse(s3)
    for (var option in data) {

        if (data[option]['group']==selected_table) {
            var newOption = document.createElement('option');
            newOption.value = data[option]['name'];
            newOption.innerHTML = data[option]['label'].substring(9,);
            s2.options.add(newOption);
            var_sesh_var.push(data[option]['name']);
            var_sesh_html.push(data[option]['label'].substring(9,));

        }
    }
    localStorage.setItem(s2.id+'_key_list', var_sesh_var.join("`"));
    localStorage.setItem(s2.id+'_key_list_html', var_sesh_html.join("`"));


}

// set session storage variable for variable
function set_session_var(s1){
    var s1 = document.getElementById(s1);
    localStorage.setItem(s1.id+'_key', s1.value);
    localStorage.setItem(s1.id+'_key_html', s1.options[s1.selectedIndex].text);
}

function set_session_var_indval(s1){
    var s1 = document.getElementById(s1);
    localStorage.setItem(s1.id+'_key', s1.value);
}