//type="text/javascript"
//document.getElementById("CreateForm").addEventListener("submit", checkForm)
document.getElementById("CreateConst").addEventListener("submit", checkConst)


function checkConst(event) {
    var el = document.getElementById("CreateConst");
//    console.log(el);
//    console.log(555 + 666);
    event.preventDefault();

    var fail = false
    var alias = el.alias_id.value;
    var aliases = el.aliases.value.split(' ');
//    console.log(alias);
//    console.log(aliases);
    let i = 0;
    while (i < aliases.length) {
        if (alias == aliases[i]) {
            fail = 'Такая конституента уже существует';
            break;}
        i++;
    }

    if (fail) {
        document.getElementById("alias_error").innerHTML = fail;
////        return false
    }

    else {
        document.getElementById('CreateConst').submit();
    }
}


function checkForm(event) {
    var el = document.getElementById("CreateForm");
    console.log(5 + 6);
    event.preventDefault();

    var name = el.name_create.value;
    var pass = el.type_create.value;
//    var repass = el.repass.value;
//    var state = el.state.value;

    var fail = false

    if (name == 1) {
        fail = 'Name can`t be "1"';}


//    if (name == "" || pass == "" || repass == "" || state == "") {
//        fail = 'Fulfill all fields';}
//    else if (name.length < 2 || name.length > 50) {
//        fail = 'Insert correct name';}
//    else if (pass != repass) {
//        fail = 'Passwords are not equal';}
//    else if (pass.split("&").length > 1) {
//        fail = 'Don`t use "&" in password';}

    if (fail) {
        document.getElementById("error1").innerHTML = fail;
////        return false
    }

    else {
        document.getElementById('CreateForm').submit();
    }
}







function insertThisInThere(thisChar, thereId) {
	function theCursorPosition(ofThisInput) {
		// set a fallback cursor location
		var theCursorLocation = 0;

		// find the cursor location via IE method...
		if (document.selection) {
			ofThisInput.focus();
			var theSelectionRange = document.selection.createRange();
			theSelectionRange.moveStart('character', -ofThisInput.value.length);
			theCursorLocation = theSelectionRange.text.length;
		} else if (ofThisInput.selectionStart || ofThisInput.selectionStart == '0') {
			// or the FF way
			theCursorLocation = ofThisInput.selectionStart;
		}
		return theCursorLocation;
	}

	// now get ready to place our new character(s)...
	var theIdElement = document.getElementById(thereId);
	var currentPos = theCursorPosition(theIdElement);
	var origValue = theIdElement.value;
	var newValue = origValue.substr(0, currentPos) + thisChar + origValue.substr(currentPos);

	theIdElement.value = newValue;

}
