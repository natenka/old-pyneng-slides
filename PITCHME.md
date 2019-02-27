# Python для сетевых инженеров 

---
## PEP 8 - руководство по написанию кода

---

## Расположение кода

+++?color=rgba(144, 238, 144, 0.1)

### Отступы. Да

```python
# Выравнивание по открывающейся скобке
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# 
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# Hanging indents should add a level.
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)
```

+++?color=rgba(255, 0, 0, 0.1)

### Отступы. Нет

```python
# Выравнивание по открывающейся скобке
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# 
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# Hanging indents should add a level.
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)
```
