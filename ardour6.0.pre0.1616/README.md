### Clone

``` 
git clone git://git.ardour.org/ardour/ardour.git ardour6.0.pre0.1616
```

## Ardour 6.0

MIDI track fan out and audio recording crash patch

### Creating the patch

```
$ diff -u disk_writer.cc disk_writer_fix.cc > ~/ardour6.0.pre0.1616.patch
```

### Applying the patch

Under ardour/libs/ardour:

```
$ patch < ~/ardour6.0.pre0.1616.patch
```
