# File of coop names by URL
def get_coop_names():
    coops = {
        'brown': 'Brown',
        'scully': 'Scully',
        'ifc': 'IFC',
        '2d': '2D',
        'realfood': 'Real Food'
    }
    return coops

#----------------------------------------------------------------------

def genRosterHTML(members):

    html_code = (
        '<table class="table" id="myTable" style="margin: 0;">'
        )
    
    html_code += ('<thead id="theader">')
    html_code += ('<tr><th scope="col">Member Name</th><th scope="col">Dietary Restrictions</th>'
                '<th scope="col">Cook Shift</th><th scope="col">Chore Shift</th></tr>')
    html_code += ('</thead><tbody id="tbody">')

    for member in members:
        # don't display members that do not have names
        if member.user_name == '':
            continue

        html_code += '<tr>'

        html_code += ('<th scope="row">{0}</th>'
                    '<td>{1}</td>'
                    '<td>{2}</td>'
                    '<td>{3}</td>').format(member.user_name,
                                        member.user_allergies,
                                        member.user_cookday,
                                        member.user_choreday,
                                        )
        # html_code += ('<td><input type="button" class="btn btn-primary btn-sm" value="Remove" onclick="deleteRow(this)"></td>')
        # html_code += ('<td hidden>{0}</td>').format(member.user_netid)
        html_code += '</tr>'
    
    html_code += ('</tbody></table>')

    return html_code

#----------------------------------------------------------------------

def genRosterOverviewHTML(members):

    html_code = (
        '<table class="table" id="myTable" style="margin: 0;">'
        )
    
    html_code += ('<thead id="theader">')
    html_code += ('<tr><th scope="col">Member NetID</th><th scope="col">Member Name</th><th scope="col">Admin Status</th>')
    html_code += ('</thead><tbody id="tbody">')

    # sort members

    for member in members:
        html_code += '<tr>'
        
        user_name = member.user_name
        if member.user_name == '':
            user_name = "User needs to add their profile information"

        user_admin = 'Member'
        if member.user_admin:
            user_admin = 'Admin'

        html_code += ('<th scope="row">{0}</th>'
                    '<th scope="row">{1}</th>'
                    '<td>{2}</td>').format(member.user_netid,
                                        user_name,
                                        user_admin,
                                        )
        html_code += ('<td><input type="button" class="btn btn-danger btn-sm" value="Remove" onclick="deleteRow(this)"></td>')
        if member.user_admin == False:
            html_code += ('<td><input type="button" class="btn btn-primary btn-sm" value="Make Admin" onclick="addAdmin(this)"></td>')
        html_code += ('<td hidden>{0}</td>').format(member.user_netid)
        html_code += '</tr>'
    
    html_code += ('</tbody></table>')

    return html_code

#----------------------------------------------------------------------

def genItemTableHTML(items, is_food, is_admin, netid):
    '''
        Create HTML code 
    '''
    html_code = (
        '<table class="table" id="myTable" style="margin: 0;">'
        )
    
    html_code += ('<thead id="theader">')
    html_code += ('<tr><th scope="col">Item</th><th scope="col">Type</th>')
    if is_food is True:
        html_code += ('<th scope="col">Food Type</th>')
    html_code += ('<th scope="col">Qty</th><th scope="col">Comments</th>'
                '<th scope="col">Alt Item</th><th scope="col">For Shift?</th>'
                '<th scope="col">Ordered?</th>'
                '<th scope="col">Upvotes</th>'
                '</tr>')
    html_code += ('</thead><tbody id="tbody">')

    # sort items by food type
    if is_food is True:
        items.sort(key=lambda x: x.food_type)
    else:
        items.sort(key= lambda x: x.item_name)

    for item in items:
        html_code += '<tr>'
        html_code += ('<th scope="row">{0}</th>'
                        '<td>{1}</td>').format(item.item_name,
                                                 item.item_type)
        if is_food is True:
            html_code += ('<td>{0}</td>').format(item.food_type)
        html_code += ('<td>{0}</td>'
                    '<td>{1}</td>'
                    '<td>{2}</td>').format(item.item_quantity,
                                        item.item_reason,
                                        item.alt_request)
        if item.for_shift is True:
            for_shift = "Yes"
        else:
            for_shift = "No"
        html_code += ('<td>{0}</td>').format(for_shift)
        if item.item_ordered is True:
            ordered = "Yes"
            html_code += ('<td><div class="form-check">'
            '<input name="order-box" class="form-check-input" type="checkbox" value="" id="order-check" onclick="updateOrdered(this)" checked>')
        else:
            ordered = "No"
            html_code += ('<td><div class="form-check">'
            '<input name="order-box" class="form-check-input" type="checkbox" value="" id="order-check" onclick="updateOrdered(this)">')
        html_code += ('<label class="form-check-label" for="order-check">{0}</label>').format(ordered)
        html_code += ('</div></td>')
        upvote_count = str(len(item.upvoted_members))
        if netid in item.upvoted_members:
            html_code += ('<td><button type="button" class="btn btn-info btn-sm" onclick="changeUpvote(this)">')
            html_code += upvote_count + ('</button></td>')
        else:
            html_code += ('<td><button type="button" class="btn btn-secondary btn-sm" onclick="changeUpvote(this)">')
            html_code += upvote_count + ('</button></td>')
        if is_admin or (netid == item.requesting_user):
            html_code += ('<td><button type="button" class="btn btn-danger btn-sm" onclick="removeItem(this)">Remove</button></td>')
        html_code += ('<td hidden>{0}</td>').format(item.item_id)

        html_code += '</tr>'
    
    html_code += ('</tbody></table>')

    return html_code

#----------------------------------------------------------------------

def genRecipeGalleryHTML(recipes):
    # inner
    html_code = ('<div class="carousel-inner py-4">')

    # row
    html_code += ('<div class="carousel-item active">')
    html_code += ('<div class="container">')
    html_code += ('<div class="row">')

    # single item
    for recipe in recipes:
        html_code += ('<div class="col-lg-4 d-lg-block">')
        html_code += ('<div class="card">')

        img_src = ('\'static\',filename=\'{0}\'').format(recipe.recipe_img)
        html_code += ('<img src="{{ url_for({0}) }}" class="card-img-top"/>').format(img_src)
        html_code += ('<div class="card-body">')
        html_code += ('<h5 class="card-title">{0}</h5>').format(recipe.recipe_name)

        if recipe.recipe_link: 
            html_code += ('<p class="card-text"><a href="{0}" target="_blank">Link to Recipe</a></p>').format(recipe.recipe_link)

        # html_code += ('<a href="#!" class="btn btn-primary">Instructions</a>')
        html_code += ('<button type="button" class="btn btn-primary" id="view_instr-btn" data-bs-toggle="modal" data-bs-target="#viewInstructionsModal{0}">').format(recipe.recipe_id)
        html_code += ('Instructions </button>')

        # Remove button
        html_code += ('<input type="button" class="btn btn-danger btn-sm" value="Remove" onclick="removeRecipe(this)">')

        # hidden recipe ID
        html_code += ('<p hidden>{0}</p>').format(recipe.recipe_id)

        html_code += ('</div></div></div>')

        # modal for each recipe's instructions
        html_code += ('<div class="modal fade" id="viewInstructionsModal{0}" tabindex="-1" role="dialog" aria-labelledby="recModalLabel">').format(recipe.recipe_id)
        html_code += ('<div class="modal-dialog" role="document">')
        html_code += ('<div class="modal-content">')
        html_code += ('<div class="modal-header"><h4>How To Make {0}!</h4>').format(recipe.recipe_name)
        html_code += ('<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button></div>')
        html_code += ('<div class="modal-body">')
        html_code += ('<h5>Ingredients:</h5><p>{0}</p><hr>').format(recipe.recipe_ingredients)
        html_code += ('<h5>Instructions:</h5><p>{0}</p>').format(recipe.recipe_instructions)
        html_code += ('</div></div></div></div>')
    
    html_code += ('</div></div></div>') # row

    html_code += ('</div>') # inner

    # controls
    html_code += ('<div class="d-flex justify-content-center mb-4">')
    html_code += ('<button class="carousel-control-prev position-relative" type="button" data-bs-target="#recipeCarousel" data-bs-slide="prev">')
    html_code += ('<span class="carousel-control-prev-icon" aria-hidden="true"></span>')
    html_code += ('<span class="visually-hidden">Previous</span>')
    html_code += ('</button>')
    html_code += ('<button class="carousel-control-next position-relative" type="button" data-bs-target="#recipeCarousel" data-bs-slide="next">')
    html_code += ('<span class="carousel-control-next-icon" aria-hidden="true"></span>')
    html_code += ('<span class="visually-hidden">Next</span>')
    html_code += ('</button>')
    html_code += ('</div>')

    return html_code