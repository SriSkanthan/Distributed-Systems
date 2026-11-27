# server.py
from xmlrpc.server import SimpleXMLRPCServer
from datetime import datetime, timezone, date
 
HOST = "0.0.0.0"
PORT = 8000
CLOCK_TOLERANCE_SECONDS = 5
 
 
def get_server_time():
    """Return the current server time in UTC."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
 
 
def validate_client_time(client_time):
    """Check whether the client's timestamp is valid and close to server time."""
    try:
        client_dt = datetime.fromisoformat(client_time)
        if client_dt.tzinfo is None:
            return {
                "valid": False,
                "message": "Timestamp must include a timezone.",
                "server_time": get_server_time()
            }
 
        server_dt = datetime.now(timezone.utc)
        client_dt = client_dt.astimezone(timezone.utc)
        difference = (client_dt - server_dt).total_seconds()
 
        if difference > CLOCK_TOLERANCE_SECONDS:
            return {
                "valid": False,
                "message": "Client time is in the future.",
                "server_time": server_dt.isoformat(timespec="seconds")
            }
 
        if abs(difference) > CLOCK_TOLERANCE_SECONDS:
            return {
                "valid": False,
                "message": "Client system time is incorrect.",
                "server_time": server_dt.isoformat(timespec="seconds")
            }
 
        return {
            "valid": True,
            "message": "Client time verified successfully.",
            "server_time": server_dt.isoformat(timespec="seconds")
        }
 
    except (TypeError, ValueError):
        return {
            "valid": False,
            "message": "Invalid timestamp format.",
            "server_time": get_server_time()
        }
 
 
def calculate_age(client_time, dob_text):
    """Validate time first; calculate age only after validation succeeds."""
    validation = validate_client_time(client_time)
 
    if not validation["valid"]:
        return {
            "status": "REJECTED",
            "notification": validation["message"],
            "correct_server_time": validation["server_time"]
        }
 
    try:
        dob = date.fromisoformat(dob_text)
        today = datetime.now(timezone.utc).date()
 
        if dob > today:
            return {
                "status": "ERROR",
                "message": "Date of birth cannot be in the future."
            }
 
        age = today.year - dob.year
        if (today.month, today.day) < (dob.month, dob.day):
            age -= 1
 
        return {
            "status": "SUCCESS",
            "message": validation["message"],
            "age": age,
            "server_time": get_server_time()
        }
 
    except (TypeError, ValueError):
        return {
            "status": "ERROR",
            "message": "Invalid date of birth. Use YYYY-MM-DD."
        }
 
 
server = SimpleXMLRPCServer((HOST, PORT), allow_none=True)
server.register_function(calculate_age, "calculate_age")
 
print(f"RPC server is running on port {PORT}...")
print("Waiting for client requests...")
 
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\\nRPC server stopped.")
    server.server_close()
