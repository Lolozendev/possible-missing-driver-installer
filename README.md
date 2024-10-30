# possible-missing-driver-installer on debian based systems
Solve a warning occuring while updating your debian based system.

I often runned through an issue when updating my system. I would get warnings about some possible missing firmwares:

```
    W: Possible missing firmware /lib/firmware/rtl_nic/rtl8168f-2.fw for module r8169
    W: Possible missing firmware /lib/firmware/rtl_nic/...
    W: Possible missing firmware /lib/firmware/rtl_nic/...
    W: Possible missing firmware /lib/firmware/rtl_nic/...
    ...
```

This python script read the warnings from a file given in parameter, download them and install them for you.
