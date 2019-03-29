function ele(id) {
	return document.getElementById(id)
}

function filterName() {
	var reg = new RegExp(".*" + ele("nameFilt").value + ".*", "i");
	var tb = ele('tbody');
	for (var i = 0, row; row = tb.rows[i]; i++) {
		if (reg.test(row.cells[1].innerHTML + " " + row.cells[2].innerHTML)) { // need to impl show/no show if other filter on
			row.style.display = ''
		} else {
			row.style.display = 'none'
		}
	}
}

function alConf(user, match) {
	return confirm("Match " + user + " With " + match + "?")
}
