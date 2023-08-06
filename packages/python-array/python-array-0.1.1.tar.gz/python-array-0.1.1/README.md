# python-array

See https://python-utilities.readthedocs.io/en/latest/array.html

## Install

```
pip3 install -U python-array
```

## Usage

```py
>>> from python_array import CTypesView
>>> text = bytearray(b"Hello, I am a simple ASCII string!")
>>> ctview = CTypesView(text, itemsize=1)
>>> ctview.view[0] = 0x61
>>> print(text)
aello, I am a simple ASCII string!
>>> ctview.to_uint16()[3] = 0x6554
>>> print(text)
aello,Te am a simple ASCII string!
```

## License

MIT

## Contact

Maintained by [Shawn Presser](https://www.shawwn.com). If you found it useful, please consider [joining my patreon](https://www.patreon.com/shawwn)!

My Twitter DMs are always open; you should [send me one](https://twitter.com/theshawwn)! It's the best way to reach me, and I'm always happy to hear from you.

- Twitter: [@theshawwn](https://twitter.com/theshawwn)
- Patreon: [https://www.patreon.com/shawwn](https://www.patreon.com/shawwn)
- HN: [sillysaurusx](https://news.ycombinator.com/threads?id=sillysaurusx)
- Website: [shawwn.com](https://www.shawwn.com)

