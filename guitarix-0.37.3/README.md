### Creating the patch

```
$ diff -Naur guitarix-0.37.3 guitarix-0.37.3-patch > guitarix-0.37.3.patch
```

### Applying the patch

Under the root source tree:

```
$ patch -p1 < guitarix-0.37.3.patch
```
### Pre Headless

- fixed 256
- no MIDI input processing
