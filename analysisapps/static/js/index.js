//Print to console
console.log('Hello World');

//Assign variables
let name = 'mosh';
let age = 30; // Number literal
let isApproved = true; // Boolean
let lastName = null;
typeof name; // get variable type

// create dictionary
let person = {
name: 'Mosh',
age: 30};

// create list
let selectedColors = ['red','blue'];
selectedColors[2] = 'green'; // add item to list
selectedColors[3] = 3;
console.log(selectedColors[0]); // access by index
console.log(selectedColors.length); // get length of list

// define a function, with optional parameter, and return value
function greet(name, big, lastName='') {
console.log('Hello ' + name + ' ' +lastName);
return big * 5
}
let new_var = greet('bob',10,'smith');
console.log(new_var);

