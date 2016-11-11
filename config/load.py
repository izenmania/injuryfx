import yaml
import os

pdir = os.path.dirname(os.path.realpath(__file__))
conf_stream = open(pdir+"/yaml/config.yaml", "r")
conf = yaml.load(conf_stream)
