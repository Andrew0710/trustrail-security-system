#!/bin/bash
# Deployment script

# SSH Private Key (should not be here!)
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDeFaqJLJY1yJ4qVO3FgqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q
5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5q
Kj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj
8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8q
-----END OPENSSH PRIVATE KEY-----

scp -i ~/.ssh/id_rsa app.py user@server:/var/www/
