# bambu

Unofficial async Python client for BambooHR (work in progress).

### Configuration

    $ cat .env
    DOMAIN = "mycompany"
    TOKEN = "48f95dd"
    # vim: ft=toml

### SBOM

Download and start [DependencyTrack](https://dependencytrack.org) first:

    $ curl -LO https://dependencytrack.org/docker-compose.yml
    $ docker compose up -d
    $ open http://localhost:8080/ 
    
Default pasword is admin/admin, change it after first login to for instance
admin/admin1.

Log in and create a new project and read the _Object Identifier_ from
_Project Details_. Save it as `DT_PROJECT` in `.env`. 

From _Administration_ choose _Access Management_ and subsequently _Teams_.
Create a new team (i.e. SBOM Uploaders) with appropriate permitions. See
_API Keys_ and save as `DT_API_KEY` in `.env`.

Run:

    $ make sbom
    $ cat build/cyclonedx.json

<!---
vim: sw=4:et:ai
-->