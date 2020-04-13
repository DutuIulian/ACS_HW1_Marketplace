"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Semaphore

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.products_mutex = Semaphore(1)

        self.producer_mutex = Semaphore(1)
        self.products = [[]]
        self.next_producer_id = 0

        self.cart_mutex = Semaphore(1)
        self.carts = [[]]
        self.next_cart_id = 0

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.producer_mutex.acquire()
        producer_id = self.next_producer_id
        self.next_producer_id += 1
        self.producer_mutex.release()
        self.products.append([])
        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        self.products_mutex.acquire()
        if len(self.products[producer_id]) < self.queue_size_per_producer:
            for i in range(product[1]):
                self.products[producer_id].append(product[0])
            self.products_mutex.release()
            return True
        else:
            self.products_mutex.release()
            return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.cart_mutex.acquire()
        cart_id = self.next_cart_id
        self.carts.append([])
        self.next_cart_id += 1
        self.cart_mutex.release()
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        self.products_mutex.acquire()
        for product_list in self.products:
            if product in product_list:
                product_list.remove(product)
                self.carts[cart_id].append(product)
                self.products_mutex.release()
                return True

        self.products_mutex.release()
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        try:
            self.carts[cart_id].remove(product)
            return True
        except:
            return False

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.carts[cart_id]

