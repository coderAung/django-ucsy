from dataclasses import dataclass

from django.http import QueryDict


class FormValidator:
    def __init__(self, keys:list[str], rules:dict[str, str]):
        self._keys:list[str] = keys
        self._rules:dict[str, str] = rules

    def validate(self, post:QueryDict):
        errors:dict[str, str] = {}
        for k in self._keys:
            value = post.get(k)
            if value == '':
                errors.update({k: self._rules.get(k)})
        return errors

    class Builder:
        def __init__(self):
            self._keys:list[str] = []
            self._rules:dict[str, str] = {}

        def rule(self, key:str, message:str = '') -> 'FormValidator.Builder':
            if message == '':
                message = f'{key} cannot be empty.'
            
            self._keys.append(key)
            self._rules.update(({key: message}))
            return self
        
        def build(self) -> 'FormValidator':
            v = FormValidator(keys=self._keys, rules=self._rules)
            return v