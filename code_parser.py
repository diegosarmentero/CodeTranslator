# -*- coding: utf-8 -*-

import ast
import os
import json

import astor


LOCAL_DICTIONARY = {}


def _translate_word(word):
    #TODO: do the actual translation
    return word


def get_translation(name):
    if name in LOCAL_DICTIONARY:
        name = LOCAL_DICTIONARY[name]
    else:
        #TODO: divide the name in words and translate each one, then create
        #a single function name and store that in the dict for future usage.
        name = _translate_word(name)
        LOCAL_DICTIONARY[name] = name
    return name


class Visitor(ast.NodeVisitor):

    code_names = []

    def visit_ClassDef(self, node):
        if node.name not in self.code_names:
            self.code_names.append(node.name)
        for item in node.body:
            self.visit(item)
        return node

    def visit_FunctionDef(self, node):
        if node.name not in self.code_names:
            self.code_names.append(node.name)
        return node

    def visit_Name(self, node):
        if node.id not in self.code_names:
            self.code_names.append(node.id)
        return node

    def visit_Attribute(self, node):
        if node.attr not in self.code_names:
            self.code_names.append(node.attr)
        return node


class ParserTranslator(ast.NodeTransformer):

    def visit_ClassDef(self, node):
        node.name = get_translation(node.name)
        for item in node.body:
            self.visit(item)
        return node

    def visit_FunctionDef(self, node):
        node.name = get_translation(node.name)
        return node

    def visit_Name(self, node):
        node.id = get_translation(node.id)
        return node

    def visit_Attribute(self, node):
        node.attr = get_translation(node.attr)
        return node


def create_po(path):
    visitor = Visitor()
    for root, dirs, files in os.walk(path, followlinks=True):
        for filen in files:
            if os.path.splitext(filen.lower())[-1] != '.py':
                continue
            filename = os.path.join(root, filen)
            with open(filename, 'r') as f:
                source = f.read()
                module = ast.parse(source)
                visitor.visit(module)

    name = "%s.po" % os.path.basename(path)
    filename = os.path.join(path, name)
    with open(filename, 'w') as fp:
        json.dump(visitor.code_names, fp, 2)
    return filename


def translate_source(path, output):
    parser_translator = ParserTranslator()
    for root, dirs, files in os.walk(path, followlinks=True):
        for filen in files:
            if os.path.splitext(filen.lower())[-1] != '.py':
                continue
            filename = os.path.join(root, filen)
            module = None
            with open(filename, 'r') as f:
                source = f.read()
                module = ast.parse(source)
            relative = os.path.relpath(filename, path)
            fullpath = os.path.join(output, relative)
            folder = os.path.dirname(fullpath)
            if not os.path.exists(folder):
                os.makedirs(folder)
            print fullpath
            with open(fullpath, 'w') as f2:
                result = parser_translator.visit(module)
                code = astor.to_source(result)
                f2.write(code)