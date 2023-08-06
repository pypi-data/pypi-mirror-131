# lord kelvin

evm interface

## Quickstart:

- to run tests, type:

```
make -C tools
```

- or to use a specific ganache port:

```
PORT=1234 make -C tools
```

- to run tests, then get a shell, type:

```
make -C tools sh
```

- or to use a specific ganache port:

```
PORT=1234 make -C tools sh
```

## Using different networks

- if you're using docker, you have to do this inside the VM

- to use ganache (the default), type:

```
. env.sh
```

- to use kovan, type:

```
. env.kovan.sh
```
