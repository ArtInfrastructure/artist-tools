
# BEFORE RUNNING: Set this to your installation id, as provided by the art technician.
INSTALLATION_ID = None

# The IP (and optionally port) of the public server running in the cloud
CLOUD_HOST = "127.0.0.1:8080"

# The IP (and optionally port) of the on-site server
ART_SERVER_HOST = "127.0.0.1:8000"

# The timeout after which the weather client will fail if it hasn't had a response
WEATHER_TIMEOUT = 80 # in seconds

# The port on which the status listener will sit
# Change this if you receive a error like 'Address already in use'
STATUS_WEB_PORT = 8090
