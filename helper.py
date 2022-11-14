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
    html_code += ('<tr><th scope="col">Member Name</th><th scope="col">Allergies/Dietary Restrictions</th>'
                '<th scope="col">Cook Shift</th><th scope="col">Chore Shift</th>')
    html_code += ('</thead><tbody id="tbody">')

    for member in members:
        html_code += '<tr>'

        html_code += ('<th scope="row">{0}</th>'
                    '<td>{1}</td>'
                    '<td>{2}</td>'
                    '<td>{3}</td>').format(member.user_name,
                                        member.user_allergies,
                                        member.user_cookday,
                                        member.user_choreday,
                                        )
        
        html_code += '</tr>'
    
    html_code += ('</tbody></table>')

    return html_code

#----------------------------------------------------------------------

def genItemTableHTML(items):
    '''
        Create HTML code 
    '''
    html_code = (
        '<table class="table" id="myTable" style="margin: 0;">'
        )
    
    html_code += ('<thead id="theader">')
    html_code += ('<tr><th scope="col">Item</th><th scope="col">Type</th>'
                '<th scope="col">Qty</th><th scope="col">Comments</th>'
                '<th scope="col">Alt Item</th><th scope="col">For Shift?</th>'
                '<th scope="col">Fulfilled?</th><th scope="col"> </th></tr>')
    html_code += ('</thead><tbody id="tbody">')

    for item in items:
        html_code += '<tr>'

        html_code += ('<th scope="row">{0}</th>'
                    '<td>{1}</td>'
                    '<td>{2}</td>'
                    '<td>{3}</td>'
                    '<td>{4}</td>').format(item.item_name,
                                        item.item_type,
                                        item.item_quantity,
                                        item.item_reason,
                                        item.alt_request
                                        )
        if item.for_shift is True:
            for_shift = "Yes"
        else:
            for_shift = "No"
        html_code += ('<td>{0}</td>').format(for_shift)
        html_code += ('<td><div class="form-check">'
        '<input class="form-check-input" type="checkbox" value="" id="order-check">')
        if item.item_ordered is True:
            ordered = "Yes"
        else:
            ordered = "No"
        html_code += ('<label class="form-check-label" for="order-check">{0}</label>').format(ordered)
        html_code += ('</div></td>')
        html_code += ('<td><button type="button" class="btn btn-primary btn-sm" id="rm-btn">Remove</button></td>')

        html_code += '</tr>'
    
    html_code += ('</tbody></table>')

    return html_code