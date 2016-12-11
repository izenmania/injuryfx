"""Load any configuration information, including connection credentials, from yaml/config.yaml"""
import yaml
import os

# Load the config.yaml data into a dict for use in other modules
pdir = os.path.dirname(os.path.realpath(__file__))
conf_stream = open(pdir+"/yaml/config.yaml", "r")
conf = yaml.load(conf_stream)
