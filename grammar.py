import yaml


class Grammar:
    def __init__(self, grammar_file):
        with open(grammar_file) as f:
            self.raw = yaml.load(f, Loader=yaml.Loader)
            print(self.raw)



if __name__ == "__main__":
    grammar = Grammar('expression.yaml')
