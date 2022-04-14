// function to populate table drop down based on tract or blockgroup selected
function populate_tables(s1,s2,s3,s4,s5,s6,s7){
    var s1 = document.getElementById(s1);
    var s2 = document.getElementById(s2);
    var s3 = document.getElementById(s3);
    var s4 = document.getElementById(s4);
    var s5 = document.getElementById(s5);
    var s6 = document.getElementById(s6);
    var s7 = document.getElementById(s7);

    sessionStorage.setItem('test_key', "{{cols}}");

    // set session storage variable for tract_block group
    sessionStorage.setItem(s1.id+'_key', s1.value);

    s2.innerHTML = '';
    s3.innerHTML = '';
    s4.innerHTML = '';
    s5.innerHTML = '';
    s6.innerHTML = '';
    s7.innerHTML = '';
    if (s1.value == null | s1.value == '') {
        sessionStorage.removeItem(s2.id + '_key')
        sessionStorage.removeItem(s3.id + '_key')
        sessionStorage.removeItem(s4.id + '_key')
        sessionStorage.removeItem(s4.id + '_key_list')
        sessionStorage.removeItem(s5.id + '_key')
        sessionStorage.removeItem(s5.id + '_key_list')
        sessionStorage.removeItem(s6.id + '_key')
        sessionStorage.removeItem(s6.id + '_key_html')
        sessionStorage.removeItem(s6.id + '_key_list')
        sessionStorage.removeItem(s6.id + '_key_list_html')
        sessionStorage.removeItem(s7.id + '_key')
        sessionStorage.removeItem(s7.id + '_key_html')
        sessionStorage.removeItem(s7.id + '_key_list')
        sessionStorage.removeItem(s7.id + '_key_list_html')
    }


    // assign table drop down items by tract or block group selection
    if(s1.value == 'Tract'){
        var optionArray = [
            '|Select a table...',
            // 'dp04|DP04 - Selected Housing Characteristics',
            'dp05|DP05 - ACS Demographic and Housing Estimates',
            // 's0802|S0802 - Means of Transportation to Work by Selected Characteristics',
            // 's1501|S1501 - Educational Attainment', 's1701|S1701 - Poverty Status in the Past 12 Months',
            // 's1810|S1810 - Disability Characteristics', 's1901|S1901 - Income in the Past 12 Months'
    ];
    } else if(s1.value == 'Block Group'){
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
    for(var option in optionArray){
    var pair = optionArray[option].split('|');
    var newOption = document.createElement('option');
    newOption.value = pair[0];
    newOption.innerHTML = pair[1];
    s2.options.add(newOption);
    }

    // run for loop to assign the value and label
    for(var option in optionArray){
    var pair = optionArray[option].split('|');
    var newOption = document.createElement('option');
    newOption.value = pair[0];
    newOption.innerHTML = pair[1];
    s3.options.add(newOption);
    }

    // reset the variable drop downs to blank if tr_bg changed after
    if(s1.value == ''){
    var newOption = document.createElement('option')
    newOption.value = '';
    newOption.innerHTML = '';
    s4.options.add(newOption);
    s5.options.add(newOption);
    s6.options.add(newOption);
    s7.options.add(newOption);
    }

}


//function to populate category drop down based on table selected
function populate_cat(s1,s2, s3){
    var s1 = document.getElementById(s1);
    var s2 = document.getElementById(s2);
    var s3 = document.getElementById(s3);

    if (s1.value == '') {
        s2.innerHTML = '';
        var newOption = document.createElement('option')
        newOption.value = '';
        newOption.innerHTML = '';
        s2.options.add(newOption);
        sessionStorage.removeItem(s2.id + '_key')
        sessionStorage.removeItem(s2.id + '_key_list')
    }
    else {
        s2.innerHTML = '';
        var newOption = document.createElement('option')
        newOption.value = '';
        newOption.innerHTML = 'Select a category...';
        s2.options.add(newOption);
        sessionStorage.removeItem(s2.id + '_key')
        sessionStorage.removeItem(s2.id + '_key_list')
    }

    s3.innerHTML = '';
    var newOption = document.createElement('option')
    newOption.value = '';
    newOption.innerHTML = '';
    s3.options.add(newOption);
    sessionStorage.removeItem(s3.id + '_key')
    sessionStorage.removeItem(s3.id + '_key_list')
    sessionStorage.removeItem(s3.id + '_key_list_html')

    // set session storage variable for table
    sessionStorage.setItem(s1.id+'_key', s1.value);

    // API urls for columns
    const api_url_profile = 'https://api.census.gov/data/2019/acs/acs5/profile/variables.json'
    const api_url_subject = 'https://api.census.gov/data/2019/acs/acs5/subject/variables.json'
    const api_url_detailed = 'https://api.census.gov/data/2019/acs/acs5/variables.json'
    var first_char = s1.value[0];
    var api_url = '';

    if (first_char == 'd') {
        api_url = api_url_profile
    }
    else if (first_char == 's') {
        console.log('yes');
        api_url = api_url_subject
    }
    else if (first_char == 'b') {
        api_url = api_url_detailed
    }

    // Get table columns from api census
    $.getJSON(api_url, function(data) {
        var cats_sesh_var = [];
        let column_id = Object.entries(data.variables);

        // Get sorted array to display variables cleanly
        var column_id_sorted = [];
        for(var option in column_id) {
            column_id_sorted.push([column_id[option][0],column_id[option][1].label])
        }

        column_id_sorted.sort(function(a, b) {
            var valueA, valueB;
            valueA = a[1];
            valueB = b[1];
            if (valueA < valueB) {return -1;}
            else if (valueA > valueB) {return 1;}
            return 0;
        });


        // Add variables to drop down
        var cats = [];
        for(var option in column_id_sorted) {
            key = column_id_sorted[option][0];
            val = column_id_sorted[option][1];
            let table_name = key.substring(0,s1.value.length).toLowerCase();
            var col_type = '';
            var col_index = '';
            if (api_url == api_url_profile) {
                 col_type = 'Percent';
                 col_index = 7;
            }
            else if (api_url == api_url_subject) {
                col_type = 'Estimate';
                col_index = 8;
            }
            if (s1.value == table_name && val.substring(0,col_index) == col_type){

                // only keep variable text after last '!!'
                var exp_count = ( val.split("!!", -1).length ) - 1;
                var val_edited = val;
                for(i=0;i < exp_count-1;i += 1){
                    val_edited = val_edited.substring(val_edited.indexOf('!!')+2,)
                    if (i==0) {
                        var category = val_edited.substring(0,val_edited.indexOf('!!'));
                    }
                }

                category = category.charAt(0).toUpperCase() + category.slice(1).toLowerCase();
                // Dont have repeat options
                if (cats.includes(category, 0) == false) {
                    var newOption = document.createElement('option');
                    newOption.value = category;
                    newOption.innerHTML = category;
                    s2.options.add(newOption);
                    cats.push(category);
                    cats_sesh_var.push(category);
                };
            }
        }
        sessionStorage.setItem(s2.id+'_key_list', cats_sesh_var.join("`"));
    });
}


//function to populate variable drop down based on category selected
function populate_var(s1,s2,s3){

    var s1 = document.getElementById(s1);
    var s2 = document.getElementById(s2);
    var s3 = document.getElementById(s3);

    if (s1.value == '') {
        s2.innerHTML = '';
        var newOption = document.createElement('option')
        newOption.value = '';
        newOption.innerHTML = '';
        s2.options.add(newOption);
        sessionStorage.removeItem(s2.id + '_key')
        sessionStorage.removeItem(s2.id + '_key_list')
    }
    else {
        s2.innerHTML = '';
        var newOption = document.createElement('option')
        newOption.value = '';
        newOption.innerHTML = 'Select a category...';
        s2.options.add(newOption);
        sessionStorage.removeItem(s2.id + '_key')
        sessionStorage.removeItem(s2.id + '_key_list')
    }

    sessionStorage.setItem(s1.id+'_key', s1.value);

    // Get table columns from api census
    const api_url = 'https://api.census.gov/data/2019/acs/acs5/profile/variables.json'
    $.getJSON(api_url, function(data) {
        var var_sesh_var = [];
        var var_sesh_html = []
        let column_id = Object.entries(data.variables);

        // Get sorted array to display variables cleanly
        var column_id_sorted = [];
        for(var option in column_id) {
            column_id_sorted.push([column_id[option][0],column_id[option][1].label])
        }

        column_id_sorted.sort(function(a, b) {
            var valueA, valueB;
            valueA = a[1];
            valueB = b[1];
            if (valueA < valueB) {return -1;}
            else if (valueA > valueB) {return 1;}
            return 0;
        });

        // Add variables to drop down
        for(var option in column_id_sorted){
            key = column_id_sorted[option][0];
            val = column_id_sorted[option][1];
            let table_name = key.substring(0,s3.value.length).toLowerCase();
            if (s3.value == table_name && val.substring(0,7) == 'Percent') {
                // only keep variable text after last !!
                let exp_count = ( val.split("!!", -1).length ) - 1;
                let val_edited = val;

                for(i=0;i < exp_count-1;i += 1) {
                    val_edited = val_edited.substring(val_edited.indexOf('!!')+2,)
                    if (i==0) {
                        var category = val_edited.substring(0,val_edited.indexOf('!!'));
                    };
                };

                category = category.charAt(0).toUpperCase() + category.slice(1).toLowerCase();
                val_edited = val_edited.charAt(0).toUpperCase() + val_edited.slice(1).toLowerCase();
                val_edited = val_edited.replace('!!',' - ')
                if (category == s1.value && val_edited.substring(0,category.length) !== category) {
                    var newOption = document.createElement('option');
                    newOption.value = key+":"+val_edited;
                    newOption.innerHTML = val_edited;
                    s2.options.add(newOption);
                    var_sesh_var.push(key);
                    var_sesh_html.push(val_edited);
                };
            }
        }
        sessionStorage.setItem(s2.id+'_key_list', var_sesh_var.join("`"));
        sessionStorage.setItem(s2.id+'_key_list_html', var_sesh_html.join("`"));
    });
}

// set session storage variable for variable
function set_session_var(s1){
    var s1 = document.getElementById(s1);
    sessionStorage.setItem(s1.id+'_key', s1.value);
    sessionStorage.setItem(s1.id+'_key_html', s1.options[s1.selectedIndex].text);
}

function set_session_var_indval(s1){
    var s1 = document.getElementById(s1);
    sessionStorage.setItem(s1.id+'_key', s1.value);
}


