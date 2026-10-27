"""
Q6. RMI - Temperature Conversion: Celsius to Fahrenheit   (using Pyro4)

RMI (Remote Method Invocation): the CLIENT calls a method that actually
runs on the SERVER, as if it were a local function.

SETUP (once, in PowerShell / cmd):   pip install Pyro4
HOW TO RUN (Windows):                python q06_rmi_temperature.py
Server and client run in this one file (no name server needed).
"""
import threading
import Pyro4   # Python Remote Objects library (RMI for Python)


# ---------------------------- SERVER SIDE ----------------------------
@Pyro4.expose                       # makes the class callable from remote clients
class TemperatureConverter(object):
    def celsius_to_fahrenheit(self, celsius):
        # formula: F = C * 9/5 + 32
        return (celsius * 9 / 5) + 32


def start_server(ready_event, uri_holder):
    daemon = Pyro4.Daemon()                         # the Pyro server
    uri = daemon.register(TemperatureConverter)     # register the remote object
    uri_holder.append(str(uri))                     # give the address to the client
    print("[SERVER] Remote object ready at:", uri)
    ready_event.set()
    daemon.requestLoop()                            # keep serving requests


# ---------------------------- CLIENT SIDE ----------------------------
def client(uri):
    remote_obj = Pyro4.Proxy(uri)                   # proxy = stand-in for remote object
    celsius = float(input("Enter temperature in Celsius: "))
    fahrenheit = remote_obj.celsius_to_fahrenheit(celsius)   # REMOTE CALL
    print(f"{celsius} C = {fahrenheit} F")


if __name__ == "__main__":
    ready = threading.Event()
    uri_holder = []
    threading.Thread(target=start_server, args=(ready, uri_holder), daemon=True).start()
    ready.wait()
    client(uri_holder[0])
