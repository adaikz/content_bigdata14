# Login to Master

Этот документ рассказывает, как зайти на мастер, используя сгенерированный для вас приватный ключ. 

Далее по тексту замените name.surname на ваш логин в ЛК.

### Где взять ключ

Зайдите в ЛК и найдите ключ во вкладке "Персональная информация". Скачайте его нажав на кнопку "Загрузить".

### Зачем нужен ключ

Этим ключом вы также будете пользоваться для SSH логина на мастер, для настройки прокси (см. [тут](proxy.md)), а также в первой лабораторной работе для логина на собственный кластер AWS.

## Для пользователей macOS/Linux

Зайдите в консоль (терминал).

Для начала скопируем ключ в директорию `~/.ssh` с помощью команды:

```
cp ~/Downloads/newprolab.pem ~/.ssh/.
```

Обратите внимание, возможно вам нужно заменить `~/Downloads/newprolab.pem` на реальный путь до вашего ключа, в этом примере указан путь для пользователей macOS.

Настраиваем права для ключа:

```
chmod 0600 ~/.ssh/newprolab.pem
```

С помощью этой команды ключ становится доступным только текущему пользователю, в противном случае ssh будет считать его "слишком открытым" и "небезопасным".

Заходим на master по SSH:

```
ssh -i ~/.ssh/newprolab.pem name.surname@bd-master.newprolab.com
```

При первом заходе вас спросит `Are you sure you want to continue connecting?` нужно набрать `yes`.

### Продвинутый совет для пользователей MacOS/Linux

Упростите себе жизнь при работе с SSH.

Создайте config-файл и опишите в нём ваше подключение:

```
nano ~/.ssh/config
```

Файл `config` должен иметь такую структуру:

```
Host bdmaster
HostName bd-master.newprolab.com
User name.surname
Port 22
IdentityFile ~/.ssh/newprolab.pem
ServerAliveInterval 60
```

Из nano можно выйти с сохранением:
- нажимаем CMD+X
- набираем "у" (чтобы подтвердить сохранение) и Enter

Теперь вы сможете подключаться просто используя созданный идентификатор без указания имени пользователя, хостнейма и сертификата через:

```
ssh bdmaster
```

## Для пользователей Windows

### Если у вас Windows 10

Откройте терминал Command prompt. Его можно найти или через поиск или нажать `win+R` и набрать `cmd.exe`. Также можно использовать PowerShell.

Заходим на master по SSH:

```
ssh -i path\to\newprolab.pem name.surname@bd-master.newprolab.com
```

Вам нужно заменить `path\to\newprolab.pem` на путь к ключу. Если вы скачали его в папку Загрузки, то путь будет:
```
%HOMEPATH%\Загрузки
```

или
```
%HOMEPATH%\Downloads
```

(`%HOMEPATH%` это сокращение, которое указывает на домашнюю директорию пользователя).

При первом заходе вас спросит `Are you sure you want to continue connecting?` нужно набрать `yes`.

### Инструкция по gitbash (если у вас нет поддержки ssh в терминале)

Скачайте и установите программу Git по ссылке https://gitforwindows.org/. На все вопросы выбирайте значения по умолчанию.

После установки запустите gitbash (`C:/Program Files/Git/git-bash.exe`).

Для начала скопируем ключ в директорию `~/.ssh` с помощью команды:

```
cp ~/Downloads/newprolab.pem ~/.ssh/.
```

Обратите внимание, возможно вам нужно заменить `~/Downloads/newprolab.pem` на реальный путь до вашего ключа.

Заходим на master по SSH:

```
ssh -i ~/.ssh/newprolab.pem name.surname@bd-master.newprolab.com
```

При первом заходе вас спросит `Are you sure you want to continue connecting?` нужно набрать `yes`.

### Продвинутый совет для пользователей gitbash


Упростите себе жизнь при работе с SSH.

Создайте config-файл и опишите в нём ваше подключение:

```
nano ~/.ssh/config
```

Файл `config` должен иметь такую структуру:

```
Host bdmaster
HostName bd-master.newprolab.com
User name.surname
Port 22
IdentityFile ~/.ssh/newprolab.pem
ServerAliveInterval 60
```

Из nano можно выйти с сохранением:
- нажимаем Control+X
- набираем "у" (чтобы подтвердить сохранение) и Enter

Теперь вы сможете подключаться просто используя созданный идентификатор без указания имени пользователя, хостнейма и сертификата через:

```
ssh bdmaster
```

## FAQ

---

**Q**: При попытке подключения возникает ошибка "Connection closed by 89.xxx.xxx.208 port 22"

**A**: Скорее всего вы пытались подключаться к мастеру с неправильными параметрами несколько раз, поэтому сервер вас временно заблокировал. Проверьте правильность ключа и юзернейма и попытаетесь еще раз через 10-15 минут.

Ну и наиболее редкая причина этой ошибки - ваш аккаунт не работает на сервере. Пишите координатору и попросите его проверить.

---

**Q**: При попытке подключения возникает "WARNING: UNPROTECTED PRIVATE KEY"

**A**: Для линукса/мака надо выполнить команду для ключа:

```
chmod 0600 ~/.ssh/newprolab.pem
```

Для Windows, нажмите правой кнопкой по файлу, Properties -> Security -> Edit. В поле "Group or user names" нужно удалить все записи и оставить только вашего юзера. У него должны стоять все галочки в поле Allow. См. https://stackoverflow.com/a/50877382
