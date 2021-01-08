import pickle
import numpy as np
import networkx as nx
from pyvis.network import Network
#https://pyvis.readthedocs.io/en/latest/documentation.html

# Get the product amount of each node
def getCounts(root):
        number = []
        if root == None:
            return 
        q = list()
        q.append(root)
        level = -1
        while q:
            count = len(q)
            level += 1
            while count > 0:
                count -= 1
                node = q.pop(0)
                number.append(node.productCount)
                for _, v in node.children.items():
                    if v:
                        q.append(v)
        return np.percentile(number, 99)
                        

def drawGraph(root, name, scale):    
    def levelOrder(root, threshold,scale):
        if root == None:
            return 
        q = list()
        q.append(root)
        level = -1
        while q:
            count = len(q)
            level += 1
            while count > 0:
                count -= 1
                node = q.pop(0)
                if node.productCount > threshold:
                    G.add_node(node.id, label=node.name, title=node.name+"#product: "+str(node.productCount), group=level,size=node.productCount**0.5/scale)
                else:
                    G.add_node(node.id, label=' ', title=node.name+"#product: "+str(node.productCount), group=level,size=node.productCount**0.5/scale)
                for _, v in node.children.items():
                    if v:
                        q.append(v)
                        G.add_edge(node.id, v.id)
    top1 = getCounts(root)
    G=nx.Graph()
    levelOrder(root, top1, scale)
    
    g = Network(height=800, width=1200, heading=name)
    g.toggle_hide_edges_on_drag(False)
    g.from_nx(G)
    g.show(name+'.html')



def main():
    objects = []
    with (open("tree-all.pickle", "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
            
    #check the product amount of each category
    #for _, v in objects[0].children.items():
    #    print(v.name, len(v.children), v.subtreeProductCount)
    
    music = objects[0].children['Musical Instruments']
    office = objects[0].children['Office Products']
    pet = objects[0].children['Pet Supplies']
    cd = objects[0].children['CDs & Vinyl']
    Electronics =  objects[0].children['Electronics']
    clothing =  objects[0].children['Clothing, Shoes & Jewelry']
    book = objects[0].children['Books']
    
    #small
    drawGraph(music, 'Musical Instruments', 1)
    drawGraph(pet, 'Pet Supplies', 1)
    drawGraph(office, 'Office Products', 1)
    
    #medium
    drawGraph(Electronics, 'Electronics', 1)
    drawGraph(cd, 'CDs & Vinyl', 5)
    
    #large
    drawGraph(clothing, 'Clothing, Shoes & Jewelry', 5)
    drawGraph(book, 'Books', 8)

if __name__ == '__main__':
    main() 