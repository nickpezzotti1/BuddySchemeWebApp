function ele(id) {
	return document.getElementById(id)
}

function filter() {
	var tb = ele('tbody');
	var reg = new RegExp(".*" + ele("nameFilt").value + ".*", "i");
	var menFil = selMenFil();
	for (var i = 0, row; row = tb.rows[i]; i++) {
		if (filterName(row, reg) && (menFil === 'All' || mentorFilter(row, menFil))) {
			row.style.display = ''
		} else {
			row.style.display = 'none'
		}
	}
}

function filterName(row, reg) {
	if (reg.test(row.cells[1].innerHTML + " " + row.cells[2].innerHTML)) { // need to impl show/no show if other filter on
		return true
	} else {
		return false
	}
}

function selMenFil() {
	var radios = document.getElementsByName('menFilter');
	for (var i = 0, length = radios.length; i < length; i++) {
		if (radios[i].checked) {
			return radios[i].value;
		}
	}
}

function mentorFilter(row, fil) {
	if ((row.cells[4].innerHTML === 'Yes' && fil === 'tor') || (row.cells[4].innerHTML === 'No' && fil === 'tee')) {
		return true
	} else {
		return false
	}
}
