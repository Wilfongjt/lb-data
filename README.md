# lb-data
Setup Postgres rest development environment

* registrant-token indentifies the user to the system
* api-token is specific to a set of api methods
* user-token is specific to an application, limits access to api
* app-token ?? this the same as the api-token

# Goal

Allow multiple applications to use the same API

# Requirments
* Provide an application registry by version 
* Provide an app-token for each application by version  
* Provide application specific user registry
* Provide a user-token for each user session

# API Patterns
 | desc   | role | params |  success/fail | example |
 | ------ | ---- | ------ | ------  | ------- |
 | app registration  | anonymous | app(JSONB) | {"results":"1"} {"results":"-1"} | app('{"app-name":"my-app",<br /> "version":"1.0.0",<br /> "username": "aaa@bbb.com",<br /> "password":"\<password\>"}') |
 | get app-token     | anonymous | token(JSONB) | {"results":"\<app-token\>"} {"results":"-1"}  | token('{"app-key":"my-app@1.0.0",  "username":"aaa@bbb.com", "password":"\<password\>"}') |
 | user registration | anonymous | user(TEXT, JSONB) | {"results":"1"} {"results":"-1"} | user('{"app-token":"\<app-token-string\>", "user-name":"xxx@yyy.com", "password":"\<password\>"}') |                                         
 | get user-token    | anonymous | token(JSONB) | {"results":"\<user-token\>"} {"results":"-1"}  | token('{"app-token":"\<app-token-string\>", "user-name":"xxx@yyy.com", "password":"\<password\>"}') |

token-anonymous {"username":"anonymous@register.com",
                 "type":"app",
                 "role":"anonymous"}
                 select ((current_setting('app.lb_register_anonymous')::JSONB - 'password') || ('{"type":"app"}'::JSONB));

# models (TEXT)
models are environment variables
* anonymous-model = {"username":"anonymous@register.com",       
                    "email":"anonymous@register.com", 
                    "password":"g1G!gggg", 
                    "role":"anonymous"}
* registrar-model = {"registrar-name":"registrar@register.com", 
                    "email":"registrar@register.com", 
                    "password":"g1G!gggg", 
                    "role":"registrar", 
                    "app-id":"<>.1.0.0"}
* testregistrar-model  = {"type":"app",
                      "app-id":"my-app@1.0.0",
                      "username":"testuser@register.com",
                      "email":"testuser@register.com",
                      "password":"g1G!gggg",
                      "role":"registrar"}
testuser-model  = {"type":"app",
                      "app-id":"my-app@1.0.0",
                      "username":"testuser@register.com",
                      "email":"testuser@register.com",
                      "password":"g1G!gggg",
                      "role":"user"}
                      
# tokens (TEXT)
Tokens are JSON Web Tokens
* anonymous-token-content = {"username":"anonymous@register.com",       "role":"anonymous"}
* app-token-content       = {"registrar-name":"registrar@register.com", "role":"registrar"}
* user-token-content      = {"username":"<>@<>.<>",                     "role":"user",     "app-id": "<>@<>.<>"}

# forms (JSONB)
A form is client submitted set of attributes
* app-form  = {"app-name":"",  "type":"", "version":"1.0.0", "username":"", "password":""}
* user-form = {"username": "", "type": "user", "password": ""}

# functions
* add application, app(app-form TEXT) return {"username":"anonymous@register.com", "type":"app", "token":"aaaaaa"}
* add application, app(anonymous-token TEXT, app-form JSONB)
* get app-token,   app(anonymous-token TEXT, app-id TEXT) returns {"username":"anonymous@register.com", "type":"app", "token":"aaaaaa"}

* add user,        user(app-token, user-form) 
* get user,        user(app-token, user-credentials) returns {"username":"anonymous@register.com", "type":"user", "token":"uuuuu"}

# Applications
Admin-application is the starting point, 
* register applications 
* get anonymous token 
Client Application
* create users
* update user

# ToDo
app 
function: Insert an application record
parameters
    anonymous-token TEXT
    app-form JSONB
returns {}
    
app
function: Select an application record
parameters:
    anonymous-token TEXT
    app-form JSONB
return {}    

Get anonymous-token from admin application

```
app(form JSONB)
BEGIN
    -- make token
    _token = maketoken
    return app(_token, form)
END

app(token TEXT, form JSONB)
BEGIN
    -- role is 
    -- validate token
    if not is_valid_token(token, expected_role) then
        return '{"result":"0"}'::JSONB;

    -- validate form attributes
    if not(form ? 'app-name') then return '{"results":"-1"}';
    if not(form ? 'version') then return '{"results":"-2"}';
    if not(form ? 'username') then return '{"results":"-3"}';
    if not(form ? 'password') then return '{"results":"-4"}';

    if id in form:
        UPDATE
    else
        -- stop versions
        -- validation checks
        INSERT
END;
```     

# Storage
## Register
    * id(UUID), obj (JSONB), created(TIMESTAMP), updated(TIMESTAMP)
* id, type, attributes, created, updated
id:uuid, type:'app', object:{"type":"app", "name": "<app-name>", "version":"1.0.0", "username":"<username>", "password":"<password>"}
id:uuid, type:'user', object:{"type":"user","name": "<app-name>", "username":"<username>", "password":"<password>"} 

## Tokens
    * id(integer), uuid(UUID), obj (JSONB), created(TIMESTAMP), updated(TIMESTAMP)
 
    * id(integer), key(UUID), obj (JSONB), created(TIMESTAMP), updated(TIMESTAMP)
 
 
 
# Processes
## Register an Application
### register an application,          
    * store application name, user-name, and encrypted password
    * generate and store a reusable application token (app-token)

## Retrieve Token
### retrieve your application's token 
    * an app-token changes when you update your password
    * changing your password for a specific application version will 
    * old tokens are still valid so you wont need to change the app configuration when you change your password 
    * do this once and use it for your web app  
    * configure your application to use the token   >> Devlopment use .env

## Register an Application User
### get an api-token from your app configuration, 
    >>  api-token
    * 
* register new user,              
    

## Retrieve a User Token
* signin and get a user-token                               
    






# Get Started
## Create account, 
we have at least two applications (an admin-app and a primary-app) so account needs to handle multiple applications 
     
                    >> credential({username, password}) 
                    > upsert credentials
                    > add registrant-role
                    > return a registrant-token [ id, username, role:[roles] ]
                    
## Create an application, 
                    >> register(registrant-token, {name, version})
                    > upsert application 
                    > add 'owner:<registrant-id>'
                    > 

## Create user account
                    >> credential(app-token, {username, password})
                    

# Application Tokens
* registrant-token  contains user-identifer, user-access [register-write, register-read]
* api-token         contains application-identifer       []
* user-token        contains user-identifier, application-identifer, user-access   
* app-token         contains application-identifier, 

# Tables
* credentials (id, username, password, row, created, updated)
* register    (id, name, row, created, updated )


# Progression
create credentials                  john@some.com [registrant]
register the "my-app" application   john@some.com [registrant, apps:{app1:[<app-role>,<app-role>,...], app2:[<app-role>,<app-role>,...]]

# Vocabulary
credentials are username and password
version is follows major.minor.patch pattern
applicaton-name is a unique combination of a name, version number, ownername, and password  (e.g. <name>@<version>)
app-token is a token that grants application specific access to the api

administration-application 
primary-app
admin-app

# Application Registration
* An uncredentialed person adds the application-name and personal credentials to the register
* Establishes a unique application identity 
* Pairs up the application and an owner
* Pairs up the Application and the API
* Establishes the person as the application owner
* An owner has rights to update the application's registration
* Creates an app-token for the application
* The app-token grants the right to create an application account, or signin to an application

# User Registration
* An uncredentialed person adds their credentials to access the api that supports the application
* Registration allows the person to request an a user specific api-token aka user-token
* A registered person is known as a registrant



# Registrant Authorization

send Form >> 'id' not in Form   >> sync Form values to table field values 
                                >> remove password 
                                >> insert   
            >> id exists then update table fields found in object
# Thinking

# Configuration Settings
three states of a value
* Undefined means not available eg crud="ru" doesnt provide insert  
* Lowercase means optional e.g., "c"
* Uppercase means required e.g., "C" requires field on insert  

# Imutable
Imutable ("I") values can be created/inserted but not changed/updated. 
Imutables are passed as part of the json object to the API.
Imutables are checked to ensure they have not been changed.
The differnce between "I" and "U", "I" declares imutability whereas the absense of "U", less obviously, implies imutability.
"I" also has the sideeffect of making the API confirm the value has not changed.

# Fields
## Expected Table Field Values 
* "C" in crud = "C" defines a required insert field value
* "c" in crud = "c" defines an optionally insertable table field value
* "c" in crud = "U" defines a required update table field value  
* crud = "u" defines an optionally updateable table field value
* "I" in crud defines an imutable attribute, it can be created and is required for update but cant be updated
* "F" in crud defines a form field, 
    F and C are mutually exclusive, 
    F and U are mutually exclusive, 
    F implies a C,
    F implies a U,
    forms are not passed in a form, 
    a form is assembled, 
    only one Form per record

# Forms
* Forms are JSON objects. 
* Forms are interfaces between client and backend
* Forms 
* The list of Attributes apply to API input objects

## Expected JSON Attributes 
* "C" in json is a required attribute on insert defines a required insertable input Form attribute
* "c" in json defines an optional insertable input Form attribute
* if no "C" or "c" then value cannot be inserted
* "U" in json defines a required updatable input attribute
* "u" in json defines an optional updatable input attribute
* if no "U" or "u" then value cannot be updated
* "I" in json defines an imutable attribute, same as "U" except it cant be upbdated
* "I" in json defines an imutable attribute, it can be created and is required for update but cant be updated
* "D" in json defines an attribute that is not stored in the Form, these are automatically removed from Form 
 
# Partition and Sort Keys
https://aws.amazon.com/blogs/database/choosing-the-right-dynamodb-partition-key/
* json = "P" defines a required partition key
* json = "S" defines a required sort key
* json = "p" defines an optional secondary partition key
* json = "s" defines an optional secondary sort key 

# Defaults 
* default = "<string-value>"
* default = <numeric-value>
* default = "<date-value>"
* default = "<function-name>()"
* default = "<function-name>(_<field-name>)"
* default = <json-object>
* default = <json-list>


# Template Keys
    [[update_combos_format]] update statements, all possible combinations of optional fields
    [[required_update_inputs]]
    [[required_insert_inputs]]
    [[required_insert_inputs]]
    [[insert - values]]
    [[insert - columns]]
    [[insert - sync - json - values]]
    [[set - defaults]]
    [[declare - upsert]]
    [[where - clause]]
    [[set - clause]]
    [[required - insert - attributes]]
    [[insert - parameter - types]]
    [[select - parameter - types]]
    [[update - parameter - types]]
    [[delete-parameter-types]]
    [[select - columns]]
    [[update - columns]]
    [[insert - parameters]]
    [[db-extensions]]
    [[tbl-fields]] table column definitions

# Register an Application
Register your application and get an application-token
```
app_form = {
    "type": "app", 
    "app-name": "my-app", 
    "version": "1.0.0", 
    "username": "abc@xyx.com", 
    "password": <your-password>"
}

register(app_form)
```
# Register a User
Register a user and create a user token
```
# retrieve your application token manually from register table
app_token = '<application-token>'
app_form = {
    "app-name": "my-app", 
    "version": "1.0.0", 
    "username": "abc@xyx.com", 
    "password": "<your-password-here>"
}

user(app_token, form)

```
# Signin 
Signin and get a user-token