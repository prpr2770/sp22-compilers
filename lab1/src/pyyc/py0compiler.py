#! bin/usr/python2

"""
Script to generate the compilation of programs written in "P0" - a subset of the python language containing
the following features: 
1. input() with NO ARGUMENTS
2. BINARY integer addition, UNARY integer subtraction
3. print
4. assignments - variables. 
"""

import compiler as compilerpkg
import sys


class FileCompiler:

    def __init__(self, filepath):
        self.filepath = filepath
        self.compute_outputfilename(filepath, "assembly")
        self.compute_outputfilename(filepath, "flat_py")
        self.verified_ast = None 
        self.raw_ast = None
        self.ast_tags = None 


        self.PO_unique_tags = ['Printnl', "CallFunc(Name('input'), [], None, None)", 'Const', 'Name', 'CallFunc', 'Stmt', 'AssName', 'Add', 'Discard', 'UnarySub', 'Assign']
        print("completed INIT!")

    def compute_outputfilename(self, filepath, output_type):
        """
        Script to generate the file-path of the output assembly code. 
        """
        if output_type == "assembly":
            self.assembly_filepath = filepath[:-3] + ".s"
        elif output_type == "flat_py":
            self.flattenedpy_filepath = filepath[:-3] + "_flat.py"
        else:
            print("ERROR: INVALID OUTPUT DATA TYPE")

    def obtain_tags_rec(self, ast):
        """
        Recursive function to navigate `compiler.ast.Node` and enumerate all the node-instances.
        """
        childlist = []
        for child in ast.getChildNodes():
            if child != None or isinstance(child, compilerpkg.ast.Node):
                self_type = child.__class__.__name__
                if self_type not in childlist: 
                    childlist.append(  str(self_type) )

                if self_type == "CallFunc":
                    childlist.append( str(child) )

                new_vals = self.obtain_tags_rec(child)
                if new_vals != []:
                    childlist += new_vals
        
        return childlist

    def obtain_unique_ast_nodes(self, ast):
        tag_list = self.obtain_tags_rec(ast)
        return list(set(tag_list))

    def verify_ast(self, lang_frag):
        """
        Detetermine if the AST-Nodes contained in `self.raw_ast` lies within that which is permitted for  
        """

        if lang_frag =="P0":
            
            self.ast_tags = self.obtain_unique_ast_nodes(self.raw_ast)            
            isInValidP0 = False
            for tag in self.ast_tags:
                if tag not in self.PO_unique_tags:
                    isInValidP0 = True

            if(not isInValidP0):
                self.verified_ast = self.raw_ast
        else:
            print("ERROR: INVALID LANGUAGE FRAGMENT")
            pass

    def obtain_ast(self, lang_frag):
        """
        Parse and Extract the AST from the input python code. 
        """
        self.raw_ast = compilerpkg.parse(self.filepath)
        self.verify_ast(lang_frag)

        if(self.verified_ast != None):
            print("verified AST: ")
            print(self.verified_ast)
        else:
            print(self.raw_ast)
            print(self.ast_tags)
            print("ERROR: INVALID INPUT CODE : LANGUAGE FRAGMENT VIOLATION ")

    def compile(self):
        """
        Main method that implements compilation. 
        Input: .py file. 
        Output: .s file and _flat.py file. 

        Steps of the Process: 
        1. Parse and Create AST of the input .py file. 
        2. Verify that the AST corresponds to the language fragment : P0, P1, etc. 
        3. Flatten-AST file. 
        4. Sanity-Check : Convert "flattened-AST" into "_flat.py" file. 
        5. Translate FlatAST into ASSEMBLY. 
        6. Output .s file. 
        """

        self.obtain_ast("P0")
        



def main():
    """
    Take input-arguments that refer to the python-p0-scirpts.  
    Compile them and generate a assembly( AT&T syntax ) ".s" file.
    """
    input_files =  sys.argv[1:]
    print( input_files )

    for input_file in input_files:
        print(input_file)
        compiler =  FileCompiler(input_file)
        print(compiler.assembly_filepath)
        print(compiler.flattenedpy_filepath)
        compiler.compile()


if __name__ =="__main__":
    main()