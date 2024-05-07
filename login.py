import pymysql.cursors
import json

def lambda_handler(event, context):
    # Connect to the database
    connection = pymysql.connect(host='motormojo.crwa8q8k0lvn.ap-south-1.rds.amazonaws.com',
                                 user='your-username',
                                 password='your-password',
                                 database='your-database',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            for record in event['Records']:
                if record['eventName'] == 'INSERT':
                    # Extract user data from Cognito event
                    user_data = record['dynamodb']['NewImage']
                    
                    # Insert user data into MySQL database
                    sql = "INSERT INTO users (username, email) VALUES (%s, %s)"
                    cursor.execute(sql, (user_data['username']['S'], user_data['email']['S']))
                elif record['eventName'] == 'MODIFY':
                    # Extract modified user data from Cognito event
                    user_data = record['dynamodb']['NewImage']
                    
                    # Update user data in MySQL database
                    sql = "UPDATE users SET email = %s WHERE username = %s"
                    cursor.execute(sql, (user_data['email']['S'], user_data['username']['S']))
    return {
        'statusCode': 200,
        'body': json.dumps('User data stored in MySQL database')
    }
