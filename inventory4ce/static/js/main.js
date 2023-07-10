this.infoPopover()
this.helpPopover()
this.lmgtfy()
this.theRealLMGTFY()
function fetchSearch(query) {
  
  history.replaceState( {} , 'foo', encodeURI('/#search=' + query));

  fetch('/search?q='+query)
    .then(response => response.json())
    .then(data => {

    if (data.query != document.getElementById("search").value) {
      return
    }

    this.infoPopover()
    var results = data.results
    var numberOfResults = results.length

    if (query === '') {
      document.getElementById('results').style.display = 'none';
      document.getElementById('indices').style.display = 'block';
      document.getElementById('upload-form').style.display = 'block';
      document.getElementById('queue').style.display = 'none';
    } else {
      document.getElementById('indices').style.display = 'none';
      document.getElementById('upload-form').style.display = 'none';
      document.getElementById('results').style.display = 'block';
      document.getElementById('queue').style.display = 'none';               
    }
    //refresh Cat-width
    document.getElementById("searchCatMiddle").width = numberOfResults*3
    // get row template
    var t = document.querySelector("#resultrow")
    var columns = t.content.querySelectorAll("td")

    // remove existing rows
    var tb = document.querySelector("#table-results tbody")
    tb.textContent = ""

    // add results as rows
    for (var i = 0; i < results.length; i++) {
      var result = results[i]
      columns[0].textContent = result.abbreviation.join(", ")
      columns[1].textContent = result.term
      columns[2].textContent = result.definition
      columns[3].querySelector("a").setAttribute('href', result.url)
      columns[3].querySelector("a").textContent = result.id
      columns[4].textContent = result.score

      var clone = document.importNode(t.content, true)
      tb.appendChild(clone)
      
    }

    if (numberOfResults > 0) {
      document.getElementById('noresults').style.display = 'none';
      if (numberOfResults == 200){
        document.getElementById('number-of-results').innerText = 'Only 200 results are displayed - try to narrow it down';
      } else if (numberOfResults == 1){
        document.getElementById('number-of-results').innerText = 'One Result';
      } else {
        document.getElementById('number-of-results').innerText = numberOfResults +' Results';
      }
      document.getElementById('number-of-results').style.display = 'block';
    } else{
      document.getElementById('number-of-results').style.display = 'none';
      document.getElementById('noresults').style.display = 'block';
    }
  })

}


function handleFileUpload(event) {
  document.getElementById('search-field').style.display = 'none';
  document.getElementById('results').style.display = 'none';
  document.getElementById('indices').style.display = 'none';
  document.getElementById('upload-form').style.display = 'none';
  document.getElementById('queue').style.display = 'block';
  
  var form = event.form
  console.log(event)
  var formData = new FormData()
  var url = form.action
  formData.append('file', event.files[0])
  console.log(formData)

  fetch(url, {method: "POST", body: formData}).then(response => response.json())
  .then(data => {
    document.getElementById('queue').style.display = 'none';
    document.getElementById('messages').style.display = 'block';

    if(data.status==='success'){
      console.log(data.link)
      var link = document.createElement('a')
      link.href=data.link
    
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      document.getElementById('message').textContent = 'Creating a list of abbreviations was succesful.';
    
    } else {
      document.getElementById('message').textContent = data.message;
    }
  })
 
}


function lmgtfy(){
  if(window.location.href.includes('/#search=') == true){
    query = decodeURI(window.location.href.split('/#search=',2)[1]);
    console.log(query)
    document.getElementById("search").value = query
    this.fetchSearch(query);  // redo search due to race condition
  }
}
 function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
// the real LMGTFY
async function theRealLMGTFY(){
  if(window.location.href.includes('/#lmgtfy=') == true){
    var lmgtfy = decodeURI(window.location.href.split('/#lmgtfy=',2)[1]);
    var query =''
    for (var i=0; i < lmgtfy.length; i++){
      query = query + lmgtfy.charAt(i);
      document.getElementById("search").value = query
      this.fetchSearch(query);  // redo search due to race condition
      await this.sleep(200-(i*10));
    }
  }
}

// activate and fill the info popover
function infoPopover() {
console.log('info Popover-initialized');
 fetch("/counter")
  .then(response => response.json())
  .then(data => {

    console.log(data);
    var content = '<b>shortCATS</b> is a search for Abbreviations in Thales.<br />Latest document from '+data.latestDoc+'<br />Number of documents: '+data.documents+'<br />Number of visits: '+data.visits+'<br />Total DB queries: '+data.queries+'<br /><br />Sources:<br />'
   
    for(source of data.sources) {
      content += '<b>' +source['key']+'</b> ('+source['doc_count']+' Docs)<br />';
    }
    
    $('[data-toggle="infoPopover"]').attr('data-content', content);
    //document.getElementById('info-popover').attr('data-content', content);
    document.getElementById('numdocs').innerHTML = data.documents;
  })
}
// popover 
$(document).ready(function () {$(function () {
  $('[data-toggle="infoPopover"]').popover()
});
})

// activate and fill the help popover
function helpPopover() {
  console.log('help Popover-initialized');
      
      var content = '<b>shortCATS searching for abbreviations:</b> <br> please enter your unknown abbreviation in the search field and shortCats will search for the meaning in the given directories. <br> <b>shortCATS creating list of abbreviations: </b> <br> ShortCats can find all abbreviations in a docx document. All words that have at least two capital letters and/or no vowels are considered abbreviations.<br>ShortCats appends a list with all found abbreviations at the end of the document. Since not for all abbreviations an explanation can be found the list must be gone through again by the author of the document. If more than one definition is found for an abbreviation, all definitions are appended to the table. It is up to the author to choose the appropriate meaning. Since the sources of shortCats overlap, there may be several entries in the list with the same definition.<br>If shortCats recognizes words as abbreviations that are not abbreviations, you can use the feedback form at the bottom right to let us know, and we will take care that this word will not be suggested as an abbreviation in the future.  '
     
      $('[data-toggle="helpPopover"]').attr('data-content', content);
    
  }
  // popover 
  $(document).ready(function () {$(function () {
    $('[data-toggle="helpPopover"]').popover()
  });
  })
