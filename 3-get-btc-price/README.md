## Output Example:

> symlink does not work here because `uv run` is needed
> 
> workaround by creating script that runs target script with script's own python environment
> 
> make sure it is executable `chmod +x <script>`

```
❯ cd $HOME
❯ ll ~/bin/btc | awk '{ print $1 }'
-rwxr-xr-x@
❯ cat ~/bin/btc

uv run $HOME/code/pmpme/etc/.venv/bin/python $HOME/code/pmpme/etc/3-get-btc-price/btc.py


❯ btc
₿ ➡️  $87,123
~ ❯
```

### References:

- free api (no api key required), https://openpublicapis.com/api/coingecko
- alt (with api key needed), https://docs.coingecko.com/docs/setting-up-your-api-key
- alt altogether, https://coinmarketcap.com/currencies/bitcoin/
