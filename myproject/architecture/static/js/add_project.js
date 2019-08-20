$(function() {
    var div_architect = $('#div_id_architect');
    var architect_name = $('#div_id_architect_name');
    var architect_description = $('#div_id_architect_description');

    architect_name.css('display', 'none');
    architect_description.css('display', 'none');
    
    var form = div_architect.parent();
    var button = $("button").text("Add architect");
    console.log(button)
    button.attr('class', 'btn btn-success');
    button.after(div_architect);

    function toggle_buttons(event) {
        event.stopImmediatePropagation();
        console.log('click');
        console.log(div_architect.style.display);
        if (div_architect.style.display !== 'none') {
            div_architect.style.display = 'none';
            architect_name.style.display= 'block';
            architect_description.style.display= 'block';
            button.className = 'btn btn-danger';
            button.innerText = 'Show list of architects';
            div_architect.querySelector('select option[selected]').value = ""
        } else {
            div_architect.style.display = 'block';
            architect_name.style.display= 'none';
            architect_description.style.display= 'none';
            button.className = 'btn btn-success';
            button.innerText = 'Add architect';
        }
    }
    // div_architect.('select option[selected]').value = "";
    // button.addEventListener('click', toggle_buttons)
});
