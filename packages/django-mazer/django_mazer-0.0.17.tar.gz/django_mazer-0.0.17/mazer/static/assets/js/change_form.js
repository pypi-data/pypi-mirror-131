(function($) {
const noSelect2 = '.empty-form select, .select2-hidden-accessible, .selectfilter, .selector-available select, .selector-chosen select';
$('input').filter('[class!=vTimeField]').filter('[class!=vDateField]').filter('[type!=checkbox]').filter('[type!=submit]').addClass('form-control');
$('input[class=vTimeField],input[class=vDateField]').addClass('form-select');
let select_related = $('.related-widget-wrapper > select');
let select_all = $('.position-relative > select');
select_related.addClass('form-control form-select');
select_all.addClass('form-control form-select');
select_related.not(noSelect2).select2({width: '70%'});
select_all.not(noSelect2).select2({width: '100%'});


$(document).ready(function () {
    $('.add-row a').addClass('btn btn-outline-success float-start');
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