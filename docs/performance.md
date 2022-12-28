# Performance considerations

Creating lots of Shapes in a loop means for every step `fuse`and `clean` will be called. In an example like the below, both functions get slower and slower the more objects are already fused. Overall it takes on my machine 11.5 sec.

```python
holes = AlgCompound()
r = Rectangle(2, 2)
for loc in GridLocations(4, 4, 20, 20):
    if loc.position.X**2 + loc.position.Y**2 < (diam / 2 - 1.8) ** 2:
        holes += r @ loc

c = Circle(diam / 2) - holes
```

## Lazy evaluation

One way to avoid it is to use the `LazyAlgCompound` context. It will just collect all objects and at exit of the context call `fuse` once with all objects and `clean` once. Overall it takes 0.326 sec.

```python
with LazyAlgCompound() as holes:
    r = Rectangle(2, 2)
    for loc in GridLocations(4, 4, 20, 20):
        if loc.position.X**2 + loc.position.Y**2 < (diam / 2 - 1.8) ** 2:
            holes += r @ loc

c = Circle(diam / 2) - holes
```

## Vectorized operations

Another option is to use the vectorized operations, e.g. `AlgCompound - List[AlgCompound]`. It is another syntax for the `LazyAlgCompound` approach above and slightly faster. Overall it takes 0.264 sec.

```python
r = Rectangle(2, 2)
holes = [
    r @ loc
    for loc in GridLocations(4, 4, 20, 20)
    if loc.position.X**2 + loc.position.Y**2 < (diam / 2 - 1.8) ** 2
]

c = Circle(diam / 2) - holes
```
