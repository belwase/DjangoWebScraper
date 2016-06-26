
def getDropdown(option, obj=""):
  html = ''
  if option == 'static_location':
    html = """<div class="dropdown form-group">
               <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Select  Location
                   <span class="caret"></span></button>
                    <ul class="dropdown-menu">
                      <li class="location"><a class="option_dropdown ">Asia</a></li>
                      <li class="location"><a class="option_dropdown ">Europe</a></li>
                      <li class="location"><a class="option_dropdown ">South Pacific</a></li>
                      <li class="location"><a class="option_dropdown ">America</a></li>
                      <li class="location"><a class="option_dropdown ">Africa</a></li>'
                    </ul>
                </div>"""	

  elif option == 'location':
    html = """<div class="dropdown form-group">
               <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Select  Location
                   <span class="caret"></span></button>
                    <ul class="dropdown-menu">""" 
    loc_list = obj.objects.all()
    for loc in loc_list:
      html = html +   '<li class="location"><a class="option_dropdown " value="' + loc.url +'">'+loc.name + '</a></li>' 

    html = html + """</ul>
                </div>"""


  elif option == 'trip_category':
    html = """<div class="dropdown form-group">
               <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Select  Category
                   <span class="caret"></span></button>
                    <ul class="dropdown-menu">"""
    cat_list = obj.objects.all()
    for cat in cat_list:
        html = html + '<li class="category"><a class="option_dropdown" value="' + cat.cat+ '" >'+cat.name + ' </a></li>'
    
    html = html + """</ul>
                </div>""" 
  #print html
  return html