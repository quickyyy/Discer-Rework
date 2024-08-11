    ______________________________________________________
    $$$$$$$..|$$/..._______..._______...______....______..
    $$.|..$$.|/..|./.......|./.......|./......\../......\.
    $$.|..$$.|$$.|/$$$$$$$/./$$$$$$$/./$$$$$$..|/$$$$$$..|
    $$.|..$$.|$$.|$$......\.$$.|......$$....$$.|$$.|..$$/.
    $$.|__$$.|$$.|.$$$$$$..|$$.\_____.$$$$$$$$/.$$.|......
    $$....$$/.$$.|/.....$$/.$$.......|$$.......|$$.|......
    $$$$$$$/..$$/.$$$$$$$/...$$$$$$$/..$$$$$$$/.$$/....... Rework :D
    ______________________________________________________
## Translations:

 - [RU](https://github.com/quickyyy/Discer-Rework/blob/main/READMERU.md)


## Welcome to Discer Rework!

Discer rework - is a rework of my old project of checker (and not only?) discord tokens
## The changes that have been made

- Complete overhaul of the structure and code as a whole
- Changing the output in the console
- Now there's a compiled version (woo, yoohoo!)
- Changed and redesigned settings
- There should be no more problems with the path, you can specify any absolute or short path in the script directory.
- The design and flow of the project has been coordinately changed
- Now checks for discord badges (Testing function)
## Roadmap

- add multithreading as in the old version

- Screw the gui?

- Suggest your variations to @bredcookie


## FAQ

#### Why not use proxy/fake_useragent?

For discord, it doesn't matter how many requests come from one IP, at least on tests. fake_useragent is also not important, additionally, Nuitka does not want to work with it.

#### What are the settings in discer.q3 responsible for?

- printdebuglines - bool (True/False) - Outputs debug lines to the console (not too necessary for the average user)
- simpleverify - bool (True/False) - Doesn't display account details in the console (which means nowhere yet)
- checkonbadges - bool (True/False) - Since this is a feature being tested, I've added enabling and disabling it in the settings (I may remove it after public tests)
- printinvalidtokens - bool (True/False) - is responsible for outputting invalid tokens to the console (If False, it will only output an error about invalid token)
- sslverificationonrequest - bool (True/False) - Disables ssl check on request to discord (On tests, helped to revive the checker)
All these settings are changed by changing the discer.q3 file, if it is not in the directory, the script will create a config and ask the user to change it and restart discer.
## Support

For support, dm me in  t.me/quicky_lzt or join our @bredcookie channel.


## License

[MIT](https://choosealicense.com/licenses/mit/)

