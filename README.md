# Installation
Docker (required):
  - Windows:
    + Download Docker: https://www.docker.com/products/docker-desktop/
    + Install: Run Docker Desktop Installer.exe
  - Linux: Run the following command line
    sh install_docker.sh

Docker Desktop (recommended for Windows):
  - Download: https://www.docker.com/products/docker-desktop/

# Execution
  - To run start the server, run this commands:
    + docker-compose up -d
  - Dockerfile configuration at the moment is not able to auto run the file for importing data to the database. If you are having the same situation on you computer, please proceed as follow:
    1. The webserver container name by default is "webserver_my_server_1". If it is in your case, please proceed to the next step.
      1.1. To get the webserver container name, run this command: docker container ls -a
      1.2. You can use either the container id or container name for the next step.
    2. Go into the container in interactive mode: docker exec -it <container's name> sh
    3. Go into the folder "root/tools": cd /root/tools
    4. Run the file "csv2pgsql_JP.py" to import the data: python3 csv2pgsql_JP.py