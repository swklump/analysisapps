// function to populate table drop down based on tract or blockgroup selected
function populate_tables(s1,s2,s3,s4,s5){
    var s1 = document.getElementById(s1);
    var s2 = document.getElementById(s2);
    var s3 = document.getElementById(s3);
    var s4 = document.getElementById(s4);
    var s5 = document.getElementById(s5);

    var vals = [s2,s3,s4,s5];
    for (v in vals) {
        vals[v].innerHTML = '';
    }

    if (s1.value == null | s1.value == '') {
        for (v in vals) {
            sessionStorage.removeItem(vals[v].id + '_key')
        }
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
}

//function to populate category drop down based on table selected
function populate_col(s1,s2,s3){
    var s1 = document.getElementById(s1);
    var s2 = document.getElementById(s2);

    // Reset values if previous drop down is blank
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


    // Add options to column drop down
    var selected_table = s1.value.toUpperCase()+'_cols';
    for (var option in s3[selected_table]) {
        var newOption = document.createElement('option');
        newOption.value = s3[selected_table][option];
        newOption.innerHTML = s3[selected_table][option];
        s2.options.add(newOption);
    }


}