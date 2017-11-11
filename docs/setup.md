1. cookiecutter
2. git clone etag-api
3. docker build -t api . 
	* Important etag-api uses different dependencies
4. Setup postgres
        docker run -it -v <localpath with empty directory>:/var/lib/postgresql/data postgres
        docker exec -it <container> /bin/bash
        psql -U postgres
        create database etag;
        create database etag_auth;
        create user etagadmin with password 'etagadmin';
        GRANT ALL PRIVILEGES ON DATABASE "etag" to etagadmin;
        GRANT ALL PRIVILEGES ON DATABASE "etag_auth" to etagadmin;
