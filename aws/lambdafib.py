import json

def lambda_handler(event, context):
    print ("Calc Fib(100000)")
    return {
        'statusCode': 200,
        'body': json.dumps(fib(100000))
    }
    
# This is much faster than the recursive version.
#
def fib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a+b
    return a
