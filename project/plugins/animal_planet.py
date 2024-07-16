from taskweaver.plugin import Plugin, register_plugin

@register_plugin
class SQLManagementSystem(Plugin):
    def __call__(self, name: str):
        if(len(name)!=0):
            name = "I am a Doug!"
            return name
        else:
            name = "I am king!"
            return name
