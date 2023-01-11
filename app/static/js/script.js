/* Close all autocomplete lists */
document.addEventListener('click', function (e) {
	closeAllLists(e.target);
});

/* Count for arrow key item-selecting */
var count = 0;
var branch_count = 0;

/* Code bank input */
function bank_autocomplete(id) {
	input_ = document.getElementById(id);
	value_ = document.getElementById(id).value;
	axios
		.get(`/bank?search=${value_}`)
		.then(function (response) {
			/* Code auto complete de day */
			var arr = response.data;
			console.log(arr);
			var a,
				b,
				i,
				val = value_;
			closeAllLists(); /* Close lists on new input */
			currentFocus = -1;
			/* Create a DIV element containing items (values) */
			a = document.createElement('DIV');
			a.setAttribute('id', input_.id + 'autocomplete-list');
			a.setAttribute('class', 'autocomplete-items');
			/* Append the DIV as a child of the autocomplete container (input's sibling)*/
			input_.parentNode.appendChild(a);
			/* Check if the items */
			for (i = 0; i < arr.length; i++) {
				/* Create a DIV for matching element:*/
				b = document.createElement('DIV');
				b.innerHTML = arr[i];
				b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
				/* Insert the value for the autocomplete */
				b.addEventListener('click', function (e) {
					input_.value = this.getElementsByTagName('input')[0].value;
					closeAllLists();
				});
				a.appendChild(b);
			}
		})
		.catch(function (error) {
			console.log(error);
		});

	/* Execute function when a key is pressed */
	count += 1;
	if (count == 1) {
		input_.addEventListener('keydown', function (e) {
			var x = document.getElementById(input_.id + 'autocomplete-list');
			if (x) x = x.getElementsByTagName('div');
			if (e.keyCode == 40) {
				/* If the arrow DOWN key is pressed, increase the currentFocus variable */
				currentFocus++;
				/* and make the current item more visible */
				addActive(x);
			} else if (e.keyCode == 38) {
				/* If the arrow UP key is pressed, decrease the currentFocus variable:*/
				currentFocus--;
				/* and make the current item more visible */
				addActive(x);
			} else if (e.keyCode == 13) {
				/* If the ENTER key is pressed, prevent the form from being submitted,*/
				e.preventDefault();
				if (currentFocus > -1) {
					/* and simulate a click on the "active" item */
					if (x) x[currentFocus].click();
				}
			}
		});
	}
}

/* Code branch input */
function branch_autocomplete(id) {
	branch = document.getElementById(id);
	branch_value = document.getElementById(id).value;
	bank = document.getElementById('bank');
	bank_value = document.getElementById('bank').value;
	axios
		.get(`/branch?search=${branch_value}&bank=${bank_value}`)
		.then(function (response) {
			/* Code branch auto complete de day */
			console.log(response.data);
			var branch_arr = response.data;
			var a,
				b,
				i,
				val = branch_value;
			closeAllLists(); /* Close lists on new input */
			currentFocus = -1;
			/* Create a DIV element containing items (values) */
			a = document.createElement('DIV');
			a.setAttribute('id', branch.id + 'autocomplete-list');
			a.setAttribute('class', 'autocomplete-items');
			/* Append the DIV as a child of the autocomplete container (input's sibling)*/
			branch.parentNode.appendChild(a);
			/* Check if the items */
			for (i = 0; i < branch_arr.length; i++) {
				/* Create a DIV for matching element:*/
				b = document.createElement('DIV');
				b.innerHTML = branch_arr[i];
				b.innerHTML += "<input type='hidden' value='" + branch_arr[i] + "'>";
				/* Insert the value for the autocomplete */
				b.addEventListener('click', function (e) {
					branch.value = this.getElementsByTagName('input')[0].value;
					closeAllLists();
				});
				a.appendChild(b);
			}
		})
		.catch(function (error) {
			console.log(error);
		});
	/* Execute function when a key is pressed */
	branch_count += 1;
	if (branch_count == 1) {
		branch.addEventListener('keydown', function (e) {
			var x = document.getElementById(branch.id + 'autocomplete-list');
			if (x) x = x.getElementsByTagName('div');
			if (e.keyCode == 40) {
				/* If the arrow DOWN key is pressed, increase the currentFocus variable */
				currentFocus++;
				/* and make the current item more visible */
				addActive(x);
			} else if (e.keyCode == 38) {
				/* If the arrow UP key is pressed, decrease the currentFocus variable:*/
				currentFocus--;
				/* and make the current item more visible */
				addActive(x);
			} else if (e.keyCode == 13) {
				/* If the ENTER key is pressed, prevent the form from being submitted,*/
				e.preventDefault();
				if (currentFocus > -1) {
					/* and simulate a click on the "active" item */
					if (x) x[currentFocus].click();
				}
			}
		});
	}
}

/* Close all autocomplete lists, except ones passed as an argument:*/
function closeAllLists(elmnt, inp) {
	var x = document.getElementsByClassName('autocomplete-items');
	if (!elmnt) {
		for (var i = 0; i < x.length; i++) {
			x[i].parentNode.removeChild(x[i]);
		}
	} else {
		for (var i = 0; i < x.length; i++) {
			if (elmnt != x[i] && elmnt != inp) {
				x[i].parentNode.removeChild(x[i]);
			}
		}
	}
}

/* Classify an item as "active" */
function addActive(x) {
	if (!x) return false;
	/*start by removing the "active" class on all items:*/
	removeActive(x);
	if (currentFocus >= x.length) currentFocus = 0;
	if (currentFocus < 0) currentFocus = x.length - 1;
	/*add class "autocomplete-active":*/
	x[currentFocus].classList.add('autocomplete-active');
}

/* Remove the "active" class */
function removeActive(x) {
	for (var i = 0; i < x.length; i++) {
		x[i].classList.remove('autocomplete-active');
	}
}
