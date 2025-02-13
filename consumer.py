"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
import time

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self)
        for key, value in kwargs.items():
            if key == "name":
                self.name = value
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()
            for action in cart:
                for i in range(action['quantity']):
                    self.do_action(cart_id, action['product'], action['type'])

            checkout = self.marketplace.place_order(cart_id)
            for item in checkout:
                print (self.name + " bought " + str(item))

    def do_action(self, cart_id, product, action_type):
        while True:
            result = False
            if action_type == "add":
                result = self.marketplace.add_to_cart(cart_id, product)
                time.sleep(self.retry_wait_time)
            elif action_type == "remove":
                result = self.marketplace.remove_from_cart(cart_id, product)

            if result:
                return

