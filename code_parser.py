# -*- coding: utf-8 -*-

import ast
import os

#import astor


def expand_attribute(attribute):
    parent_name = []
    while attribute.__class__ is ast.Attribute:
        parent_name.append(attribute.attr)
        attribute = attribute.value
    name = '.'.join(reversed(parent_name))
    attribute_id = ''
    if attribute.__class__ is ast.Name:
        attribute_id = attribute.id
    elif attribute.__class__ is ast.Call:
        if attribute.func.__class__ is ast.Attribute:
            attribute_id = '%s.%s()' % (
                expand_attribute(attribute.func.value),
                attribute.func.attr)
        else:
            attribute_id = '%s()' % attribute.func.id
    name = attribute_id if name == '' else ("%s.%s" % (attribute_id, name))
    return name


class TranslatorVisitor(ast.NodeVisitor):

    testing = True

    def parse(self, astmodule):
        self.symbols = []
        self.imports = []
        self.visit(astmodule)
        a = 234

    def visit_Import(self, node):
        for item in node.names:
            if item.asname:
                self.imports.append(item.asname)
            else:
                self.imports.append(item.name)
        return node

    def visit_FromImport(self, node):
        for item in node.names:
            if item.asname:
                self.imports.append(item.asname)
            else:
                self.imports.append("%s.%s" % (item.module, item.name))
        return node

    def visit_ClassDef(self, node):
        if node.name not in self.symbols:
            self.symbols.append(node.name)
        for item in node.body:
            self.visit(item)
        return node

    def visit_FunctionDef(self, node):
        if node.name not in self.symbols:
            self.symbols.append(node.name)
        for item in node.body:
            self.visit(item)
        return node

    def visit_Name(self, node):
        if node.id not in self.symbols:
            self.symbols.append(node.id)
        return node

    def visit_Attribute(self, node):
        expanded = expand_attribute(node)
        ignore = any(expanded.startswith(i) for i in self.imports)
        if not ignore and node.attr not in self.symbols:
            self.symbols.append(node.attr)
        return node


#class ParserTranslator(ast.NodeTransformer):

    #def visit_ClassDef(self, node):
        #node.name = get_translation(node.name)
        #for item in node.body:
            #self.visit(item)
        #return node

    #def visit_FunctionDef(self, node):
        #node.name = get_translation(node.name)
        #return node

    #def visit_Name(self, node):
        #node.id = get_translation(node.id)
        #return node

    #def visit_Attribute(self, node):
        #node.attr = get_translation(node.attr)
        #return node


def create_po(path):
    visitor = TranslatorVisitor()
    for root, dirs, files in os.walk(path, followlinks=True):
        for filen in files:
            if os.path.splitext(filen.lower())[-1] != '.py':
                continue
            filename = os.path.join(root, filen)
            with open(filename, 'r') as f:
                source = f.read()
                module = ast.parse(source)
                visitor.parse(module)
                print visitor.symbols
    #name = "%s.po" % os.path.basename(path)
    #filename = os.path.join(path, name)
    #with open(filename, 'w') as fp:
        #json.dump(visitor.code_names, fp, 2)
    #return filename


#def translate_source(path, output):
    #parser_translator = ParserTranslator()
    #for root, dirs, files in os.walk(path, followlinks=True):
        #for filen in files:
            #if os.path.splitext(filen.lower())[-1] != '.py':
                #continue
            #filename = os.path.join(root, filen)
            #module = None
            #with open(filename, 'r') as f:
                #source = f.read()
                #module = ast.parse(source)
            #relative = os.path.relpath(filename, path)
            #fullpath = os.path.join(output, relative)
            #folder = os.path.dirname(fullpath)
            #if not os.path.exists(folder):
                #os.makedirs(folder)
            #with open(fullpath, 'w') as f2:
                #result = parser_translator.visit(module)
                #code = astor.to_source(result)
                #f2.write(code)