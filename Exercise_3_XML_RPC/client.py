# client.py
import xmlrpc.client
from datetime import datetime, timezone, timedelta
 
SERVER_URL = "http://127.0.0.1:8000"
proxy = xmlrpc.client.ServerProxy(SERVER_URL, allow_none=True)
 
# Enter date of birth in YYYY-MM-DD format.
dob = input("Enter your date of birth (YYYY-MM-DD): ")
 
# Intentionally incorrect local time for the first request.
dummy_time = datetime.now(timezone.utc) + timedelta(hours=2)
client_time = dummy_time.isoformat(timespec="seconds")
 
print("\\nSending request with intentionally incorrect time...")
response = proxy.calculate_age(client_time, dob)
 
# If rejected, update the timestamp using the server-provided time.
if response["status"] == "REJECTED":
    print("\\nSERVER NOTIFICATION:", response["notification"])
    print("Correct server time:", response["correct_server_time"])
 
    client_time = response["correct_server_time"]
    print("\\nClient time updated. Resending the request...")
 
    response = proxy.calculate_age(client_time, dob)
 
# Display the final response.
if response["status"] == "SUCCESS":
    print("\\nRequest accepted.")
    print("Server message:", response["message"])
    print("Calculated age:", response["age"])
    print("Verified server time:", response["server_time"])
else:
    print("\\nRequest could not be completed.")
    print(response.get("message", response.get("notification", "Unknown error.")))