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
                '<th scope="col">Cook Shift</th><th scope="col">Chore Shift</th><th scope="col"> </th></tr>')
    html_code += ('</thead><tbody id="tbody">')

    for member in members:
        # don't display members that do not have names
        if member.user_name == '':
            break

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

def genRosterOverviewHTML(members):

    html_code = (
        '<table class="table" id="myTable" style="margin: 0;">'
        )
    
    html_code += ('<thead id="theader">')
    html_code += ('<tr><th scope="col">Member NetID</th><th scope="col">Member Name</th><th scope="col">Admin Status</th>')
    html_code += ('</thead><tbody id="tbody">')

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
        html_code += ('<td><input type="button" class="btn btn-primary btn-sm" value="Remove" onclick="deleteRow(this)"></td>')
        html_code += ('<td hidden>{0}</td>').format(member.user_netid)
        html_code += '</tr>'
    
    html_code += ('</tbody></table>')

    return html_code

#----------------------------------------------------------------------

def genItemTableHTML(items, is_food):
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
                '<th scope="col">Ordered?</th><th scope="col"> </th></tr>')
    html_code += ('</thead><tbody id="tbody">')

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
                                        item.alt_request
                                        )
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
        html_code += ('<td><button type="button" class="btn btn-primary btn-sm" onclick="removeItem(this)">Remove</button></td>')
        html_code += ('<td hidden>{0}</td>').format(item.item_id)

        html_code += '</tr>'
    
    html_code += ('</tbody></table>')

    return html_code