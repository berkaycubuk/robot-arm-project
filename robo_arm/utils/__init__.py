import yaml

def load_blocks_file():
    with open(r'/home/jnuu/robot-arm/blocks.yaml') as file:
        blocks_file = yaml.safe_load(file)

    return blocks_file['blocks']

def write_blocks_file(data):
    with open(r'/home/jnuu/robot-arm/blocks.yaml', 'w') as file:
        yaml.dump({'blocks': data}, file)

def load_orders_file():
    with open(r'/home/jnuu/robot-arm/orders.yaml') as file:
        orders_file = yaml.safe_load(file)

    return orders_file

def write_orders_file(data):
    with open(r'/home/jnuu/robot-arm/orders.yaml', 'w') as file:
        yaml.dump(data, file)

def find_order(orders, order_id):
    found = None
    for order in orders:
        if order['id'] == order_id:
            found = order
            break

    return found

def find_block(blocks, block_name):
    found = None
    for block in blocks:
        if block['name'] == block_name:
            found = block
            break

    return found
