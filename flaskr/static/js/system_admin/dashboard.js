function confSus() {
		return confirm("Please Confirm You Wish To Suspend This Scheme. All Assosicated Data Will Be Retained")
}

function confDel() {
		return confirm("Please Confirm You Wish To Delete This Scheme And All Assosicated Data.")
}

function ele(id) {
		return document.getElementById(id)
}
function filter() {
		var tb = ele('tbody')
		var reg = new RegExp(".*" + ele("nameFilt").value + ".*", "i")
		var actFil = selActFil()
		for (var i = 0, row; row = tb.rows[i]; i++) {
				if (filterName(row, reg) && (actFil === 'All' || activeFilter(row, actFil))) {
						row.style.display = ''
				} else {
						row.style.display = 'none'
				}
		}
}
function filterName(row, reg) {
		if (reg.test(row.cells[1].innerHTML)) {   // need to impl show/no show if other filter on
				return true
		} else {
				return false
		}
}
function selActFil() {
		var radios = document.getElementsByName('actFilter');
		for (var i = 0, length = radios.length; i < length; i++)
		{
				if (radios[i].checked)
				{
						return radios[i].value;
				}
		}
}
function activeFilter(row, fil) {
		if ((row.cells[3].innerHTML === 'Active' && fil === 'act') || (row.cells[3].innerHTML === 'Suspended' && fil === 'sus')) {
				return true
		} else {
				return false
		}
}
