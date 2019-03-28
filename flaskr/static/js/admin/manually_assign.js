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

function alConf(name) {
	return confirm("Match {{udata.first_name + "
		" + udata.last_name}} With " + name + "?")
}
