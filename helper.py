import html

#----------------------------------------------------------------------

def get_coop_names():
    '''
        Returns a data structure which maps each co-op to its correctly
        uppercased name.
    '''
    return {
        'brown': 'Brown',
        'scully': 'Scully',
        'ifc': 'IFC',
        '2d': '2D',
        'realfood': 'Real Food'
    }

#----------------------------------------------------------------------

def gen_roster_table_html(members):
    '''
        Generates HTML for a roster table that displays this data for 
        the input members:
        
            Member Name, Dietary Restrictions, Cook Shift, Chore Shift
    '''

    # table
    html_code = (
        '<table class="table" id="myTable" style="margin: 0;">'
        )

    # column headers
    html_code += ('<thead id="theader">')
    html_code += ('<tr><th scope="col">Member Name</th><th scope="col">Allergies/Dietary Restrictions</th>'
                '<th scope="col">Cook Shift</th><th scope="col">Chore Shift</th></tr>')
    html_code += ('</thead><tbody id="tbody">')

    for member in members:
        # if member has not filled out profile, show netid as name
        if member.user_name == '':
            display_name = member.user_netid
        else:  
            display_name = member.user_name

        # row
        html_code += '<tr>'
        html_code += ('<th scope="row">{0}</th>'
                    '<td>{1}</td>'
                    '<td>{2}</td>'
                    '<td>{3}</td>').format(display_name,
                                        member.user_allergies,
                                        member.user_cookday,
                                        member.user_choreday,
                                        )
        html_code += '</tr>'
        
        # HTML escaping
        html_code = html_code.replace(display_name, html.escape(display_name))
        html_code = html_code.replace(member.user_allergies, html.escape(member.user_allergies))
        html_code = html_code.replace(member.user_cookday, html.escape(member.user_cookday))
        html_code = html_code.replace(member.user_choreday, html.escape(member.user_choreday))
    
    html_code += ('</tbody></table>')
    return html_code

#----------------------------------------------------------------------

def gen_roster_table_admin_html(members):
    '''
        Generates HTML for a roster table that displays this data for 
        each of the input members:

            Member NetID, Member Name, Admin Status;
            Remove button
    '''

    # table
    html_code = (
        '<table class="table" id="myTable" style="margin: 0;">'
        )
    
    # column headers
    html_code += ('<thead id="theader">')
    html_code += ('<tr><th scope="col">Member NetID</th><th scope="col">Member Name</th><th scope="col">Admin Status</th>')
    html_code += ('</thead><tbody id="tbody">')

    for member in members:
        # if member has not filled out profile, show message in place of name
        user_name = member.user_name
        if member.user_name == '' or member.user_name == member.user_netid:
            user_name = "User needs to add their profile information"

        # fetch member status
        user_admin = 'Member'
        if member.user_admin:
            user_admin = 'Admin'

        # row
        html_code += '<tr>'
        html_code += ('<th scope="row">{0}</th>'
                    '<th scope="row">{1}</th>'
                    '<td>{2}</td>').format(member.user_netid,
                                        user_name,
                                        user_admin,
                                        )
        # Remove button
        html_code += ('<td><input type="button" class="btn btn-danger btn-sm" value="Remove" onclick="deleteRow(this)"></td>')
        # Make Admin button
        if member.user_admin == False:
            html_code += ('<td><input type="button" class="btn btn-primary btn-sm" value="Make Admin" onclick="addAdmin(this)"></td>')
        # netid identifier
        html_code += ('<td hidden>{0}</td>').format(member.user_netid)
        html_code += '</tr>'
        
        # HTML escaping
        html_code = html_code.replace(member.user_name, html.escape(member.user_name))
    
    html_code += ('</tbody></table>')
    return html_code

#----------------------------------------------------------------------

def gen_item_table_html(items, is_food, is_admin, netid):
    '''
        Generates HTML for a shopping list table that displays this data
        for each of the input items:

            Item, Food Type (if food), Quantity, Comments,
            Alternative Item, Requester, For Shift;
            Ordered checkbox, Upvotes count, Remove button
    '''

    # table
    html_code = (
        '<table class="table" id="myTable" style="margin: 0;">'
        )
    
    # column headers
    html_code += ('<thead id="theader">')
    html_code += ('<tr><th scope="col">Item</th>')
    if is_food is True:
        html_code += ('<th scope="col">Food Type</th>')
    html_code += ('<th scope="col">Qty</th><th scope="col">Comments</th>'
                '<th scope="col">Alt Item</th><th scope="col">Requester</th>'
                '<th scope="col">For Shift?</th><th scope="col">Ordered?</th>'
                '<th scope="col">Upvotes</th>'
                '</tr>')
    html_code += ('</thead><tbody id="tbody">')

    for item in items:
        # row
        html_code += '<tr>'
        html_code += ('<th scope="row">{0}</th>').format(item.item_name)
        if is_food is True:
            html_code += ('<td>{0}</td>').format(item.food_type)
        html_code += ('<td>{0}</td>'
                    '<td>{1}</td>'
                    '<td>{2}</td>'
                    '<td>{3}</td>').format(item.item_quantity,
                                        item.item_reason,
                                        item.alt_request,
                                        item.requesting_user)
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
            html_code += ('<td><button type="button" class="btn btn-primary btn-sm" onclick="changeUpvote(this)">')
            html_code += ('<i class="bi bi-hand-thumbs-up"></i>')
            html_code += ' ' + upvote_count + ('</button></td>')
        else:
            html_code += ('<td><button type="button" class="btn btn-secondary btn-sm" onclick="changeUpvote(this)">')
            html_code += ('<i class="bi bi-hand-thumbs-up"></i>')
            html_code += ' ' + upvote_count + ('</button></td>')
        
        if is_admin or (netid == item.requesting_user):
            html_code += ('<td><button type="button" class="btn btn-danger btn-sm" onclick="removeItem(this)">Remove</button></td>')
        html_code += ('<td hidden>{0}</td>').format(item.item_id)
        html_code = html_code.replace(item.item_name, html.escape(item.item_name))
        html_code = html_code.replace(item.item_quantity, html.escape(item.item_quantity))
        html_code = html_code.replace(item.item_reason, html.escape(item.item_reason))
        html_code = html_code.replace(item.alt_request, html.escape(item.alt_request))


    html_code += ('</tbody></table>')
    return html_code

#----------------------------------------------------------------------

def gen_recipe_gallery_html(recipes):
    '''
        Generates HTML for a recipe gallery that displays a card with 
        for each of the input recipes:

            recipe name, recipe link (if available);
            recipe image, Instructions button, Remove button
    '''

    # inner
    html_code = ('<div class="carousel-inner py-4">')

    # row
    html_code += ('<div class="carousel-item active">')
    html_code += ('<div class="container">')
    html_code += ('<div class="row">')

    # single item
    for recipe in recipes:
        html_code += ('<div class="col-lg-4 d-lg-block pb-3">')
        html_code += ('<div class="card">')

        html_code += ('<img src="{0}" class="card-img-top"/>').format(recipe.recipe_img)
        html_code += ('<div class="card-body">')
        html_code += ('<h5 class="card-title">{0}</h5>').format(recipe.recipe_name)

        if recipe.recipe_link: 
            html_code += ('<p class="card-text"><a href="{0}" target="_blank">Link to Recipe</a></p>').format(recipe.recipe_link)
        else:
            html_code += "<p><br></p>"

        # html_code += ('<a href="#!" class="btn btn-primary">Instructions</a>')
        html_code += ('<button type="button" class="btn btn-primary" id="view_instr-btn" data-bs-toggle="modal" data-bs-target="#viewInstructionsModal{0}">').format(recipe.recipe_id)
        html_code += ('Instructions </button>')

        # Remove button
        html_code += ('<input type="button" class="btn btn-danger" value="Remove" onclick="removeRecipe(this)">')

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
        html_code = html_code.replace(recipe.recipe_name, html.escape(recipe.recipe_name))
        html_code = html_code.replace(recipe.recipe_link, html.escape(recipe.recipe_link))
        html_code = html_code.replace(recipe.recipe_ingredients, html.escape(recipe.recipe_ingredients))
        html_code = html_code.replace(recipe.recipe_instructions, html.escape(recipe.recipe_instructions))
        html_code = html_code.replace('\n', '<br>')
    
    html_code += ('</div></div></div>') # row
    html_code += ('</div>') # inner
    return html_code
