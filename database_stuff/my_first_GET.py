#!/bin/bash/python

import urllib2
import json


def get_config(id):
    webcall = "http://localhost:5000/todo/api/v1.0/tasks/%s"%id
    #print webcall
    webcalled1=urllib2.urlopen(webcall)
    #print webcalled1
    configjson = json.load(webcalled1)
    #print configjson
    print configjson['parameters']
    watertimes = configjson['parameters']['watertimes']
    print watertimes





get_config(1)


    # tempjson = "/Users/meiera/Documents/git/data_annotation/Planteome_annotation/IRRI/test1.json"
    # TEMPJSON = open(tempjson, "w")
    # TEMPJSON.write(webcalled1)
    # TEMPJSON.close()
    # with open("/Users/meiera/Documents/git/data_annotation/Planteome_annotation/IRRI/test1.json") as data_file:
    #     trait_json=json.load(data_file)
    # return trait_json