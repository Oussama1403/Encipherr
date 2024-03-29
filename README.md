<p align="center">
  <a href="https://encipherr.pythonanywhere.com/">
    <img src="https://github.com/Oussama1403/Encipherr/blob/main/src/static/pwa/512x512-blue.png" width="100">
  </a>
  <h3 align="center">Encipherr</h3>

 
  <p align="center">
    Free online encryption and decryption tool.
    <br>
    <a href="https://encipherr.pythonanywhere.com/"><strong> Explore Encipherr »</strong></a>
  </p>
</p>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<div align="center">

[contributors-shield]: https://img.shields.io/github/contributors/Oussama1403/Encipherr.svg?style=for-the-badge
[contributors-url]: https://github.com/Oussama1403/Encipherr/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Oussama1403/Encipherr.svg?style=for-the-badge
[forks-url]: https://github.com/Oussama1403/Encipherr/network/members
[stars-shield]: https://img.shields.io/github/stars/Oussama1403/Encipherr.svg?style=for-the-badge
[stars-url]: https://github.com/Oussama1403/Encipherr/stargazers
[issues-shield]: https://img.shields.io/github/issues/Oussama1403/Encipherr.svg?style=for-the-badge
[issues-url]: https://github.com/Oussama1403/Encipherr/issues
[license-shield]: https://img.shields.io/github/license/Oussama1403/Encipherr.svg?style=for-the-badge
[license-url]: https://github.com/Oussama1403/Encipherr/blob/main/LICENSE.txt

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


### Made with love using:
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![Python](https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white) ![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

</div>

## About The Project

<!-- [![screenshot](screenshot.png)](https://encipherr.pythonanywhere.com/) -->
<a href="https://encipherr.pythonanywhere.com/"><img src="images/scrn_1.png" width="200" />  <img src="images/scrn_2.png" width="200" /></a>

Encipherr is a web app that provides powerful encryption of data. It is fast and free, and it is open source. It uses no ads, and it is the only easy way to encrypt your data in any web browser.

Encipherr uses <a href="https://fr.wikipedia.org/wiki/Advanced_Encryption_Standard" target="_blank">AES</a> encryption algorithm. 
AES is both fast, and cryptographically strong. It is a good default choice for encryption and it's considered one of the strongest algorithms available.  

## Usage
Visit <a href="https://Encipherr.pythonanywhere.com/" target="_blank">Encipherr website</a> \
or install project files and run it locally:

```bash
git clone https://github.com/Oussama1403/Encipherr

```
The project directory will contain:

```
.
├── CHANGELOG.md
├── LICENSE.txt
├── main.py
├── README.md
├── requirements.txt
├── screenshot.png
└── src
    ├── app.py
    ├── config.py
    ├── db.sqlite3
    ├── modules.py
    ├── robots.txt
    ├── routes.py
    ├── static
    │   ├── assets
    │   │   └── logo.png
    │   ├── css
    │   │   └── style.css
    │   ├── easter-egg
    │   │   ├── egg.html
    │   │   └── egg.js
    │   ├── js
    │   │   ├── ajaxcall.js
    │   │   └── upload.js
    │   ├── pwa
    │   │   ├── 512x512-blue.png
    │   │   ├── 512x512.png
    │   │   ├── app.js
    │   │   ├── manifest.json
    │   │   └── offline.html
    │   └── uploads
    ├── sw.js
    └── templates
        ├── about.html
        ├── base.html
        ├── home.html
        ├── page-404.html
        ├── page-500.html
        └── privacy.html

9 directories, 30 files

```

:warning: Make sure python3 and flask framework are installed.

install modules:
```bash
pip install -r requirements.txt
```
then run the server by typing in your terminal:

```python
python3 main.py
```
## CHANGELOG
Read the latest notable changes made to a Encipherr [here](CHANGELOG.md)

## TODO
- Custom encryption key (password) (Done) :heavy_check_mark:.
- More encryption algorithms.
- Offline usage (semi-ready).

## Encipherr-CLI :sparkles:

<b>A command line interface (CLI) version of Encipherr for the offline usage.
<a href="https://github.com/Oussama1403/Encipherr-CLI">github.com/Oussama1403/Encipherr-CLI</a></b>

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to test your changes.

## License
[MIT](https://choosealicense.com/licenses/mit/)
