B O T L I B
###########

os level integration of bot technology.

synopsis
========

| ``bot <cmd> [key=value] [key==value]``
| ``bot cfg server=<server> channel=<channel> nick=<nick>`` 
| ``bot -cv mod=irc,rss``

| ``(*) default channel/server is #botlib on localhost``

description
===========

A solid, non hackable bot, that runs under systemd as a 24/7 background
service and starts the bot after reboot, intended to be programmable in a
static, only code, no popen, no imports and no reading modules from a
directory, way that **should** make it suitable for embedding.

install
=======

| ``pip3 install botlib``

configuration
=============

configuration is done by calling the bot as a cli, bot <cmd> allows you to
run bot commands on a shell. use the cfg command to edit configuration on
disk, the botd background daemon uses the botctl program.

sasl
----

| ``bot pwd <nickservnick> <nickservpass>``
| ``bot cfg password=<outputfrompwd>``

users
-----

| ``bot cfg users=True``
| ``bot met <userhost>``

rss
---

| ``bot rss <url>``

24/7
----

| ``cp /usr/local/share/botd/botd.service /etc/systemd/system``
| ``botctl cfg server=<server> channel=<channel> nick=<nick>`` 
| ``systemctl enable botd --now``

programming
===========

**BOTLIB** is programmable, to program the bot you have to have the code
available as employing your own code requires that you install your own bot as
the system bot. This is to not have a directory to read modules from to add
commands to the bot but include the own programmed modules directly into the
python code, so only trusted code (your own written code) is included and
runnable. Reading random code from a directory is what gets avoided. As
experience tells os.popen and __import__, importlib are avoided, the bot
scans modules from sys.path (for now).

**BOTLIB** stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Files are JSON dumps
that are read-only so thus should provide (disk) persistence more change. Files
paths carry the type in the path name what makes reconstruction from filename
easier then reading type from the object. Only include your own written code
**should** be the path to "secure".

code
----

you can fetch the source code (or clone/fork) from git repository.

| ``git clone https://github.com/bthate/botlib``


or download the tar from https://pypi.org/project/botlib/#files

modules
-------

| bot.bus       event bus
| bot.clt       client
| bot.dbs	database
| bot.dpt	dispatcher
| bot.evt	event
| bot.fnd	find
| bot.hdl	handler
| bot.irc	irc bot
| bot.log	log command
| bot.obj	objects
| bot.ofn	object functions
| bot.opt	output cache
| bot.prs	parsing
| bot.rpt	repeater
| bot.rss	rss poller
| bot.run	runtime
| bot.sys	system commands
| bot.tbl	table
| bot.thr	threads
| bot.tmr	timer
| bot.tms	times
| bot.utl	utils

commands
--------

cd into the extracted directory and add your module to the bot package.

open your module file, in this example it's the hlo (hello) module and
add your command code to the file.

| ``joe bot/hlo.py``

::

  def hlo(event):
     event.reply("hello!")

then add your module to the all module so it get imported on start.

| ``joe bot/all.py``

::

  import bot.hlo as hlo
  Table.addmod(hlo)

updating
========

install the bot on the system and restart the daemon.
 
| ``python3 setup.py install``
| ``python3 setup.py install_data``
| ``systemctl restart botd``
