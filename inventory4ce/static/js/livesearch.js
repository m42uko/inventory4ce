jQuery(document).ready(function () {
  jQuery("#item").keyup(function () {
    // Retrieve the input field text and reset the count to zero
    var filter = $(this).val(),
      count = 0;

    // Loop through the comment list
    jQuery(".searchvalues").each(function () {
      // If the list item does not contain the text phrase fade it out
      if (jQuery(this).text().search(new RegExp(filter, "i")) < 0) {
        jQuery(this).fadeOut();

        // Show the list item if the phrase matches and increase the count by 1
      } else {
        jQuery(this).show();
        count++;
      }
    });

    // Update the count
    var numberItems = count;
    jQuery("#filter-count").text("Items found: " + count); //<span id="filter-count"></span> if you want to show number of found items
  });
});
