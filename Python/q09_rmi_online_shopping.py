"""
Q9. Online Shopping application using RMI (Pyro4)

Client  : sends product name + quantity to the server.
Server  : keeps product names and prices, calculates total cost,
          applies discount, calculates final amount, sends it to client.
Client  : prints the discount and the final amount.

Discount rule used here:  total >= 5000 -> 10%,  total >= 1000 -> 5%, else 0%

SETUP (once):   pip install Pyro4
HOW TO RUN:     python q09_rmi_online_shopping.py
"""
import threading
import Pyro4


# ---------------------------- SERVER SIDE ----------------------------
@Pyro4.expose
class ShoppingServer(object):
    def __init__(self):
        # the server maintains product name -> price
        self.products = {
            "laptop": 50000,
            "mouse": 500,
            "keyboard": 1200,
            "headphones": 2000,
        }

    def get_product_list(self):
        return self.products

    def calculate_bill(self, product, quantity):
        product = product.lower()
        if product not in self.products:
            return None                              # unknown product

        price = self.products[product]
        total = price * quantity                     # total cost

        if total >= 5000:                            # apply discount
            discount_percent = 10
        elif total >= 1000:
            discount_percent = 5
        else:
            discount_percent = 0

        discount_amount = total * discount_percent / 100
        final_amount = total - discount_amount       # final amount to pay
        return {"price": price, "total": total,
                "discount_percent": discount_percent,
                "discount_amount": discount_amount,
                "final_amount": final_amount}


def start_server(ready_event, uri_holder):
    daemon = Pyro4.Daemon()
    uri = daemon.register(ShoppingServer)
    uri_holder.append(str(uri))
    ready_event.set()
    daemon.requestLoop()


# ---------------------------- CLIENT SIDE ----------------------------
def client(uri):
    shop = Pyro4.Proxy(uri)

    print("Available products:", shop.get_product_list())
    product = input("Enter product name : ")
    quantity = int(input("Enter quantity     : "))

    bill = shop.calculate_bill(product, quantity)    # REMOTE CALL
    if bill is None:
        print("Product not available")
    else:
        print(f"\nTotal cost   : Rs. {bill['total']}")
        print(f"Discount     : {bill['discount_percent']}%  (Rs. {bill['discount_amount']})")
        print(f"Final amount : Rs. {bill['final_amount']}")


if __name__ == "__main__":
    ready = threading.Event()
    uri_holder = []
    threading.Thread(target=start_server, args=(ready, uri_holder), daemon=True).start()
    ready.wait()
    client(uri_holder[0])
