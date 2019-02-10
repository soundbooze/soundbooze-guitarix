## Jack Capture

Milliseconds duration patch

### Creating the patch

```
$ diff -Naur jack_capture jack_capture_patch > jack_capture-0.9.73.patch
```

### Applying the patch

Under the root source tree:

```
$ patch -p1 < jack_capture-0.9.73.patch
```
