class Model(object):
    products = {
        'milk': {'price': 1.50, 'quantity': 10},
        'eggs': {'price': 0.20, 'quantity': 100},
        'cheese': {'price': 2.00, 'quantity': 10}
    }

    def get(self, name):
        return self.products.get(name)


class View(object):
    def show_item_list(self, item_list):
        print('-' * 20)
        for item in item_list:
            print("* Name: %s" % item)
        print('-' * 20)

    def show_item_info(self, name, item_info):
        print("Name: %s Price: %s Quantity: %s" % (name, item_info['price'], item_info['quantity']))
        print('-' * 20)

    def show_empty(self, name):
        print("Name: %s not found" % name)
        print('-' * 20)


class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_items(self):
        items = self.model.products.keys()
        self.view.show_item_list(items)

    def show_item_info(self, item):
        item_info = self.model.get(item)
        if item_info:
            self.view.show_item_info(item, item_info)
        else:
            self.view.show_empty(item)


if __name__ == '__main__':
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.show_items()
    controller.show_item_info('cheese')
    controller.show_item_info('apple')
