function update_correctly() {
    var num_teams = document.getElementById('num_teams').value

    for (var i = 2; i < 11; i++) {
	if (i <= num_teams) {
	    document.getElementById('t_' + i).className = '';
	    document.getElementById('t_f_' + i).className = 'form-inline';
	}
	else {
	    document.getElementById('t_' + i).className = 'hidden';
	    document.getElementById('t_f_' + i).className = 'form-inline hidden';
	}
    }
    num_teams = parseInt(num_teams);
    for (var i = 2; i <= 5; i ++) {
	if (i <= ((num_teams + 1) / 2)) {
	    document.getElementById('j_h_' + i).className = 'form-inline';
	}
	else {
	    document.getElementById('j_h_' + i).className = 'form-inline hidden';
	}
    }
    document.getElementById('cost').innerText = '$' + (num_teams * 20);
}
