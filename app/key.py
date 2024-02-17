
# import os
# from secrets import token_bytes
# from base64 import b64encode


# secret_key = b64encode(token_bytes(64)).decode()
# print(f"Generated Secret Key: {secret_key}")

####################################################################################################################

import bcrypt

# Generate a bcrypt hash for an empty string
bcrypt_hash = bcrypt.hashpw(b"", bcrypt.gensalt())

# Trim the bcrypt hash to 64 characters
secret_key = bcrypt_hash.decode()[:64]

print("Bcrypt Secret Key:", secret_key)
####################################################################################################################


# pgadmin user password set DATABASE_URL=postgresql://postgres:WpFYyE0GjCCIey5soRST6Oh45TDCusvMvt6Bm3vdRwxIYm3y8OhuK@localhost:5432/admin_database_pg

# admin secret key: $2b$12$zVz1pCAaCYgFwdExvKJKZu7FFioHaV58/RPHWXSTTLmrRLXOzfOby