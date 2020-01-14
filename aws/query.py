from tabulate import tabulate
import boto3
import inquirer

client = boto3.client('ec2')

# Create simple pagination function (looks like the new API's in Boto3 don't have them natively yet)


def paginate(operation, key, args={}):

    results = []
    next_token = None
    operation_args = args

    # Start a loop to work through all paginated results
    while True:

        # Check if we have a next token (used to paginate)
        if next_token:
            # If so, set up our API arguments to include the token
            operation_args['NextToken'] = next_token

        # Make the API call based on the passed in operation and the arguments to use.
        call = getattr(client, operation)(**operation_args)
        #  Add the results to our list of results (based on the key argument)
        results.extend(call[key])

        # Update the next token (if there is one)
        next_token = call.get('NextToken')
        if not next_token:
            # If there isn't, that's all of our results - return them.
            return results


# Get all the instance types using the new DescribeInstanceTypeOfferings API
instance_types = paginate(To
                          operation='describe_instance_type_offerings',
                          key='InstanceTypeOfferings')

# Set up a Map of attributes a user can request to compare
# Also allows us to provide "Friendly" table headers later
attribute_map = {'Hibernation Supported': 'HibernationSupported', 'Hypervisor': 'Hypervisor', 'Free Tier': 'FreeTierEligible', 'Current Generation': 'CurrentGeneration',
                 'Bare Metal': 'BareMetal'
                 }

# Using inquirer, setup a checkbox selection from the instance types we got back
# Our choices will be only the InstanceType key from every result, sorted.
questions = [
    inquirer.Checkbox(
        'i_types', "What Types do you want to know more about?", choices=sorted([x['InstanceType'] for x in instance_types])),
    inquirer.Checkbox(
        'attributes', "Which Attributes would you like to compare?", choices=sorted(attribute_map.keys())
    )
]

# Get the Input from a user
answers = inquirer.prompt(questions)

# Get All the extra info about the selected instances using the new DescribeInstanceTypes API
extra_info = paginate('describe_instance_types', 'InstanceTypes', args={
    'InstanceTypes': answers['i_types']
})

# Create the table rows based on the user input
rows = []

# Loop through each selected InstanceType
for instance_type in extra_info:
    # Add a row to rows, where each row is a list of values
    # We prepend the Instance Type as this is not a user selectable row but we want to include it in all rows.
    row = [instance_type['InstanceType']] + \
        [instance_type.get(attribute_map[i]) for i in answers['attributes']]

    # Add our row to a list of rows
    rows.append(row)

# Print out a table with the rows and our coloumns based on the user input + the Instance Type
print(tabulate(rows, headers=['Instance Type'] + answers['attributes']))
