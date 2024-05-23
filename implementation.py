class COLOR:
    RED = 'RED'
    BLACK = 'BLACK'

class Node:
    def __init__(self, key):
        self.key = key
        self.color = COLOR.RED # New nodes are always red
        self.left_node = None
        self.right_node = None
        self.parent = None

    def uncle(self): # Returns the uncle of the node
        if self.parent is None or self.parent.parent is None:
            return None

        if self.parent.is_left_child():
            return self.parent.parent.right_node
        else:
            return self.parent.parent.left_node

    def is_left_child(self): # Checks if the node is the left_node child of its parent
        return self == self.parent.left_node

    def sibling(self): # Returns the sibling of the node
        if self.parent is None:
            return None

        if self.is_left_child():
            return self.parent.right_node
        else:
            return self.parent.left_node

    def moveDown(self, new_parent): # changes the parent of a given node and moves it down
        if self.parent is not None:
            if self.is_left_child():
                self.parent.left_node = new_parent
            else:
                self.parent.right_node = new_parent
        new_parent.parent = self.parent
        self.parent = new_parent

    def hasRedChild(self): # Checks if the node has a red child
        if self.left_node is not None and self.left_node.color == COLOR.RED:
            return True
        elif self.right_node is not None and self.right_node.color == COLOR.RED :
            return True

class RedBlackTree:
    def __init__(self):
        self.root = None

    def left_rotate(self, x):
        new_parent = x.right_node

        if x == self.root:
            self.root = new_parent

        x.moveDown(new_parent)

        x.right_node = new_parent.left_node
        if new_parent.left_node is not None:
            new_parent.left_node.parent = x

        new_parent.left_node = x

    def right_rotate(self, x):
        new_parent = x.left_node

        if x == self.root:
            self.root = new_parent

        x.moveDown(new_parent)

        x.left_node = new_parent.right_node
        if new_parent.right_node is not None:
            new_parent.right_node.parent = x

        new_parent.right_node = x

    def swapColors(self, x1, x2): # Swaps the colors of two nodes
        temp = x1.color
        x1.color = x2.color
        x2.color = temp

    def swap_keys(self, u, v):# Swaps the keyues of two nodes
        temp = u.key
        u.key = v.key
        v.key = temp


    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
            self.root.color = COLOR.BLACK
            return

        curr_node = self.root

        while curr_node is not None:
            if curr_node.key == key:
                return
            elif key < curr_node.key:
                if curr_node.left_node is None:
                    curr_node.left_node = Node(key)
                    curr_node.left_node.parent = curr_node
                    self.fixRedRed(curr_node.left_node)
                    return
                else:
                    curr_node = curr_node.left_node  
            else:
                if curr_node.right_node is None:
                    curr_node.right_node = Node(key)
                    curr_node.right_node.parent = curr_node
                    self.fixRedRed(curr_node.right_node)
                    return
                else:
                    curr_node = curr_node.right_node
    
    def fixRedRed(self, node):
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
                self.fixRedRed(grandparent)
            else:
                if parent.is_left_child() and node.is_left_child():
                    self.swapColors(parent, grandparent)
                    self.right_rotate(grandparent)

                elif parent.is_left_child() and not node.is_left_child():
                    self.left_rotate(parent)
                    self.swapColors(node, grandparent)
                    self.right_rotate(grandparent)

                elif not parent.is_left_child() and node.is_left_child():
                    self.right_rotate(parent)
                    self.swapColors(node, grandparent)
                    self.left_rotate(grandparent)

                elif not parent.is_left_child() and not node.is_left_child():
                    self.swapColors(parent, grandparent)
                    self.left_rotate(grandparent)


    def successor(self, x):# Finds the in-order successor of the given node
        temp = x

        while temp.left_node is not None:
            temp = temp.left_node

        return temp

    def BSTreplace(self, x):# Finds the replacement node in BST for the given node
        if x.left_node is not None and x.right_node is not None:
            return self.successor(x.right_node)

        if x.left_node is None and x.right_node is None:
            return None

        if x.left_node is not None:
            return x.left_node
        else:
            return x.right_node 

    def deleteBykey(self, n):
        if self.root is None:
            return

        v = self.search(n)

        if v.key != n:
            print("No node found")
            return

        self.deleteNode(v)

    def deleteNode(self, v):
        u = self.BSTreplace(v)
        uvBlack = (u is None or u.color == COLOR.BLACK) and (v.color == COLOR.BLACK)
        parent = v.parent

        if u is None:
            if v == self.root:
                self.root = None
            else:
                # Remove v from the tree and move u up
                if uvBlack:
                    # u and v both black, fix double black at v
                    self.fixDoubleBlack(v)
                else:
                    # u or v are red, color u black
                    if v.sibling() is not None:
                        v.sibling().color = COLOR.RED

                if v.is_left_child():
                    parent.left_node = None
                else:
                    parent.right_node = None

            del v # Delete the node
            return

        if v.left_node is None or v.right_node is None:
            if v == self.root:
                v.key = u.key
                v.left_node = v.right_node = None
                del u
            else:
                # Remove v from the tree and move u up
                if v.is_left_child():
                    parent.left_node = u
                else:
                    parent.right_node = u

                del v
                u.parent = parent
                if uvBlack:
                    # u and v both are black, fix double black at u
                    self.fixDoubleBlack(u)
                else:
                    # u or v are red, color u black
                    u.color = COLOR.BLACK
        else:
            # Node to be deleted has two children, swap keyues with successor and recurse
            self.swap_keys(u, v)
            self.deleteNode(u)

    # Fixes the double black violation in the tree
    def fixDoubleBlack(self, x):
        if x == self.root:
            return

        sibling = x.sibling()
        parent = x.parent

        # No sibling, double black pushed up
        if sibling is None:
            self.fixDoubleBlack(parent)
        else:

            # Sibling red (3.2 case C)
            if sibling.color == COLOR.RED: 
                parent.color = COLOR.RED 
                sibling.color = COLOR.BLACK

                # left_node case (C1)
                if sibling.is_left_child():
                    self.right_rotate(parent)

                # right_node case(C2)
                else:
                    self.left_rotate(parent)
                self.fixDoubleBlack(x)
            else:

                # Sibling black
                if sibling.hasRedChild():#3.2 (A)

                    # At least 1 red child
                    if sibling.left_node is not None and sibling.left_node.color == COLOR.RED:

                        # left_node left_node
                        if sibling.is_left_child(): #(i)
                            sibling.left_node.color = sibling.color
                            sibling.color = parent.color
                            self.right_rotate(parent)

                        # right_node left_node
                        else: #(iv)
                            sibling.left_node.color = parent.color
                            self.right_rotate(sibling)
                            self.left_rotate(parent)
                    else:

                        # left_node right_node
                        if sibling.is_left_child(): #(ii)
                            sibling.right_node.color = parent.color
                            self.left_rotate(sibling)
                            self.right_rotate(parent)

                        # right_node right_node (iii)
                        else:
                            sibling.right_node.color = sibling.color
                            sibling.color = parent.color
                            self.left_rotate(parent)

                # 2 black children
                else: #Case B
                    sibling.color = COLOR.RED
                    if parent.color == COLOR.BLACK:
                        self.fixDoubleBlack(parent)
                    else:
                        parent.color = COLOR.BLACK

    def inorder_iterative(self):
      stack = []
      curr_node = self.root

      while curr_node is not None or len(stack) > 0:
          if curr_node is not None:
              stack.append(curr_node)
              curr_node = curr_node.left_node
          else:
              curr_node = stack.pop()
              print(curr_node.key, end=" ")  
              curr_node = curr_node.right_node

    # Searches for a given keyue in the tree and returns the node if found
    # Otherwise, returns the last node encountered 
    def search(self, n):
        temp = self.root
        while temp is not None:
            if n < temp.key:
                if temp.left_node is None:
                    break
                else:
                    temp = temp.left_node
            elif n == temp.key:
                break
            else:
                if temp.right_node is None:
                    break
                else:
                    temp = temp.right_node

        return temp

rbt = RedBlackTree()

rbt.insert(7)
rbt.insert(3)
rbt.insert(18)
rbt.insert(10)
rbt.insert(22)
rbt.insert(8)
rbt.insert(11)
rbt.insert(26)
rbt.insert(2)
rbt.insert(6)
rbt.insert(13)

rbt.inorder_iterative()
print()

rbt.deleteBykey(18)
rbt.deleteBykey(11)
rbt.deleteBykey(3)
rbt.deleteBykey(10)
rbt.deleteBykey(22)

rbt.inorder_iterative()
