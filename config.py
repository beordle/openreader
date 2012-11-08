#coding:utf-8
import yaml
def yamlwrite(config):
  stream = file('config.yaml', 'w')
  yaml.dump(config, stream, allow_unicode=True)

f = file('config.yaml','r')
config = yaml.load(f)

