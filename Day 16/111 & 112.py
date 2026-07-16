from prettytable import PrettyTable
table = PrettyTable()

table.add_column("Pokemon Name", ["Pikachu", "Squirtle", "Charmander"], "l", "t")
table.add_column("Type", ["Electric", "Water", "Fire"], "l", "t")

print(table)