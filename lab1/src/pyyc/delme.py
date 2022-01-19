#! usr/bin/python2

import compiler as compilerpkg

global counter

counter = 0 


def obtain_children(ast):
    global counter 

    childlist = []
    for child in ast.getChildNodes():
        if child != None:
            counter += 1
            print(counter, child, type(child) )
            childlist.append( child )
            childlist += [obtain_children(child)]
    return childlist

def obtain_tags_rec(ast):
    global counter 

    childlist = []
    for child in ast.getChildNodes():
        if child != None or isinstance(child, compilerpkg.ast.Node):
            counter += 1
            print(counter, child, child.__class__.__name__ )
            self_type = child.__class__.__name__
            if self_type not in childlist: 
                childlist.append(  str(self_type) )

            if self_type == "CallFunc":
                childlist.append( str(child) )

            new_vals = obtain_tags_rec(child)
            if new_vals != []:
                childlist += new_vals
    
    return childlist

def obtain_tags(ast):
    tag_list = obtain_tags_rec(ast)
    return list(set(tag_list))


    
    



if __name__=="__main__":
    code = """print "help"\na = 4 + 5\nc = a + 2\nd=c+input()\ne=3 + -2\n5+6"""

    print(code)

    raw_ast = compilerpkg.parse(code)
    #print(raw_ast)

    children_tags = obtain_tags(raw_ast)
    
    unique_tags = list(set(children_tags))
    print( unique_tags )






