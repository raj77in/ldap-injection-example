# ldap-injection-example

1. First you need to install the requirements for the LDAP server. The server is created in python, so
   you need to run: `pip install -r requirements.txt`. **Note**: The LDIF is contained within the
   python script, so if you want to change that, you can modify it in the script.
2. I have also provided another sample LDIF file.
3. Once you have installed the server, you can run it with: `python server.py`
4. Now, you need to install `default-jdk` to have `javac` which is requirement for the client.
5. Once you have javac, you can run the script: `bash ./run-client.sh`. This will compile the client, run a
   query and then show you the command for LDAP injection.

Have fun. You can now try to script this to get the full password with injection.
