## Добро пожаловать в Discer Rework!

Discer rework - это переделка моего старого проекта по проверке (и не только?) токенов Дискорда.
## Изменения, которые были сделаны

- Полная переработка структуры и кода в целом
- Изменение вывода в консоли
- Теперь есть скомпилированная версия ( ура, ура!)
- Изменены и переработаны настройки
- Больше не должно быть проблем с путями, вы можете указать любой абсолютный или короткий путь в директории скрипта.
- Дизайн и поток проекта был координально изменен
- Теперь проверяет наличие значков дискорд (функция для тестирования)
## Дорожная карта

- добавить многопоточность, как в старой версии

- Портить gui?

- Предложите свои варианты @bredcookie


## FAQ

#### Почему бы не использовать proxy/fake_useragent?

Для discord не имеет значения, сколько запросов приходит с одного IP, по крайней мере, на тестах. fake_useragent тоже не важен, к тому же Nuitka не хочет с ним работать.

#### За что отвечают настройки в discer.q3?

- printdebuglines - bool (True/False) - Вывод отладочных строк в консоль (не слишком нужно для обычного пользователя)
- simpleverify - bool (True/False) - Не выводить данные об аккаунте в консоль (это значит, что пока нигде)
- checkonbadges - bool (True/False) - Поскольку эта функция тестируется, я добавил включение и отключение в настройках (возможно, уберу после публичного тестирования)
- printinvalidtokens - bool (True/False) - отвечает за вывод недействительных токенов в консоль (если False, то будет выводиться только ошибка о недействительном токене)
- sslverificationonrequest - bool (True/False) - отключает проверку ssl при запросе к discord (На тестах помогло оживить чекер)
Все эти настройки изменяются путем изменения файла discer.q3, если его нет в директории, скрипт создаст конфиг и попросит пользователя изменить его и перезапустить discer.
## Поддержка

Для получения поддержки напишите мне в t.me/k3kzia или присоединяйтесь к нашему каналу @bredcookie.


## Лицензия

[MIT](https://choosealicense.com/licenses/mit/)
