from taskweaver.plugin import Plugin, register_plugin

@register_plugin
class SQLManagementSystem(Plugin):
    def __call__(self, name: str):
        match(name):
            case "Dog":
                print("A dog is a domestic mammal of the family Canidae and the order Carnivora.")
            case "Cat":
                print("Commonly referred to as the domestic cat or house cat, is a small domesticated carnivorous mammal.")
            case "Horse":
                print("The horse is a domesticated, one-toed, hoofed mammal. It belongs to the taxonomic family Equidae and is one of two extant subspecies of Equus ferus.")
            case "Rabbit":
                print("Rabbits are small mammals in the family Leporidae, which is in the order Lagomorpha.")
            case "Frog":
                print("A frog is any member of a diverse and largely carnivorous group of short-bodied, tailless amphibians composing the order Anura.")
            case _:
                print("Animal undocumented in animal planet.")