BEGIN;
  SELECT plan(2);

  -- insert
  SELECT is ( reg_schema.user( sign('{"username": "testuser@register.com", "role": "anonymous"}'::json, current_setting('app.jwt_secret')), '{"type": "user", "app-id": "my-test-app@1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}'::JSONB )::JSONB, '{"status": "200", "msg": "ok"}'::JSONB, 'user - insert test'::TEXT );

  -- select
  SELECT matches(
  					reg_schema.user(
  						sign('{"username": "testuser@register.com", "role": "anonymous"}'::json,
  						current_setting('app.jwt_secret')
  					),
                    '{"id": "my-test-app@1.0.0"}'::JSONB
                )::TEXT,
                '[a-zA-Z\.0-9_]+',
                'user - select from register by id and check token'::TEXT );

  SELECT * FROM finish();

ROLLBACK;

---------------------
Select regexp_matches (('{"result": {"test": "insert", "type": "app", "email": "test@register.com", "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAtbmFtZSI6Im15LXRlc3QtYXBwIiwgInZlcnNpb24iOiIxLjAuMCIsICJyb2xlIjoicmVnaXN0cmFyIn0.X8lz4Vday09EV6J0b3TN6CxJ2ViJWp_EZAlswJ2ouDw", "version": "1.0.0", "app-name": "my-test-app", "username": "testuser@register.com"}, "status": "200"}'::JSONB ->> 'result')::JSONB ->> 'token', '[a-zA-Z\.0-9_]+');

SELECT regexp_matches('{"status": "200", "result": "asxc2345."}', '{"status": "200", "result": "[a-z\.0-9_]+"}');


SELECT regexp_matches('{"result": "asdf", "status": "200"}', '{"result": "[a-z]+", "status": "200"}');



---------------------------


CREATE OR REPLACE FUNCTION
reg_schema.app(_token TEXT, _form_text TEXT) RETURNS JSONB
AS $$
  DECLARE rc TEXT;
  DECLARE secret TEXT;
  DECLARE rc_form JSONB;
  DECLARE _model_user JSONB;

  Declare _id TEXT;Declare _type TEXT;Declare _form JSONB;Declare _password TEXT;Declare _active BOOLEAN;Declare _created TIMESTAMP;Declare _updated TIMESTAMP;

BEGIN

    -- returns a single user's info
    -- need to figure out postgres environment variables

    _model_user := current_setting('app.lb_register_anonymous')::jsonb;

    -- figure out which token: app-token or user-token
    if not(reg_schema.is_valid_token(_token, _model_user ->> 'role')) then
        return '{"result": "0"}'::JSONB;
    end if;

    -- convert Text to JSONB to ref
    _form := _form_text::JSONB;

    -- confirm proper attributes in _form
    if not(_form ? 'id') then
        return '{"resutl":"-2", "msg":"bad id"}'::JSONB;
    end if;

    _id = _form ->> 'id';

    -- go get the data

    select reg_form
    into rc_form
    from reg_schema.register
    where reg_id= _id;

    if rc_form is NULL then
      rc_form := '{"result":-1}'::JSONB;
    else
      rc_form :=  format('{"result":%s}',rc_form::TEXT)::JSONB;
    end if;

    RETURN rc_form;
END;  $$ LANGUAGE plpgsql;

-- add app
Select
 reg_schema.app(
      sign('{"username": "testuser@register.com", "role": "anonymous"}'::json, current_setting('app.jwt_secret')),
      '{"type": "app", "app-name": "my-test-app", "version": "1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}'::JSONB
    )::JSONB
    ;
select
reg_schema.app(
      sign('{"username": "testuser@register.com", "role": "anonymous"}'::json, current_setting('app.jwt_secret')),
      '{"id": "my-test-app@1.0.0"}'::TEXT
    )::JSONB
    ;

select reg_form
    from reg_schema.register
    where reg_id= 'my-test-app@1.0.0';
------------------------------------



select ((current_setting('app.lb_register_anonymous')::JSONB - 'password') || ('{"type":"app"}'::JSONB));

select current_setting('app.lb_register_anonymous')::JSONB ->> 'username';

select ((current_setting('app.lb_register_anonymous')::JSONB - 'password') || '{"type":"app"}'::JSONB);

select current_setting('app.lb_register_anonymous');
select current_setting('app.lb_register_jwt');


select '{"type": "app", "app-name": "my-app", "version": "1.0.0", "username": "abc@xyx.com", "password": "t1T!tttt"}'::JSONB ->> 'type';


reg_schema.app(
      sign('{"username":"testuser@register.com","role":"anonymous"}'::json, current_setting('app.jwt_secret')),
      '{"type": "app", "app-name": "my-app", "version": "1.0.0", "username": "abc@xyx.com", "password": "t1T!tttt"}'::JSONB
    )::JSONB

select sign('{"username":"testuser@register.com","role":"registrant"}'::json, current_setting('app.jwt_secret'));

select reg_schema.app('{"type": "app", "app-name": "my-test-app", "version": "1.0.0", "username": "testuser@register.com", "email": "test@register.com", "password": "g1G!gggg", "test": "insert"}'::JSONB);

--\c reg_db
-- insert a test user
select reg_schema.app(

	format('{"type":"%s", "app-name":"%s" , "version": "%s", "username":"%s", "password":"%s"}'::TEXT,
			current_setting('app.lb_register_testuser')::jsonb->>'type',
			current_setting('app.lb_register_testuser')::jsonb->>'app-name',
			current_setting('app.lb_register_testuser')::jsonb->>'version',
			current_setting('app.lb_register_testuser')::jsonb->>'username',
			current_setting('app.lb_register_testuser')::jsonb->>'password'
		  )::JSONB

);

select 	format('{"type":"%s", "app-name":"%s" , "version": "%s", "username":"%s", "password":"%s"}'::TEXT,
			current_setting('app.lb_register_testuser')::jsonb->>'type',
			current_setting('app.lb_register_testuser')::jsonb->>'app-name',
			current_setting('app.lb_register_testuser')::jsonb->>'version',
			current_setting('app.lb_register_testuser')::jsonb->>'username',
			current_setting('app.lb_register_testuser')::jsonb->>'password'
		  )::JSONB;

select current_setting('app.lb_register_testuser')::JSONB;

select 			current_setting('app.lb_register_testuser')::jsonb->>'type';


select format('{"type":"%s", "app-name":"%s" , "version": "%s", "username":"%s", "password":"%s"}'::TEXT,

			current_setting('app.lb_register_testuser')::jsonb->>'type',

			current_setting('app.lb_register_testuser')::jsonb->>'app-name',

			current_setting('app.lb_register_testuser')::jsonb->>'version',

			current_setting('app.lb_register_testuser')::jsonb->>'username',

			current_setting('app.lb_register_testuser')::jsonb->>'password'

		  )::JSONB;



select	reg_schema.get_app_id(current_setting('app.lb_register_testuser')::jsonb->>'app-name','1.0.0');

select current_setting('app.lb_register_testuser')::jsonb->>'app-name';

select reg_id into id from reg_schema.register
    where reg_form ->> 'form' = 'my-app'
        and reg_form ->> 'version' = '1.0.0' ;


select * from reg_schema.register;
select reg_id  from reg_schema.register where reg_form->>'version'='1.0.0' and reg_form->>'app-name'='my-app';


CREATE OR REPLACE FUNCTION reg_ins_upd_trigger_func() RETURNS trigger

AS $$

Declare _token TEXT;

Declare _custom JSON;

Declare _form JSONB;

BEGIN

   -- create application token

    IF (TG_OP = 'INSERT') THEN


        _custom := format('{"app-name":"%s", "version":"%s", "role":"registrar"}',

                    NEW.reg_form ->> 'app-name',

                    NEW.reg_form ->> 'version')::JSON;

        _token := sign( _custom::JSON, current_setting('app.jwt_secret'),  'HS256'::text);

        _form := format('{"token": "%s"}',_token)::JSONB;

        NEW.reg_form := NEW.reg_form || _form;


    ELSEIF (TG_OP = 'UPDATE') THEN

       NEW.reg_updated := CURRENT_TIMESTAMP;

    END IF;

    RETURN NEW;

END; $$ LANGUAGE plpgsql;



INSERT

  INTO reg_schema.register

  (

    reg_type, reg_password, reg_form
  ) VALUES (

    'app', 'a1A!aaaa', '{"type": "app", "version": "1.0.0", "app-name": "my-app", "username": "testuser@register.com"}'::JSONB
  );

INSERT

  INTO reg_schema.register

  (

    reg_type, reg_password, reg_form
  ) VALUES (

    'user', 'a1A!aaaa', '{"type": "user", "version": "1.0.0", "app-name": "my-app", "username": "testuser@register.com"}'::JSONB
  );



select '##### register TESTS';

BEGIN;

  SELECT plan(5);

  select '###### register';

  select '############################################## Upsert ';

  select '######################################## INSERT {}';

  SELECT is (

    reg_schema.register(

      sign('{"username":"testuser@register.com","role":"registrant"}'::json, current_setting('app.jwt_secret')),

      '{"type": "app", "app-name": "my-app", "version": "1.0.0", "username": "abc@xyx.com", "password": "t1T!tttt"}'::JSONB

    )::JSONB,

    '{"result": "1"}'::JSONB,

    'register testuser@request.com UPSERT'::TEXT

  );

  select '######################################## INSERT {}';

  SELECT is (

    reg_schema.register(

      sign('{"username":"testuser@register.com","role":"registrant"}'::json, current_setting('app.jwt_secret')),

      '{"type": "app", "app_id": "e53229aa-d09c-4cec-b566-ea553ae8078d", "username": "abc@xyx.com", "password": "t1T!tttt"}'::JSONB

    )::JSONB,

    '{"result": "1"}'::JSONB,

    'register testuser@request.com UPSERT'::TEXT

  );

  select '#############################################';

  SELECT * FROM finish();

  select '##### register TESTS Done';

ROLLBACK;


-- add new user
select reg_schema.register(
		format('{"type":"%s", "app-name":"%s" , "version": "%s", "username":"%s", "password":"%s"}'::TEXT,
				current_setting('app.lb_register_testuser')::jsonb->>'type',
			current_setting('app.lb_register_testuser')::jsonb->>'app-name',
				current_setting('app.lb_register_testuser')::jsonb->>'version',
				current_setting('app.lb_register_testuser')::jsonb->>'username',
 				current_setting('app.lb_register_testuser')::jsonb->>'password'
		  )::JSONB
 	);


select format('{"type":"%s", "app-name":"%s" , "version": "%s", "username":"%s", "password":"%s"}'::TEXT,
		current_setting('app.lb_register_testuser')::jsonb->>'type',
		current_setting('app.lb_register_testuser')::jsonb->>'app-name',
		current_setting('app.lb_register_testuser')::jsonb->>'version',
		current_setting('app.lb_register_testuser')::jsonb->>'username',
		current_setting('app.lb_register_testuser')::jsonb->>'password'
	  )::JSONB;


select sign('{"app-name":"xxx", "version":"111", "role":"registrar"}'::JSON, current_setting('app.jwt_secret'),  'HS256'::text);



INSERT

  INTO reg_schema.register

  (

    reg_type, reg_password, reg_form
  ) VALUES (

    'app', 'a1A!aaaa', '{"type": "app", "version": "1.0.0", "app-name": "my-app", "username": "testuser@register.com"}'::JSONB
  );


select
'{' ||
format('"id":"%s"',reg_id) || format('"type":"%s"',reg_type) || format('"active":"%s"',reg_active) || format('"created":"%s"',reg_created) || format('"updated":"%s"',reg_updated)

|| '}'
from reg_schema.register

select
'hu' as obj
from reg_schema.register





CREATE OR REPLACE FUNCTION

reg_schema.register(_token TEXT, _json JSONB) RETURNS JSONB

AS $$

    Declare rc jsonb;

    Declare _cur_row JSONB;

    Declare _guest JSONB;

    Declare _registrant JSONB;

    Declare _app_id TEXT;

Declare _id UUID;
Declare _type TEXT;
Declare _password TEXT;
Declare _attributes JSONB;
Declare _created TIMESTAMP;
Declare _updated TIMESTAMP;
Declare _active BOOLEAN;
  BEGIN

    _guest := current_setting('app.lb_register_guest')::jsonb;

    _registrant :=  current_setting('app.lb_register_registrant')::jsonb;

    -- figure out which token: app-token or user-token

    if reg_schema.is_valid_token(_token, _registrant ->> 'role') then

		rc := '{"result":"2"}'::JSONB;

    elsif reg_schema.is_valid_token(_token, _guest ->> 'role') then

		rc := '{"result":"1"}'::JSONB;

    else

        return '{"result": "0"}'::JSONB;

    end if;

    -- update or insert

    if

    	_json ? 'id'

    then

    	--update

    	rc := '{"result":"-2"}'::JSONB;

        -- check required attributes by type

            if _json ? 'type' then
              if _json ->> 'type' = 'app' then

                  -- all of these
                  if not(_json ? 'id' and _json ? 'type' and _json ? 'app-name' and _json ? 'version') then return '{"result":"-2"}'::JSONB; end if;
                  -- at least one of these
                  if not(_json ? 'username' or _json ? 'password') then return '{"result":"-2"}'::JSONB; end if;

              elsif _json ->> 'type' = 'user' then

                  -- all of these
                  if not(_json ? 'id' and _json ? 'type' and _json ? 'app_id') then return '{"result":"-2"}'::JSONB; end if;
                  -- at least one of these
                  if not(_json ? 'username' or _json ? 'password') then return '{"result":"-2"}'::JSONB; end if;

              else
                   return '{"result": "-2"}'::JSONB;
              end if;
            else
                 return '{"result": "-2"}'::JSONB;
            end if;
		-- get current json object

		select reg_row as _usr

		  into _cur_row

		  from reg_schema.register

		  where

            reg_id= cast(_json::jsonb ->> 'uuid' as UUID)
            ;
        rc := '{"result":"-2.1"}'::JSONB;

        -- handle the changes to base table

		-- update table object with input values

        BEGIN

            -- sync-json-values to table values

            -- all possible update combinations of updatable fields

            if _json ? 'password' and _json ? 'active' then
               update reg_schema.register
                set  reg_password = _password,  reg_active = _active,  reg_attributes = _attributes
                where
                   reg_id= cast(_json::jsonb ->> 'uuid' as UUID)
                   ;
            elsif _json ? 'active' then
               update reg_schema.register
                set  reg_active = _active,  reg_attributes = _attributes
                where
                   reg_id= cast(_json::jsonb ->> 'uuid' as UUID)
                   ;
            elsif _json ? 'password' then
               update reg_schema.register
                set  reg_password = _password,  reg_attributes = _attributes
                where
                   reg_id= cast(_json::jsonb ->> 'uuid' as UUID)
                   ;
            else
               update reg_schema.register
                set  reg_attributes = _attributes
                where
                   reg_id= cast(_json::jsonb ->> 'uuid' as UUID)
                   ;
            end if;
        EXCEPTION

		    WHEN check_violation then

		        rc := '{"result":"-2.2"}'::JSONB;

		    WHEN others then

		        rc := '{"result":"-2.2"}'::JSONB;

        END;

		if not FOUND then

		  return format('{"result":"-2.2"}')::JSONB;

		end if;

	    rc := '{"result":"2"}'::JSONB;

    else

    	BEGIN

    	    -- check required attributes by type

            if _json ? 'type' then
              if _json ->> 'type' = 'app' then

                  -- all of these on insert
                  if not(_json ? 'type' and _json ? 'app-name' and _json ? 'version' and _json ? 'username' and _json ? 'password') then return '{"result":"-1"}'::JSONB; end if;
                  -- required insert columns
                  if not(_json ? 'type' and _json ? 'password') then return '{"result":"-1"}'::JSONB; end if;

              elsif _json ->> 'type' = 'user' then

                  -- all of these on insert
                  if not(_json ? 'type' and _json ? 'app_id' and _json ? 'username' and _json ? 'password') then return '{"result":"-1"}'::JSONB; end if;
                  -- required insert columns
                  if not(_json ? 'type' and _json ? 'password') then return '{"result":"-1"}'::JSONB; end if;

              else
                 return '{"result": "-1"}'::JSONB;
              end if;
            else
                 return '{"result": "-1"}'::JSONB;
            end if;
    	    -- set defaults just in case

            /*
               -- unquoted types ['INTEGER', 'BOOLEAN']
               -- quoted types   ['TEXT', 'TIMESTAMP']
               -- json types     ['JSONB']
               --  set default in field to include
            */
            _active = true;

            -- sync json values to table values

            -- required sync assignments
            if _json ? 'type' then _type := _json ->> 'type'; else return '{"result":"-1"}'::JSONB; end if;
            if _json ? 'password' then _password := _json ->> 'password'; else return '{"result":"-1"}'::JSONB; end if;
            -- sync attributes to object
            _attributes := _json - 'password';
            -- validate

            if length(_password) < 8 then

                return '{"result":"-1"}'::JSONB;

            end if;

            -- remove pw before inserting

			rc := '{"result":"-1"}'::JSONB;

			--insert-statement

			INSERT

              INTO reg_schema.register

              (

                reg_type, reg_password, reg_attributes
              ) VALUES (

                _type, _password, _attributes
              );

            rc := '{"result":"1"}'::JSONB;

		EXCEPTION

		    WHEN unique_violation THEN

		        rc := '{"result":"-1"}'::JSONB;

		    WHEN check_violation then

		        rc := '{"result":"-1"}'::JSONB;

		    WHEN others then

		        rc := '{"result":"-1"}'::JSONB;

		END;

    end if;

    RETURN rc;

  END;

$$ LANGUAGE plpgsql;

GRANT EXECUTE ON FUNCTION

  reg_schema.register(

  TEXT, JSONB

  ) TO anonymous;




select current_setting('app.lb_register_testuser')::jsonb->>'username'
select current_setting('app.lb_register_testuser')::jsonb->>'password'
select format('{"username":"%s", "password":"%s"}'::TEXT,
			current_setting('app.lb_register_testuser')::jsonb->>'username',
			current_setting('app.lb_register_testuser')::jsonb->>'password'
		  )::JSONB;

select reg_schema.credential(
	format('{"username":"%s", "password":"%s"}'::TEXT,
			current_setting('app.lb_register_testuser')::jsonb->>'username',
			current_setting('app.lb_register_testuser')::jsonb->>'password'
		  )::JSONB

);




CREATE OR REPLACE FUNCTION

reg_schema.register(_token TEXT, _json JSONB) RETURNS JSONB

AS $$
    Declare rc jsonb;
    Declare _cur_row JSONB;
    Declare _guest JSONB;
    Declare _registrant JSONB;
    -- declare-upsert
Declare _id UUID;
Declare _type TEXT;
Declare _attributes JSONB;
Declare _created TIMESTAMP;
Declare _updated TIMESTAMP;
Declare _active BOOLEAN;
  BEGIN
    _guest := current_setting('app.lb_register_guest')::jsonb;
    _registrant :=  current_setting('app.lb_register_registrant')::jsonb;
    -- figure out which token: app-token or user-token
    if reg_schema.is_valid_token(_token, _registrant ->> 'role') then
		rc := '{"result":"2"}'::JSONB;
	elsif reg_schema.is_valid_token(_token, _guest ->> 'role') then
		rc := '{"result":"1"}'::JSONB;
    else
        return '{"result": "0"}'::JSONB;
    end if;
    -- update or insert
    if
    	_json ? 'id'
    then
    	--update
    	rc := '{"result":"-2"}'::JSONB;
    	/*
		-- get current json object
		select reg_row as _usr
		  into _cur_row
		  from reg_schema.register
		  where
            reg_id= cast(_json::jsonb ->> 'uuid' as UUID)
            ;
        rc := '{"result":"-2.1"}'::JSONB;
		-- update existing json object with input values
        BEGIN
            -- sync-json-values to table values
            -- update_combos_format
            else
              update
                  reg_schema.register
                set
                   reg_attributes = _attributes
                where
                   reg_id= cast(_json::jsonb ->> 'uuid' as UUID)
                   ;
            end if;
        EXCEPTION
		    WHEN check_violation then
		        rc := '{"result":"-2.2"}'::JSONB;
		    WHEN others then
		        rc := '{"result":"-2.2"}'::JSONB;
        END;
		if not FOUND then
		  return '{"result":"-2.2"}'::JSONB;
		end if;
	    rc := '{"result":"2"}'::JSONB;
	    */
    else
    	BEGIN
    	    -- check required attributes
    	    -- set defaults just in case
            _type = 'app'::TEXT;
            _active = true;
            -- sync json values to table values
            -- validate
            if length(_password) < 8 then
                return '{"result":"-1"}'::JSONB;
            end if;
            -- remove pw before inserting
    	    _row = _json - 'password';
			rc := '{"result":"-1"}'::JSONB;
			--insert-statement
			INSERT
              INTO reg_schema.register

              (
                reg_type, reg_attributes
              ) VALUES (
                _type, _attributes
              );
            rc := '{"result":"1"}'::JSONB;
		EXCEPTION
		    WHEN unique_violation THEN
		        rc := '{"result":"-1"}'::JSONB;
		    WHEN check_violation then
		        rc := '{"result":"-1"}'::JSONB;
		    WHEN others then
		        rc := '{"result":"-1"}'::JSONB;
		END;
    end if;
    RETURN rc;
  END;
$$ LANGUAGE plpgsql;





select format('{"username":"%s", "password":"%s"}'::TEXT,

			current_setting('app.lb_register_testuser')::jsonb->>'username',

			current_setting('app.lb_register_testuser')::jsonb->>'password'

		  )::JSONB;


select reg_schema.credential(

	format('{"username":"%s", "password":"%s"}'::TEXT,

			current_setting('app.lb_register_testuser')::jsonb->>'username',

			current_setting('app.lb_register_testuser')::jsonb->>'password'

		  )::JSONB

);





select reg_schema.credential(
	format('{"username":"%s", "password":"%s"}'::TEXT,
			current_setting('app.lb_register_testuser')::jsonb->>'username',
			current_setting('app.lb_register_testuser')::jsonb->>'password'
		  )::JSONB

);


select length(crd_password)>8;

-- add good user , bad password
select reg_schema.credential(
    sign(
      '{"username":"guest@register.com",
        "role":"guest"}'::json,current_setting('app.jwt_secret')
    ),
    '{"username":"bad@register.com"}'::jsonb
  )::JSONB;



CREATE OR REPLACE FUNCTION
reg_schema.credential(_token TEXT, _json JSONB) RETURNS JSONB
AS $$
	-- insert {username:"AA@AA.AAA", password:""}
    -- update {id:N, username:"AA@AA.AAA", password: ""}
    Declare rc jsonb;
    Declare _cur_row JSONB;
    -- Declare _username TEXT;
    -- Declare _password TEXT;
    Declare _guest JSONB;
    Declare _registrant JSONB;

Declare _id INTEGER;
Declare _username TEXT;
Declare _email TEXT;
Declare _password TEXT;
Declare _roles JSONB;
Declare _row JSONB;
Declare _created TIMESTAMP;
Declare _updated TIMESTAMP;
Declare _active BOOLEAN;
  BEGIN
    _guest := current_setting('app.lb_register_guest')::jsonb;
    _registrant :=  current_setting('app.lb_register_registrant')::jsonb;

    -- insert and update tokens are different
    -- insert tokens are an application token
    -- update tokens are a user token
    -- figure out which token: app-token or user-token

    if reg_schema.is_valid_token(_token, _registrant ->> 'role') then
		rc := '{"result":"2"}'::JSONB;
	elsif reg_schema.is_valid_token(_token, _guest ->> 'role') then
		rc := '{"result":"1"}'::JSONB;
    else
        return '{"result": "0"}'::JSONB;
    end if;

    -- required _json insert attributes
    -- update or insert

    if
    	_json ? 'id'
    then
    	--update
    	rc := '{"result":"-2"}'::JSONB;
		-- get current json object
		select crd_row as _usr
		  into _cur_row
		  from reg_schema.credentials
		  where
            crd_id= cast(_json::jsonb ->> 'id' as integer) and crd_username=reg_schema.get_username(_token)::TEXT
            ;
        rc := '{"result":"-2.1"}'::JSONB;

		-- update existing json object
		if _cur_row ? 'username' and _json ? 'username' then
		   _cur_row := jsonb_set(_cur_row, '{username}'::TEXT[], format('"%s"',_username)::jsonb, TRUE) ;
        end if;

		-- if then

		--   _cur_row := jsonb_set(_cur_row, '{email}'::TEXT[], format('"%s"',_email)::jsonb, TRUE) ;

        if _json ? 'username' then
            _username = _json ->> 'username';
        end if;

        _row = _json - 'password';

		-- update
		---- expect id in _json
		---- remove password from _json before updating
		---- merge roles when needed
		update reg_schema.credentials
		  set
            crd_username=_username, crd_password=_password, crd_row=_row
		  where
            crd_id= cast(_json::jsonb ->> 'id' as integer) and crd_username=reg_schema.get_username(_token)::TEXT
            ;
		if not FOUND then
		  return format('{"result":"-2.2"}')::JSONB;
		end if;
	    rc := '{"result":"2"}'::JSONB;

    else
    	-- insert
    	-- username
    	-- password
    	-- roles start with registrant
    	-- add user data

    	BEGIN
    	    -- set defaults just in case
            _active = true;
            _roles = '["registrant"]'::JSONB;

            -- sync json values to table values
            _username := _json ->> 'username';
            _password := _json ->> 'password';

            -- remove pw before inserting
    	    _row = _json - 'password';

			rc := '{"result":"1"}'::JSONB;

			-- tranfer obj data to row data

			--insert-statement
			INSERT
              INTO reg_schema.credentials
              (
                crd_username, crd_password, crd_row
              ) VALUES (
                _username, _password, _row
              );

		EXCEPTION
		    WHEN unique_violation THEN
		        rc := '{"result":"-1.1"}'::JSONB;
		    WHEN check_violation then
		        rc := '{"result":"-1.2"}'::JSONB;
		END;
    end if;
    RETURN rc;
  END;
$$ LANGUAGE plpgsql;


---------------------------------------------------

select reg_schema.validate_password('ccccccc');

-- select reg_schema.credential('"username":(current_setting('app.lb_register_testuser')::jsonb-'password')::jsonb - 'role');

select reg_schema.credential(
	format('{"username":"%s", "password":"%s"}'::TEXT,
			current_setting('app.lb_register_testuser')::jsonb->>'username',
			current_setting('app.lb_register_testuser')::jsonb->>'password'
		  )::JSONB

);
select format('{"username":"%s", "password":"%s"}'::TEXT,
			current_setting('app.lb_register_testuser')::jsonb->>'username',
			current_setting('app.lb_register_testuser')::jsonb->>'password'
		  )::jsonb	;

-- simple assignment, right to left
select '{"a":1}'::JSONB || '{"a": 2}';  -- right to left assignment

select '{"a":2}'::JSONB || '{"a": 1}';  -- right to left assignment
--
select '{"a":2, "b":"b", "c": "cat", "roles":["reg"]}'::JSONB || '{"a": 1, "b": "B", "roles":["guest"]}';
select '{"a":2, "b":"b", "c": "cat", "roles":["reg"]}'::JSONB || '{"d": 1, "e": "B", "g":["guest"]}';


select '{"a":"a"}'::JSONB || '{"a":"a"}'::JSONB ; -- '{"a":"a"}'::JSONB
select '{"a":"1", "b":"2"}'::JSONB || '{"a":"b"}'::JSONB ; -- '{"a":"b"m "b":"2"}'::JSONB
select '{"a":"1", "b":"2"}'::JSONB || '{}'::JSONB ; -- '{"a":"1", "b":"2"}'::JSONB

-- lists
-- concat list attributes together before the high level attributes

select jsonb_insert('{"a": [0,1,2]}', '{a, 3}', '"new_value"'); -- jsonb_insert(target-json, attribute/position, insert-value)

select jsonb_insert('{"a":2, "roles":["reg"]}'::JSONB ,'{roles,999}', '"guest"'); -- jsonb_insert(target-json, attribute/position, insert-value)
select jsonb_insert('{"a":2, "roles":["reg"]}'::JSONB ,'{roles,999}', ('{"role":"guest"}'::JSONB -> 'role')::JSONB);

select '{"role":"guest"}'::JSONB -> 'role';

select jsonb_set('[{"f1":1,"f2":null},2,null,3]', '{0,f1}','[2,3,4]', false);

DO $$
select reg_schema.credential('{"username":"b@a.com", "email": "b@a.com", "password":"a1A!aaaa"}');

	Declare _json JSONB;
    Declare _cur_json JSONB;
    Declare _role JSONB;
	BEGIN
		_json := '{"id":"1","username":"b@a.com", "password":"a1A!aaaa"}'::JSONB;
		_cur_json := '{"username":"b@a.com", "email": "b@a.com"}'::JSONB;
		if _json ? 'id' then
			if _json ? 'role' then
				_role := _json->'role';

				_cur_json := jsonb_insert(
					_cur_json,
					'{roles, 999}'::TEXT[],
					_role
				);

			end if;
		end if;

	END

$$

-- Rmove b attribute
select '["a", {"b":1}]'::jsonb #- '{1,b}';
-- pluck roles and remove first attribute
select ('{"a":"ab", "roles":["guest"]}'::jsonb -> 'roles') #- '{0}';
--
select ('{"a":"ab", "roles":["guest","goat"]}'::jsonb -> 'roles') #- '{"guest"}'; --broke

-- Merge objects
select
	'{"username":"ab", "roles":["guest","reg"]}'::jsonb ||
	'{"username":"ab", "email":"new@x.com"}'::jsonb
;

select '{"a":"ab", "roles":["guest"]}'::jsonb #- '{0,roles}';
-- Use Cases
-- Create new user
-- Change existing user

-- PREDICATES
-- is implies a one to one interchangeable meaning
-- isA implies a type
-- isDefinedBy describes an immergent property
-- contains defines a list of contents
-- isRegExp defines the pattern of datum

-- DATABASE
-- database-environment isDefinedBy database-software
-- database-software is Postgres
-- Postgres isA database-software
-- pg is Postgres

-- TABLES
-- Credentials isA table
-- Credentials is crd
-- crd is Credentials
-- Credentials contains crd_id, crd_username, crd_row, crd_created, crd_updated

-- INSERTS
-- Insert is ins
-- ins is Insert
-- Credentials-Insert is crd-ins
-- crd-ins is Credentials-Insert

-- credentials-ins requires a register-guest-token
-- Insert-pattern is credential(<new-user-fo>) or credential(<register-guest-token>, <new-user-fo>)

-- UPDATES

-- OBJECTS
--

-- PATTERNS
-- crd-insert-pt is credential(<new-user-fo>) or credential(<register-guest-token>, <new-user-fo>)
-- crd-update-pt is credential(credential(<register-guest-token>, <new-user-fo>)