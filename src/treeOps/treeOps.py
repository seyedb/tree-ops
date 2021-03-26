#
import tree
import re
import string

def list_to_tree(dlist, rootVal=None, balanced=False):
    '''Constructs a binary tree (BST or AVL) from a given list of node data.

    NOTE: 
        - if balanced=True the rebalancing procedure (consisting of tree rotations) may lead to a 
        tree where rootVal is not necessarily the root. 
        - if rootVal=None (default) the first element of dlist will be assgined to rootVal

    args:
        dlist (list): list of node data
        rootVal (node val data type): value of the root node, may or may not be from dlist
        balanced (boolean): if True the result will be a balanced tree
    returns:
        (tree) a BST from the given data list
    '''
    t = tree.tree()

    if rootVal is None:
        try:
            rootVal = dlist[0]
        except IndexError:
            print("Error! dlist, the list of node data, is empty.")
            return None

    t.add_node(rootVal, balanced)

    try:
        dlist.remove(rootVal)
    except ValueError:
        pass

    for data in dlist:
        t.add_node(data, balanced)

    return t

def dict_to_tree(tdict, root_ind=0): 
    '''Converts a (2D) nested dictionary (node adjacency information) to a tree. Can be used to 
    create an arbitrary binary tree with distinct node values.

    NOTE:
        - the input dictionary should have the follwing format: 
          {n1: {'left': n3, 'right': 'None'}, n2: {'left': 'None', 'right': n4}, ...}
          the string value 'None' represents a None-type treeNode
    
    args:
        tdict (nested dict): the dictionary containing tree data with the above-mentioned format
        root_ind (int): the index of the node in the dictionary that will be the tree root
    returns:
        (tree) a binary tree with data consistent with the provided tree data dictionary
    '''
    assert(root_ind in range(len(tdict))), "Error! Invalid root index."

    ndata_list = []
    nodes = []

    for ndata in tdict.keys():
        ndata_list.append(ndata)
        nodes.append(tree.tree().treeNode(ndata))

    t = tree.tree(nodes[root_ind])

    for ndata, children in tdict.items():

        n_ind = ndata_list.index(ndata)
        n = nodes[n_ind]

        if children['left'] != 'None':
            l_ind = ndata_list.index(children['left'])
            lnode = nodes[l_ind]
            lnode.parent = n
        else:
            lnode = None

        if children['right'] != 'None':
            r_ind = ndata_list.index(children['right'])
            rnode = nodes[r_ind]
            rnode.parent = n
        else:
            rnode = None

        n.left = lnode
        n.right = rnode

    t.update_height()
    t.update_balance_factor()

    return t

def balance_by_recursion(inTree):
    '''Converts a given binary tree (may or may not be BST) to a balanced binary tree by recursion
    in the following steps:
        - creates a sorted list of nodes from the input tree using an inorder traversal path
        - constructs a balanced tree recursively from a sorted list of nodes:
            1- find the middle of the list and make it the root
            2- get the middle left half of the list and make it the left node of the step 1
            3- get the middle right half of the list and make it the right node of the step 1

    args:
        inTree (tree) input tree
    returns:
        (tree) a balanced binary tree containing the data/nodes from the given binary tree
    '''
    path = inTree.inorder_traversal(inTree.root)
    # reset the visit status (can be avoided if visit status is removed as a node attribute)
    for node in path:
        node._setStatus(tree.node_status.UNVISITED)

    rnode = inTree._balanceByRecursion(path, 0, len(path) - 1)
    balancedt = tree.tree(rnode)

    return balancedt

def convert_to_AVL(inTree):
    '''Converts a given tree (may or may not be BST) to a balanced (AVL) tree.

    args:
        inTree (tree) input tree
    returns:
        (tree) a balanced (AVL) tree containing the data/nodes from the given tree
    '''
    avlTree = tree.tree()
    inTree._convertToAVL(inTree.root, avlTree)

    return avlTree

def text_to_tree(path, regex="", balanced=False):
    '''Splits a text into paragraphs, splits each paragraph into words and stores those words in a tree.

    NOTE: 
    - Uses regular expressions and split function to extract words. Like any machine learning problem
    dealing with text data, the challenge is how clean the words are desired to be. Here the choice of 
    the regex can affect the words that are extracted, a more sophisticated option would be using 
    libraries like NLTK. 
    Some regex examples:
        regex="["+string.punctuation+"]" would remove punctuations but also contractions like "don't" will
        become "dont" and numbers like "2.3" will become "23"
        regex="(?<!\d )["+string.punctuation+"](?!\d)", acts as above but numbers will remain unchanged
    - The size of the returned list is equal to the number of non-empty paragraphs in the text

    args:
        path (str): path to the input file
        regex (str): regular expression used while splitting paragraph into words
        balanced (boolean): if True the constructed trees will be balanced
    returns:
        (list of tree) a list of trees where each tree stores words found in any (non-empty) paragraph 
    '''
    with open(path, "r") as fid:
        txtdata = fid.read()
        paragraphs = txtdata.split("\n\n")

    parlist = list(filter(None, paragraphs))

    treelist = []
    for paragraph in parlist:
        par = paragraph.replace("\n", " ").replace("\r", "")
        wordlist = re.sub(regex,"",par).split()
        if len(wordlist) > 0:
            # use default rootVal
            t = list_to_tree(wordlist, balanced=balanced)
            treelist.append(t)

    return treelist

def find_word(wrd, indIntv, path, regex="", balanced=False):
    '''Searches for a word in a given text file: Splits a text into paragraphs, splits each paragraph into 
    words and stores those words in a tree, then searches for the word in every tree.

    NOTE:
    - See comment of the routine text_to_tree 
    - Paragraphs are indexed in a 0-based fashion

    args:
        wrd (str): the word to be searched for
        indIntv (int list): interval of paragraph indices, search will be limited to the paragraphs with
                indices within the interval
        path (str): path to the input file
        regex (str): regular expression used while splitting paragraph into words
        balanced (boolean): if True the constructed trees will be balanced
    returns:
        (list of int) index of paragraphs that contain the target word 
    '''
    res = []

    treelist = text_to_tree(path, regex=regex, balanced=balanced)
    print("The file has {} (non-empty) paragraphs (0-index based).".format(len(treelist)-1))

    indIntv.sort()
    s1, e1 = indIntv
    s2, e2 = [0, len(treelist)-1]
    if s2 > e1 or s1 > e2:
        print("Invalid interval!")
        return res
    else:
        start = max(s1, s2)
        end = min(e1, e2)
        print("Searching for '{}' in paragraphs indexed within: [{}, {}]".format(wrd, start, end))

    for pn in list(range(start, end+1)):
        if wrd in treelist[pn]:
            res.append(pn)

    return res
