from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json
from estructuras import ArbolBinario, Node, traverse_linked_list, deleteSpecificNode, insertNodeAtPosition

app = FastAPI()

orders_head = None  # Lista enlazada global de pedidos
products_tree = None  # Árbol binario global de productos
products_list = []    # Lista de productos en memoria.

@app.get('/')
def root():
    return "Hello, World!"

@app.get("/products") 
async def get_products(): # Devuelve la lista de productos desde products.json
    global products_list
    try:
        with open('products.json', 'r', encoding="utf-8") as file:
            products_list = json.load(file)

        if not products_list:
            raise HTTPException(status_code=404, detail="No products found")

        return JSONResponse(content=products_list)

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Products file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/products/{id}") # Devuelve un producto por su ID usando el árbol binario para buscar
async def get_product_by_id(id: int):
    global products_tree, products_list
    try:
        if products_tree is None:
            # Inicializar árbol la primera vez que se hace GET por ID
            if not products_list:
                with open('products.json', 'r', encoding="utf-8") as file:
                    products_list = json.load(file)
            if not products_list:
                raise HTTPException(status_code=404, detail="No products found")

            products_tree = ArbolBinario(products_list[0]["id"])
            for product in products_list[1:]:
                products_tree.insertar(product["id"])

        # Usar el árbol para buscar
        if not products_tree.buscar(id):
            raise HTTPException(status_code=404, detail="Product not found")

        # Encontrar el producto en la lista para devolverlo
        for product in products_list:
            if product["id"] == id:
                return JSONResponse(content=product)

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Products file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/products") # Agrega un nuevo producto a products.json y al árbol binario
async def add_product(request: Request):
    global products_list, products_tree
    try:
        new_product = await request.json()
        products_list.append(new_product)
        with open('products.json', 'w', encoding="utf-8") as file:
            json.dump(products_list, file, indent=4, ensure_ascii=False)
        if products_tree is None:
            products_tree = ArbolBinario(new_product["id"])
        else:
            products_tree.insertar(new_product["id"])
        return JSONResponse(content={"message": "Product added successfully", "product": new_product})
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Products file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/orders") # Devuelve la lista de pedidos desde orders.json usando lista enlazada
async def get_orders():
    global orders_head
    try:
        with open('orders.json', 'r', encoding='utf-8') as f:
            orders_list = json.load(f)
        if not orders_list:
            raise HTTPException(status_code=404, detail="No orders found")
        orders_head = None
        for order in orders_list:
            new_node = Node(order)
            if orders_head is None:
                orders_head = new_node
            else:
                current = orders_head
                while current.next:
                    current = current.next
                current.next = new_node
        # Usar traverse_linked_list para obtener los pedidos
        orders = traverse_linked_list(orders_head)
        return JSONResponse(content=orders)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="commands.json file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/orders/{order_id}") # Devuelve un pedido por su ID usando lista enlazada para buscar
async def get_order_by_id(order_id: int):
    global orders_head
    try:
        try:
            with open('orders.json', 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    orders_list = json.loads(content)
                else:
                    orders_list = []
        except FileNotFoundError:
            orders_list = []
        if not orders_list:
            raise HTTPException(status_code=404, detail="No orders found")
        orders_head = None
        for order in orders_list:
            node = Node(order)
            if orders_head is None:
                orders_head = node
            else:
                current = orders_head
                while current.next:
                    current = current.next
                current.next = node
        current = orders_head
        while current:
            if current.data.get("id") == order_id:
                return JSONResponse(content=current.data)
            current = current.next
        raise HTTPException(status_code=404, detail="Order not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/orders")
async def add_order(request: Request):
    global orders_head
    try:
        new_order = await request.json()
        new_node = Node(new_order)
        try:
            with open('orders.json', 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    orders_list = json.loads(content)
                else:
                    orders_list = []
        except FileNotFoundError:
            orders_list = []
        orders_head = None
        for order in orders_list:
            node = Node(order)
            if orders_head is None:
                orders_head = node
            else:
                current = orders_head
                while current.next:
                    current = current.next
                current.next = node
        length = len(traverse_linked_list(orders_head))
        orders_head = insertNodeAtPosition(orders_head, new_node, length + 1)
        all_orders = traverse_linked_list(orders_head)
        with open('orders.json', 'w', encoding='utf-8') as f:
            json.dump(all_orders, f, indent=4, ensure_ascii=False)
        return JSONResponse(content={"message": "Order added successfully", "order": new_order})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    global orders_head
    try:
        try:
            with open('orders.json', 'r', encoding='utf-8') as f:
                orders_list = json.load(f)
        except FileNotFoundError:
            orders_list = []
        if not orders_list:
            raise HTTPException(status_code=404, detail="No orders found")
        orders_head = None
        for order in orders_list:
            node = Node(order)
            if orders_head is None:
                orders_head = node
            else:
                current = orders_head
                while current.next:
                    current = current.next
                current.next = node
        current = orders_head
        node_to_delete = None
        while current:
            if current.data["id"] == order_id:
                node_to_delete = current
                break
            current = current.next
        if node_to_delete is None:
            raise HTTPException(status_code=404, detail="Order not found")
        orders_head = deleteSpecificNode(orders_head, node_to_delete)
        all_orders = traverse_linked_list(orders_head)
        with open('orders.json', 'w', encoding='utf-8') as f:
            json.dump(all_orders, f, indent=4, ensure_ascii=False)
        return JSONResponse(content={"message": f"Order {order_id} deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/orders/{order_id}")
async def update_order(order_id: int, request: Request):
    global orders_head
    try:
        updated_data = await request.json()
        try:
            with open('orders.json', 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    orders_list = json.loads(content) 
                else: 
                    orders_list = []
        except FileNotFoundError:
            orders_list = []

        if not orders_list:
            raise HTTPException(status_code=404, detail="No orders found")
        orders_head = None
        for order in orders_list:
            node = Node(order)
            if orders_head is None:
                orders_head = node
            else:
                current = orders_head
                while current.next:
                    current = current.next
                current.next = node
        current = orders_head
        found = False
        while current:
            if current.data.get("id") == order_id:
                updated_data["id"] = order_id
                current.data = updated_data
                found = True
                break
            current = current.next
        if not found:
            raise HTTPException(status_code=404, detail="Order not found")
        all_orders = traverse_linked_list(orders_head)
        with open('orders.json', 'w', encoding='utf-8') as f:
            json.dump(all_orders, f, indent=4, ensure_ascii=False)
        return JSONResponse(content={
            "message": f"Order {order_id} updated successfully",
            "order": updated_data
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




