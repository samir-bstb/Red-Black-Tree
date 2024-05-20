class COLOR:
    RED = False
    BLACK = True

class Node:
    def __init__(self, key, parent):
        self.key = key
        self.color = COLOR.RED
        self.parent = parent
        self.left_node = None
        self.right_node = None

    def uncle(self): # returns the uncle of the node
        if self.parent is None or self.parent.parent is None:
            return None

        if self.parent.is_left_child():
            return self.parent.parent.right_node
        else:
            return self.parent.parent.left_node

    def is_left_child(self): # checks if the node is the left child of its parent
        return self == self.parent.left_node

    def sibling(self): # returns the sibling of the node
        if self.parent is None:
            return None

        if self.is_left_child():
            return self.parent.right_node
        else:
            return self.parent.left_node

    def change_parent(self, new_parent): # changes the parent of a given node
        if self.parent is not None:
            if self.is_left_child():
                self.parent.left_node = new_parent
            else:
                self.parent.right_node = new_parent
        new_parent.parent = self.parent
        self.parent = new_parent

    def has_Red_child(self): # checks if the node has a red child
        if self.left_node is not None and self.left_node.color == COLOR.RED:
            return True
        elif self.right_node is not None and self.right_node.color == COLOR.RED :
            return True

class RedBlackTree:
    def __init__(self):
        self.root = None

    def left_rotate(self, x):
        aux = x.right_node

        x.change_parent(aux)

        x.right_node = aux.left_node
        if aux.left_node is not None:
            aux.left_node.parent = x

        aux.left_node = x
        x.parent = aux
        if self.root == x:
           self.root = aux  

    def right_rotate(self, x):
        aux = x.left_node

        x.change_parent(aux)

        x.left_node = aux.right_node
        if aux.right_node is not None:
            aux.right_node.parent = x

        aux.right_node = x
        x.parent = aux
        if self.root == x:
            self.root = aux

    def swap_colors(self, x, y):
        aux = x.color
        x.color = y.color
        y.color = aux

    def swap_values(self, x, y):
        aux = x.key
        x.key = y.key
        y.key = aux

    def fix_RedRed(self, node):
        if self.root.color == COLOR.RED:
            self.root.color = COLOR.BLACK
            return
        
        parent = node.parent
        uncle = node.uncle()
        grandparent = node.parent.parent

        if parent.color == COLOR.RED:
            if uncle and uncle.color == COLOR.RED:
                parent.color = COLOR.BLACK
                uncle.color = COLOR.BLACK
                grandparent.color = COLOR.RED
                self.fix_RedRed(grandparent)
            else:
                if parent.is_left_child() and node.is_left_child():
                    self.swap_colors(parent, grandparent)
                    self.right_rotate(grandparent)

                elif parent.is_left_child() and not node.is_left_child():
                    self.left_rotate(parent)
                    self.swap_colors(node, grandparent)
                    self.right_rotate(grandparent)

                elif not parent.is_left_child() and node.is_left_child():
                    self.right_rotate(parent)
                    self.swap_colors(node, grandparent)
                    self.left_rotate(grandparent)

                elif not parent.is_left_child() and not node.is_left_child():
                    self.swap_colors(parent, grandparent)
                    self.left_rotate(grandparent)

    def insert(self, key):
        if self.root is None:
            self.root = Node(key, None)
            self.root.color = COLOR.BLACK
            return

        curr_node = self.root

        while curr_node is not None:
            if curr_node.key == key:
                return
            elif key < curr_node.key:
                if curr_node.left_node is None:
                    curr_node.left_node = Node(key, curr_node)
                    self.fix_RedRed(curr_node.left_node)
                    return
                else:
                    curr_node = curr_node.left_node  
            else:
                if curr_node.right_node is None:
                    curr_node.right_node = Node(key, curr_node)
                    self.fix_RedRed(curr_node.right_node)
                    return
                else:
                    curr_node = curr_node.right_node  

    def successor(self, key):
        node = self.search(key)
        aux = node

        if node is None:
            return None

        if node.right_node:
            return self.minimum(node.right_node)
        else:
            while node.parent is not None:
                if node.parent.left_node is node:
                    return node.parent             
                else:
                    node = node.parent
            return aux

    def search(self, key):
      curr_node = self.root
      return self.__search(curr_node, key)

    def __search(self, curr_node, key):
        if curr_node is not None:
            if curr_node.key == key:
                return curr_node

            elif key > curr_node.key:
                curr_node = curr_node.right_node
                return self.__search(curr_node, key)
            else:
                curr_node = curr_node.left_node
                return self.__search(curr_node, key)
        else:
            return None

    def delete(self, value):
        z = self.search(value)

        if z is None:
            return

        y_orig_color = z.color

        # 1st case: Z has no children
        if z.left_node is None and z.right_node is None:
            if z.parent is not None:
                if z.is_left_child():
                    z.parent.left_node = None
                else:
                    z.parent.right_node = None
            else:
                self.root = None
            child = None

        # 2nd case: Z has only one child
        elif z.left_node is None or z.right_node is None:
            if z.left_node:
                child = z.left_node
            else:
                child = z.right_node

            if z.parent is not None:
                if z is z.parent.left_node: #z is lieft child
                    z.parent.left_node = child
                else: #z is right child
                    z.parent.right_node = child
                if child:
                    child.parent = z.parent
            else:
                self.root = child
                if child:
                    child.parent = None

        # 3rd case: Z has both children
        else:
            y = self.successor(z.key)
            y_orig_color = y.color
            z.key = y.key
            child = y.right_node

            if y is not z.right_node:
                if y.right_node:
                    y.right_node.parent = y.parent
                if y.parent.left_node is y:
                    y.parent.left_node = y.right_node
                else:
                    y.parent.right_node = y.right_node
                y.right_node = z.right_node
                if z.right_node:
                    z.right_node.parent = y
            z.right_node = y

            y.left_node = z.left_node
            if z.left_node:
                z.left_node.parent = y
            y.color = z.color

        if y_orig_color == COLOR.BLACK:
            self.fix_after_del(child)

    def fix_after_del(self, node):
        while node is not self.root and node is not None and node.color == COLOR.BLACK:
            print("entro a while con el node: ", node)
            if node is not None and node.is_left_child():
                w = node.sibling()
                if w.color == COLOR.RED:
                    w.color = COLOR.BLACK
                    node.parent.color = COLOR.RED
                    self.left_rotate(node.parent)
                    w = node.sibling()

                if self.color_of(w.left_node) == COLOR.BLACK and self.color_of(w.right_node) == COLOR.BLACK:
                    w.color = COLOR.RED
                    node = node.parent
                else:
                    if self.color_of(w.right_node) == COLOR.BLACK:
                        w.left_node.color = COLOR.BLACK
                        w.color = COLOR.RED
                        self.right_rotate(w)
                        w = node.sibling()

                    w.color = node.parent.color
                    node.parent.color = COLOR.BLACK
                    w.right_node.color = COLOR.BLACK
                    self.left_rotate(node.parent)
                    node = self.root
            elif node is not None:
                w = node.sibling()
                if w.color == COLOR.RED:
                    w.color = COLOR.BLACK
                    node.parent.color = COLOR.RED
                    self.right_rotate(node.parent)
                    w = node.sibling()

                if self.color_of(w.left_node) == COLOR.BLACK and self.color_of(w.right_node) == COLOR.BLACK:
                    w.color = COLOR.RED
                    node = node.parent
                else:
                    if self.color_of(w.left_node) == COLOR.BLACK:
                        w.right_node.color = COLOR.BLACK
                        w.color = COLOR.RED
                        self.left_rotate(w)
                        w = node.sibling()

                    w.color = node.parent.color
                    node.parent.color = COLOR.BLACK
                    w.left_node.color = COLOR.BLACK
                    self.right_rotate(node.parent)
                    node = self.root

        if node is not None:
            node.color = COLOR.BLACK
            

    def color_of(self, node):
        if node is None:
            return COLOR.BLACK
        else:
            return node.color

    def inorder_iterative(self):
      stack = []
      curr_node = self.root

      while curr_node is not None or len(stack) > 0:
          if curr_node is not None:
              stack.append(curr_node)
              curr_node = curr_node.left_node
          else:
              curr_node = stack.pop()
              print(curr_node.key, curr_node.color, end=" ")  
              curr_node = curr_node.right_node

    def minimum(self, node):
      if node is None:
          return None

      while node.left_node is not None:
          node = node.left_node

      return node

rbt = RedBlackTree()
rbt.insert(60)
rbt.insert(70)
rbt.insert(75)
rbt.insert(68)
rbt.insert(78)
rbt.insert(73)
rbt.insert(69)
rbt.insert(65)
rbt.insert(30)
rbt.insert(40)
rbt.insert(27)
rbt.insert(85)
rbt.insert(77)
rbt.inorder_iterative()
rbt.delete(27)
rbt.delete(78)
rbt.delete(85)
rbt.delete(60)
rbt.delete(70)
print()
rbt.inorder_iterative()
