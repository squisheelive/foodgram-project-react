import base64
with open("warcraft.jpg", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
print(my_string)

{'ingredients': [{'id': 1, 'amount': 10}, {'id': 2, 'amount': 99}],
 'tags': [1, 2],
  'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==',
   'name': 'string',
    'text': 'string',
     'cooking_time': 1}