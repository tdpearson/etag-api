Cybercommons API Docker Build 
===
Django Rest API which includes Tasks, Catalog, Local Data Store


Docker api works in conjuction with docker cybercom/celery image.

Installation:
 1. Install [Cybercommons](https://github.com/cybercommons/cybercom-cookiecutter)
    Installation instructions can be found at [docs](http://cybercom-docs.readthedocs.io/en/latest/installation.html)
 2. git clone [etag-api](https://github.com/etag/etag-api)
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
 5. git clone [portal](https://github.com/etag/portal)
