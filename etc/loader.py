def yml(title: str):
    import yaml
    with open(f'src/etc/{title}', 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)