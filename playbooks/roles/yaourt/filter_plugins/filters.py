#!/usr/bin/python

class FilterModule(object):
    def filters(self):
        return {
            "bool_to_int" : self.bool_to_int
        }


    def bool_to_int(self, value):
        int(bool(value))
