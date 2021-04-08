

#Create huffman algorithm
import graphviz

from IPython.display import display
import subprocess

def assign_code(nodes, label, result, prefix = ''):    
    childs = nodes[label]     
    tree = {}
    if len(childs) == 2:
        tree['0'] = assign_code(nodes, childs[0], result, prefix+'0')
        tree['1'] = assign_code(nodes, childs[1], result, prefix+'1')     
        return tree
    else:
        result[label] = prefix
        return label

def Huffman_code(vals):    
    nodes = {}
     # leafs initialization
    for n in vals.keys():
        nodes[n] = []
    # binary tree creation
    while len(vals) > 1:
        s_vals = sorted(vals.items(), key=lambda x:x[1]) 
        a1 = s_vals[0][0]
        a2 = s_vals[1][0]
        vals[a1+a2] = vals.pop(a1) + vals.pop(a2)
        nodes[a1+a2] = [a1, a2]        
    code = {}
    root = a1+a2
    tree = {}
     # assignment of the code for the given binary tree      
    tree = assign_code(nodes, root, code)  
    return code, tree

def draw_tree(tree, prefix = ''):    
    if isinstance(tree, str):            
        descr = 'N%s [label="%s:%s", fontcolor=blue, fontsize=16, width=2, shape=box];\n'%(prefix, tree, prefix)
    else: 
        # Node description
        descr = 'N%s [label="%s"];\n'%(prefix, prefix)
        for child in tree.keys():
            descr += draw_tree(tree[child], prefix = prefix+child)
            descr += 'N%s -> N%s;\n'%(prefix,prefix+child)
    return descr

def print_code_and_tree(code,tree):
    print(code)
     # Create word file
    with open('graph.dot','w') as f:
        f.write('digraph G {\n')
        f.write(draw_tree(tree))
        f.write('}') 
    # Conver word to png
    subprocess.call('dot -Tpng graph.dot -o graph.png', shell=True)
    # Open word file
    with open("graph.dot") as f:
        dot_graph = f.read()
    # Diplaty word file
    display(graphviz.Source(dot_graph))

    
def print_encoded(text,code):
   # text to encode
    encoded = ''.join([code[t] for t in text])
    print('Encoded text:',encoded)
    return encoded   
def print_decoded(encoded):
    decoded = []
    i = 0
    # decoding using the binary graph
    while i < len(encoded):
        ch = encoded[i]  
        act = tree[ch]
        while not isinstance(act, str):
            i += 1
            ch = encoded[i]  
            act = act[ch]        
        decoded.append(act)          
        i += 1
    print('Decoded text:',''.join(decoded))

if __name__ == '__main__':
    freq =  dict(a=45, b=13, c=12, d=16, e=9, f=5)   
    code, tree = Huffman_code(freq)
    print_code_and_tree(code,tree)
    #return encode and print it 
    encoded=print_encoded('abcdef',code)
    print_decoded(encoded)