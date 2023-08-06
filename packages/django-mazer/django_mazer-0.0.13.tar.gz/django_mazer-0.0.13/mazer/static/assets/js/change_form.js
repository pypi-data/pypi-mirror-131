(function($) {
const noSelect2 = '.empty-form select, .select2-hidden-accessible, .selectfilter, .selector-available select, .selector-chosen select';
$('input').filter('[type!="checkbox"]').filter('[type!="submit"]').addClass('form-control');
let select_all = $('select');
select_all.addClass('form-control form-select');
select_all.not(noSelect2).select2({width: '80%' });
$(document).ready(function () {
    $('.add-row a').addClass('btn btn-outline-success');
});

// FilePond
/*
FilePond.registerPlugin(
  FilePondPluginImagePreview,
  FilePondPluginImageExifOrientation,
  FilePondPluginFileValidateSize,
  FilePondPluginImageValidateSize,
);*/

let checkExist = setInterval(function() {
    let tooltip = $('.help-tooltip');
   if (tooltip.length) {
      tooltip.tooltip({animation: true});
      clearInterval(checkExist);
   }
}, 100);

})(jQuery);