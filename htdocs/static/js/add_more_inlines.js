$('#add_more').click(function() {
	var form_idx = $('#id_data_types-TOTAL_FORMS').val();
	var max_forms = $('#id_data_types-MAX_NUM_FORMS').val();
	$('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_data_types-TOTAL_FORMS').val(parseInt(form_idx) + 1);
	var add_more = $('#add_more');
	if (parseInt($('#id_data_types-TOTAL_FORMS').val()) >= parseInt(max_forms)) {
	    add_more.hide();
	};
});

$('#button-id-remove-form-row').click(function(){
    console.log(".remove-form-row click clicked");
});

$(document).on('click', 'button-id-remove-form-row', function (e) {
            console.log(".remove-form-row click clicked");
            e.preventDefault();
            deleteForm('inspection_report_form', $(this));
            return false;
        });

        function deleteForm(prefix_tag, btn) {
            // https://medium.com/all-about-django/adding-forms-dynamically-to-a-django-formset-375f1090c2b0#}
            // Get total number of forms counted by management form TOTAL_FORMS
            var total = parseInt($('#id_' + prefix_tag + '-TOTAL_FORMS').val());
            // Remove the closests element with class form-row
            btn.closest('.form-row').remove();
            var forms = $('.form-row');
            // subtract an extra 1 to account for the hidden empty_form;
            var formlength = forms.length - 1;
            var idstring = '#id_' + prefix_tag + '-TOTAL_FORMS';
            $(idstring).val(parseInt(formlength));
            console.log("formlength: ", formlength)
            for (var i = 0, formCount = formlength; i < formCount; i++) {
                $(forms.get(i)).find(':input').each(function () {
                    updateElementIndex(this, prefix_tag, i);
                });
            }
            return false;
        };
